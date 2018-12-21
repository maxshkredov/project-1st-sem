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

        global viewport
        viewport = self.viewport()

        global new_path
        new_path = Path()

        global new_pathitem, pathitem1, pathitem2
        pathitem1 = QGraphicsPathItem()
        pathitem2 = QGraphicsPathItem()
        new_pathitem = Pathitem()
        
        global pen
        pen = QPen(Qt.black, 10)
        pathitem1.setPen(pen)
        
        eraser = QPen(Qt.white, 10)
        pathitem2.setPen(eraser)

        global item
        item = pathitem1
        scene.addItem(item)

    def mousePressEvent(self, event):
        self.start = self.mapToScene(event.pos())
        if item == pathitem1:
            self.path1.moveTo(self.start)
        elif item == new_pathitem:
            new_path.moveTo(self.start)
        else:
            self.path2.moveTo(self.start)

    def mouseMoveEvent(self, event):
        self.end = self.mapToScene(event.pos())
        if item == pathitem1:
            self.path1.lineTo(self.end)
            pathitem1.setPath(self.path1)
        elif item == new_pathitem:
            new_path.lineTo(self.end)
            new_pathitem.setPath(new_path)
        else:
            self.path2.lineTo(self.end)
            pathitem2.setPath(self.path2)

    @classmethod   
    def erase(self):
        global item
        item = pathitem2
        scene.addItem(item)

    @classmethod  
    def draw(self):
        global item
        item = pathitem1
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

    @classmethod
    def loadfrom(self):
        global scene
        name = QFileDialog.getOpenFileName(None, 'Choose file')[0]  
        scene.addPixmap(QPixmap(name))

    @classmethod
    def saveto(self):
        name = QFileDialog.getSaveFileName(None, 'Choose file')[0]
        pixmap = QPixmap(viewport.size())
        viewport.render(pixmap)
        pixmap.save(name)

    @classmethod
    def save(self):
        pixmap = QPixmap(viewport.size())
        viewport.render(pixmap)
        pixmap.save('image.jpg')


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
        impMenu = QMenu('size', self)
        extractAction3 = QAction('Big', self)
        extractAction3.triggered.connect(Canvas.big_size)
        extractAction4 = QAction('Medium', self)
        extractAction4.triggered.connect(Canvas.medium_size)
        extractAction5 = QAction('Small', self)
        extractAction5.triggered.connect(Canvas.small_size)
        impMenu.addAction(extractAction3)
        impMenu.addAction(extractAction4)
        impMenu.addAction(extractAction5)

        extractAction1 = QAction('draw', self)
        extractAction1.triggered.connect(Canvas.draw)

        extractAction2 = QAction('colour', self)
        extractAction2.triggered.connect(Canvas.colour)

        extractAction6 = QAction('erase', self)
        extractAction6.triggered.connect(Canvas.erase)

        extractAction7 = QAction('save as', self)
        extractAction7.setShortcut('Ctrl+A')
        extractAction7.triggered.connect(Canvas.saveto)

        extractAction8 = QAction('save', self)
        extractAction8.setShortcut('Ctrl+S')
        extractAction8.triggered.connect(Canvas.save)

        extractAction9 = QAction('load', self)
        extractAction9.setShortcut('Ctrl+L')
        extractAction9.triggered.connect(Canvas.loadfrom)
        
        mainMenu = self.menuBar()

        fileMenu1 = mainMenu.addMenu('&File')
        fileMenu1.addAction(extractAction8)
        fileMenu1.addAction(extractAction7)
        fileMenu1.addAction(extractAction9)
        
        fileMenu2 = mainMenu.addMenu('&Pen')
        fileMenu2.addAction(extractAction1)
        fileMenu2.addAction(extractAction2)
        fileMenu2.addMenu(impMenu)
        
        fileMenu3 = mainMenu.addMenu('&Eraser')
        fileMenu3.addAction(extractAction6)
        
        self.setGeometry(300, 300, 600, 600)
        self.center()
        self.setWindowTitle('MyPaint')
        self.setWindowIcon(QIcon('Microsoft-Paint-icon.png'))

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Подтверждение', 'Сохранить файл?', \
                                     QMessageBox.Yes | QMessageBox.No, \
                                     QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            Canvas.saveto
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
