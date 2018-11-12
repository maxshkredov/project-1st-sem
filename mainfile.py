import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget, \
     QMessageBox, QPushButton, QAction, QFileDialog, QLabel, QMenu, \
     QGraphicsView, QVBoxLayout, QWidget, QGraphicsScene
from PyQt5.QtGui import QPixmap, QColor, QPen


class Canvas(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.setScene(QGraphicsScene())

    def clear(self):
        pass


class Pen(Canvas):
    def __init__(self):
        super().__init__()
        
    def draw(self, event):
        self.start = self.mapToScene(event.pos())
        self.path.moveTo(self.start)
        self.end = self.mapToScene(event.pos())
        self.path.lineTo(self.end)
        self.start = self.end
        self.item.setPath(self.path)

    def colour(self, cl):
        pass

    def size(self, size):
        pass

class Eraser(Pen):
    def __init__(self):
        super().__init__()

    def erase(self):
        pass

class Window(QMainWindow, Pen):
    def __init__(self):
        super(Pen, self).__init__()
        
        self.central_widget = QWidget()
        self.layout_container = QVBoxLayout()
        self.central_widget.setLayout(self.layout_container)
        self.setCentralWidget(self.central_widget)
        self.layout_container.addWidget(Canvas())
        
        self.initUI()

    def initUI(self):
        extractAction1 = QAction('draw', self)
        extractAction1.triggered.connect(Pen.draw)

        extractAction2 = QAction('setColour', self)
        extractAction2.triggered.connect(Pen.colour)
        
        impMenu3 = QMenu('size', self)
        extractAction3 = QAction('setSize', self)
        extractAction3.triggered.connect(Pen.size)
        impMenu3.addAction(extractAction3)

        extractAction4 = QAction('erase', self)
        extractAction4.triggered.connect(Eraser.draw)

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
        fileMenu2.addMenu(impMenu3)
        
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
