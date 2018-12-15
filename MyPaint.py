import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget, \
     QMessageBox, QAction, QFileDialog, QLabel, QMenu, \
     QGraphicsView, QVBoxLayout, QWidget, QGraphicsScene, QGraphicsPathItem   
from PyQt5.QtGui import QPixmap, QPen, QPainterPath, \
     QIcon
from PyQt5.QtCore import Qt


class Canvas(QGraphicsView):
    def __init__(self):
        super(Canvas, self).__init__()

        global scene
        scene = QGraphicsScene()
        self.setScene(scene)
        self.path1 = QPainterPath()
        self.path2 = QPainterPath()
        global pen
        pen = Pen()
        global eraser
        eraser = Eraser()
        global item
        item = pen
        scene.addItem(item)

    def mousePressEvent(self, event):
        self.start = self.mapToScene(event.pos())
        global item
        if item == pen:
            self.path1.moveTo(self.start)
        else:
            self.path2.moveTo(self.start)

    def mouseMoveEvent(self, event):
        self.end = self.mapToScene(event.pos())
        global item
        if item == pen:
            self.path1.lineTo(self.end)
            pen.setPath(self.path1)
        else:
            self.path2.lineTo(self.end)
            eraser.setPath(self.path2)

    @classmethod   
    def erase(self):
        global item
        item = eraser
        scene.addItem(item)

    @classmethod  
    def draw(self):
        global item
        item = pen
        scene.addItem(item)
        

class Pen(QGraphicsPathItem):
    global pen
    pen = QPen(Qt.black, 10)
    
    def __init__(self):
        super(Pen, self).__init__()

        self.setPen(pen)


class Eraser(QGraphicsPathItem):
    global eraser
    eraser = QPen(Qt.white, 10)
    
    def __init__(self):
        super(Eraser, self).__init__()

        self.setPen(eraser)


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.central_widget = QWidget()
        self.layout_container = QVBoxLayout()
        self.central_widget.setLayout(self.layout_container)
        self.setCentralWidget(self.central_widget)
        self.layout_container.addWidget(Canvas())
        
        self.initUI()

    def initUI(self):
        extractAction1 = QAction('Draw', self)
        extractAction1.triggered.connect(Canvas.draw)

        extractAction2 = QAction('Erase', self)
        extractAction2.triggered.connect(Canvas.erase)

        extractAction3 = QAction('Save', self)
        extractAction3.setShortcut('Ctrl+S')
        extractAction3.triggered.connect(self.saveto)

        extractAction4 = QAction('Open', self)
        extractAction4.setShortcut('Ctrl+O')
        extractAction4.triggered.connect(self.loadfrom)

        mainMenu = self.menuBar()

        fileMenu1 = mainMenu.addMenu('&File')
        fileMenu1.addAction(extractAction3)
        fileMenu1.addAction(extractAction4)
        
        fileMenu2 = mainMenu.addMenu('&Pen')
        fileMenu2.addAction(extractAction1)
        
        fileMenu3 = mainMenu.addMenu('&Eraser')
        fileMenu3.addAction(extractAction2)
        
        self.setGeometry(300, 300, 600, 600)
        self.center()
        self.setWindowTitle('MyPaint')
        self.setWindowIcon(QIcon('Microsoft-Paint-icon.png'))

    def saveto(self):
        name = QFileDialog.getSaveFileName(self, 'Choose file')[0]
        pixmap = QPixmap(QDesktopWidget()).toImage()
        desktop.save(self,format='jpeg')

    def loadfrom(self):
        name = QFileDialog.getOpenFileName(self, 'Choose file')[0]
        pixmap = QPixmap(name)
        self.label = QLabel(self)
        self.label.setPixmap(pixmap)
        self.label.show()
        
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Подтверждение', 'Сохранить файл?', \
                                     QMessageBox.Yes | QMessageBox.No, \
                                     QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            self.saveto()
            event.accept()
        else:
            event.accept()


    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Window()
    ex.showMaximized()
    sys.exit(app.exec_())

