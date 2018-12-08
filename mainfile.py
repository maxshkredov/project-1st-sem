import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget, \
     QMessageBox, QAction, QFileDialog, QLabel, QMenu, \
     QGraphicsView, QVBoxLayout, QWidget, QGraphicsScene, QGraphicsPathItem, \
     QColorDialog     
from PyQt5.QtGui import QPixmap, QColor, QPen, QPainterPath, \
     QMouseEvent, QIcon
from PyQt5.QtCore import Qt


class Canvas(QGraphicsView):
    def __init__(self):
        super(Canvas, self).__init__()
        
        self.setScene(QGraphicsScene())
        self.path = QPainterPath()
        self.item = Instrument()
        self.scene().addItem(self.item)

    def mousePressEvent(self, event):
        self.start = self.mapToScene(event.pos())
        self.path.moveTo(self.start)

    def mouseMoveEvent(self, event):
        self.end = self.mapToScene(event.pos())
        self.path.lineTo(self.end)
        self.start = self.end
        self.item.setPath(self.path)
        
    def clear(self):
        pass


class Instrument(QGraphicsPathItem):
    def __init__(self):
        super(Instrument, self).__init__()

        global pen
        pen = QPen(Qt.black, 10)
        self.setPen(pen)

    @classmethod
    def colour(self):
        pen.setColor(QColorDialog.getColor())

    @classmethod
    def size(self):
        pen.setWidth(15)


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
        extractAction3.triggered.connect(Instrument.size)
        extractAction8 = QAction('Medium', self)
        extractAction8.triggered.connect(Instrument.size)
        extractAction9 = QAction('Small', self)
        extractAction9.triggered.connect(Instrument.size)
        impMenu1.addAction(extractAction3)
        impMenu1.addAction(extractAction8)
        impMenu1.addAction(extractAction9)

        extractAction1 = QAction('draw', self)
        extractAction1.triggered.connect(Instrument.colour)

        extractAction2 = QAction('colour', self)
        extractAction2.triggered.connect(Instrument.colour)

        extractAction4 = QAction('erase', self)
        extractAction4.triggered.connect(Instrument.colour)

        extractAction5 = QAction('save', self)
        extractAction5.setShortcut('Ctrl+S')
        extractAction5.triggered.connect(self.saveto)

        extractAction6 = QAction('load', self)
        extractAction6.setShortcut('Ctrl+L')
        extractAction6.triggered.connect(self.loadfrom)

        extractAction7 = QAction('clear', self)
        extractAction7.triggered.connect(Canvas.clear)

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

        fileMenu4 = mainMenu.addMenu('&Canvas')
        fileMenu4.addAction(extractAction7)
        
        self.setGeometry(300, 300, 600, 600)
        self.center()
        self.setWindowTitle('MyPaint')
        self.setWindowIcon(QIcon('Microsoft-Paint-icon.png'))

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Потверждение', 'You sure, nibba?', \
                                     QMessageBox.Yes | QMessageBox.No, \
                                     QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


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
    ex.show()
    sys.exit(app.exec_())
