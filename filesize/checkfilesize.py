import os
import sys
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QMainWindow, QWidget, QFrame, QSlider, QHBoxLayout, QPushButton, \
    QVBoxLayout, QAction, QFileDialog, QApplication
from PyQt5 import QtCore, QtGui, QtWidgets

class checkfile(QMainWindow):
    def __init__(self, master=None):
        QMainWindow.__init__(self, master)
        self.setWindowTitle("check file size")
        self.createUI()
    def createUI(self):
        lbl1 = QtWidgets.QLabel('openfile', self)
        lbl1.setObjectName('openfile')
        lbl1.setText("Open file")
        lbl1.setFont(QtGui.QFont("ms gothic", 15))
        lbl1.setStyleSheet("color:#9EA2A2;")
        #lbl1.setAlignment(QtCore.Qt.AlignTop)
        lbl1.setAlignment(QtCore.Qt.AlignCenter)
        lbl1.setCursor(Qt.PointingHandCursor)
        lbl1.setGeometry ( 10, 10, 200, 200)
        lbl1.mousePressEvent=self.buttonclick


        lbl1 = QtWidgets.QLabel('filename', self)
        lbl1.setObjectName('filename')
        lbl1.setText("filename")
        lbl1.setFont(QtGui.QFont("ms gothic", 15))
        lbl1.setStyleSheet("color:#9EA2A2;")
        #lbl1.setAlignment(QtCore.Qt.AlignTop)
        lbl1.setAlignment(QtCore.Qt.AlignCenter)
        lbl1.setCursor(Qt.PointingHandCursor)
        lbl1.setGeometry ( 10, 210, 500, 200)
        lbl1.resize(lbl1.sizeHint());

        lbl1 = QtWidgets.QLabel('filesize', self)
        lbl1.setObjectName('filesize')
        lbl1.setText("filesize")
        lbl1.setFont(QtGui.QFont("ms gothic", 15))
        lbl1.setStyleSheet("color:#9EA2A2;")
        #lbl1.setAlignment(QtCore.Qt.AlignTop)
        lbl1.setAlignment(QtCore.Qt.AlignCenter)
        lbl1.setCursor(Qt.PointingHandCursor)
        lbl1.setGeometry ( 10, 420, 500, 200)
        lbl1.resize(lbl1.sizeHint());

    def buttonclick(self, event):
        filename = QFileDialog.getOpenFileName(self, "Open File", os.path.expanduser('~'))[0]
        filesize=os.path.getsize(filename)
        lbl1 = self.findChild(QtWidgets.QLabel, "filename")
        lbl1.setText(str(filename))
        print(str(filename))
        lbl1.resize(lbl1.sizeHint());
        lbl1 = self.findChild(QtWidgets.QLabel, "filesize")
        lbl1.setText(str(filesize))
        print(str(filesize))
        lbl1.resize(lbl1.sizeHint());

if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = checkfile()
    player.show()
    player.resize(500, 620)

    sys.exit(app.exec_())
