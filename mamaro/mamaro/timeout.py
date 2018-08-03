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
        app.aboutToQuit.connect(self.closeEvent)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setGeometry ( 0, 0, screenw, screenh)
        self.setStyleSheet("QMainWindow {background: 'black';}")

        image_path=os.getcwd()+"/mamaro/style/img/mamaro_time_out.png"
        image_profile = QtGui.QImage(image_path) #QImage object
        lbl1 = QtWidgets.QLabel('content1', self)
        lbl1.setPixmap(QtGui.QPixmap.fromImage(image_profile))
        lbl1.setScaledContents(True)
        lbl1.setGeometry ( 0, 0, screenw, screenh)

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
