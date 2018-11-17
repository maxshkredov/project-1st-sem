import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget, \
     QMessageBox, QPushButton, QAction, QFileDialog, QLabel, QMenu, \
     QGraphicsView, QVBoxLayout, QWidget, QGraphicsScene, QGraphicsPathItem \
     
from PyQt5.QtGui import QPixmap, QColor, QPen, QPainter, QPainterPath, \
     QMouseEvent
from PyQt5.QtCore import Qt
import pdb


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
        
    @classmethod
    def set_colour(self):
        self.item.itemChange(Instrument, Instrument.colour)

    def clear(self):
        pass


class Instrument(QGraphicsPathItem):
    def __init__(self):
        super(Instrument, self).__init__()
        
        pen = QPen(Qt.black, 10)
        self.setPen(pen)

    @classmethod  
    def colour(self):
        pen.color = Qt.red

    def size(self):
        pass


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
        impMenu2 = QMenu('colour', self)
        extractAction2 = QAction('Black', self)
        extractAction2.triggered.connect(Canvas.set_colour)
        extractAction10 = QAction('White', self)
        extractAction10.triggered.connect(Canvas.set_colour)
        extractAction11 = QAction('Red', self)
        extractAction11.triggered.connect(Canvas.set_colour)
        extractAction12 = QAction('Yellow', self)
        extractAction12.triggered.connect(Canvas.set_colour)
        extractAction13 = QAction('Green', self)
        extractAction13.triggered.connect(Canvas.set_colour)
        impMenu2.addAction(extractAction2)
        impMenu2.addAction(extractAction10)
        impMenu2.addAction(extractAction11)
        impMenu2.addAction(extractAction12)
        impMenu2.addAction(extractAction13)
        
        impMenu3 = QMenu('size', self)
        extractAction3 = QAction('Big', self)
        extractAction3.triggered.connect(Instrument.size)
        extractAction8 = QAction('Medium', self)
        extractAction8.triggered.connect(Instrument.size)
        extractAction9 = QAction('Small', self)
        extractAction9.triggered.connect(Instrument.size)
        impMenu3.addAction(extractAction3)
        impMenu3.addAction(extractAction8)
        impMenu3.addAction(extractAction9)

        extractAction4 = QAction('erase', self)
        extractAction4.triggered.connect(Instrument.size)

        extractAction5 = QAction('save', self)
        extractAction5.setShortcut('Ctrl+S')
        extractAction5.triggered.connect(self.saveto)

        extractAction6 = QAction('load', self)
        extractAction6.setShortcut('Ctrl+L')
        extractAction6.triggered.connect(self.loadfrom)

        extractAction7 = QAction('clear', self)
        extractAction7.triggered.connect(Canvas().clear)

        mainMenu = self.menuBar()

        fileMenu1 = mainMenu.addMenu('&File')
        fileMenu1.addAction(extractAction5)
        fileMenu1.addAction(extractAction6)
        
        fileMenu2 = mainMenu.addMenu('&Pen')
        fileMenu2.addMenu(impMenu3)
        fileMenu2.addMenu(impMenu2)
        
        fileMenu3 = mainMenu.addMenu('&Eraser')
        fileMenu3.addAction(extractAction4)

        fileMenu4 = mainMenu.addMenu('&Canvas')
        fileMenu4.addAction(extractAction7)
        
        self.setGeometry(300, 300, 600, 600)
        self.center()
        self.setWindowTitle('MyPaint')

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
        pass

    def loadfrom(self):
        name = QFileDialog.getOpenFileName(self, 'Choose file')[0]
        pixmap = QPixmap(name)
        self.label = QLabel(self)
        self.label.setPixmap(pixmap)
        self.label.resize(pixmap.width(), pixmap.height())
        self.resize(pixmap.width(), pixmap.height())


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Window()
    ex.show()
    sys.exit(app.exec_())
