import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtCore, QtGui, QtWidgets


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setStaysOnTop(True)
        ##set fullscreen
        #self.showFullScreen()
        ##fix size
        #self.setFixedSize(self.sizeHint())
        screenw=1920
        screenh=1080
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setGeometry ( 0, 0, screenw, screenh)
        self.setStyleSheet("QMainWindow {background: 'black';}")
        app.aboutToQuit.connect(self.closeEvent)


    def setStaysOnTop(self, staysOnTop):
        if staysOnTop:
            self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(self.windowFlags() & ~ QtCore.Qt.WindowStaysOnTopHint)

    def closeEvent(self):
        #Your desired functionality here
        print('Close button pressed')
        os._exit(1)

app = QApplication(sys.argv)
w = MainWindow()
w.show()
sys.exit(app.exec())
