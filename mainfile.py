import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget, \
     QMessageBox, QAction, QFileDialog, QLabel, QMenu, \
     QGraphicsView, QVBoxLayout, QWidget, QGraphicsScene, QGraphicsPathItem, \
     QColorDialog     
from PyQt5.QtGui import QPixmap, QPen, QPainterPath, \
     QMouseEvent, QIcon
from PyQt5.QtCore import Qt

        
class Pathitem(QGraphicsPathItem):
    def __init__(self):
        super(Pathitem, self).__init__()


class Path(QPainterPath):
    def __init__(self):
        super(Path, self).__init__()

        
class Canvas(QGraphicsView):
    def __init__(self):
        super(Canvas, self).__init__()

        global scene
        scene = QGraphicsScene()
        self.setScene(scene)
        self.path1 = QPainterPath()
        self.path2 = QPainterPath()

        global new_path
        new_path = Path()

        global new_pathitem, pathitem1, pathitem
        pathitem1 = QGraphicsPathItem()
        pathitem = Pathitem()
        new_pathitem = Pathitem()
        
        global pen
        pen = QPen(Qt.black, 10)
        pathitem.setPen(pen)
        
        eraser = QPen(Qt.white, 10)
        pathitem1.setPen(eraser)

        global item
        item = pathitem
        scene.addItem(item)

    def mousePressEvent(self, event):
        self.start = self.mapToScene(event.pos())
        global item, new_pathitem, new_path, pen
        if item == pathitem1:
            self.path1.moveTo(self.start)
        elif item == new_pathitem:
            new_path.moveTo(self.start)
        else:
            self.path2.moveTo(self.start)

    def mouseMoveEvent(self, event):
        self.end = self.mapToScene(event.pos())
        global item, new_pathitem, new_path
        if item == pathitem:
            self.path1.lineTo(self.end)
            item.setPath(self.path1)
        elif item == new_pathitem:
            new_path.lineTo(self.end)
            new_pathitem.setPath(new_path)
        else:
            self.path2.lineTo(self.end)
            pathitem1.setPath(self.path2)

    @classmethod   
    def erase(self):
        global item
        item = pathitem1
        scene.addItem(item)

    @classmethod  
    def draw(self):
        global item
        item = pathitem
        scene.addItem(item)
    
    @classmethod
    def big_size(self):
        global item, new_pathitem, new_path
        pen.setWidth(15)
        new_pathitem = Pathitem()
        new_pathitem.setPen(pen)
        new_path = Path()
        item = new_pathitem
        scene.addItem(item)

    @classmethod
    def medium_size(self):
        global item, new_pathitem, new_path
        pen.setWidth(10)
        new_pathitem = Pathitem()
        new_pathitem.setPen(pen)
        new_path = Path()
        item = new_pathitem
        scene.addItem(item)

    @classmethod
    def small_size(self):
        global item, new_pathitem, new_path
        pen.setWidth(5)
        new_pathitem = Pathitem()
        new_pathitem.setPen(pen)
        new_path = Path()
        item = new_pathitem
        scene.addItem(item)

    @classmethod
    def colour(self):
        global item, new_pathitem, new_path
        pen.setColor(QColorDialog.getColor())
        new_pathitem = Pathitem()
        new_pathitem.setPen(pen)
        new_path = Path()
        item = new_pathitem
        scene.addItem(item)


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
        impMenu1 = QMenu('size', self)
        extractAction3 = QAction('Big', self)
        extractAction3.triggered.connect(Canvas.big_size)
        extractAction8 = QAction('Medium', self)
        extractAction8.triggered.connect(Canvas.medium_size)
        extractAction9 = QAction('Small', self)
        extractAction9.triggered.connect(Canvas.small_size)
        impMenu1.addAction(extractAction3)
        impMenu1.addAction(extractAction8)
        impMenu1.addAction(extractAction9)

        extractAction1 = QAction('draw', self)
        extractAction1.triggered.connect(Canvas.draw)

        extractAction2 = QAction('colour', self)
        extractAction2.triggered.connect(Canvas.colour)

        extractAction4 = QAction('erase', self)
        extractAction4.triggered.connect(Canvas.erase)

        extractAction5 = QAction('save', self)
        extractAction5.setShortcut('Ctrl+S')
        extractAction5.triggered.connect(self.saveto)

        extractAction6 = QAction('load', self)
        extractAction6.setShortcut('Ctrl+L')
        extractAction6.triggered.connect(self.loadfrom)
        mainMenu = self.menuBar()

        fileMenu1 = mainMenu.addMenu('&File')
        fileMenu1.addAction(extractAction5)
        fileMenu1.addAction(extractAction6)
        
        fileMenu2 = mainMenu.addMenu('&Pen')
        fileMenu2.addAction(extractAction1)
        fileMenu2.addAction(extractAction2)
        fileMenu2.addMenu(impMenu1)
        
        fileMenu3 = mainMenu.addMenu('&Eraser')
        fileMenu3.addAction(extractAction4)
        
        self.setGeometry(300, 300, 600, 600)
        self.center()
        self.setWindowTitle('MyPaint')
        self.setWindowIcon(QIcon('Microsoft-Paint-icon.png'))

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Подтверждение', 'Сохранить файл?', \
                                     QMessageBox.Yes | QMessageBox.No, \
                                     QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            self.saveto
            event.accept()
        else:
            event.accept()


    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def saveto(self):
        name = QFileDialog.getSaveFileName(self, 'Choose file')[0]

    def loadfrom(self):
        name = QFileDialog.getOpenFileName(self, 'Choose file')[0]
        pixmap = QPixmap(name)
        self.label = QLabel(self)
        self.label.show()
        self.label.setPixmap(pixmap)
        self.label.resize(pixmap.width(), pixmap.height())
        self.resize(pixmap.width(), pixmap.height())



if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Window()
    ex.showMaximized()
    sys.exit(app.exec_())
