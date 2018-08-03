import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
import time
import threading
from threading import Timer

class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False

class MainWindow(QMainWindow):
    totalcou=0
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setStaysOnTop(True)
        ##set fullscreen
        #self.showFullScreen()
        ##fix size
        #self.setFixedSize(self.sizeHint())
        print("kill videoplayer!")
        os.system("sudo kill -9 `pgrep -f videoplayer.py`")
        print("kill vlc")
        os.system("sudo kill -9 `pgrep -f vlc`")
        global rtt
        rtt = RepeatedTimer(1, self.counter) # it auto-starts, no need of rt.start()

        screenw=1920
        screenh=1080
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setGeometry ( 0, 0, screenw, screenh)
        self.setStyleSheet("QMainWindow {background: 'black';}")

        image_path=os.getcwd()+"/mamaro/style/img/newQA1.png"
        image_profile = QtGui.QImage(image_path) #QImage object
        lbl1 = QtWidgets.QLabel('content1', self)
        lbl1.setPixmap(QtGui.QPixmap.fromImage(image_profile))
        lbl1.setScaledContents(True)
        lbl1.setGeometry ( 0, 0, screenw, screenh)

        image_path=os.getcwd()+"/mamaro/style/img/new_QA_next.png"
        image_profile = QtGui.QImage(image_path) #QImage object
        lbl1 = QtWidgets.QLabel('contentnext', self)
        lbl1.setPixmap(QtGui.QPixmap.fromImage(image_profile))
        lbl1.setScaledContents(True)
        lbl1.setCursor(Qt.PointingHandCursor)
        lbl1.setGeometry ( (screenw/2)-(380/2), screenh-270, 350, 120)
        lbl1.mousePressEvent=self.nextclick

        image_path=os.getcwd()+"/mamaro/style/img/new_QA_close.png"
        image_profile = QtGui.QImage(image_path) #QImage object
        lbl1 = QtWidgets.QLabel('contentclose', self)
        lbl1.setPixmap(QtGui.QPixmap.fromImage(image_profile))
        lbl1.setScaledContents(True)
        lbl1.setCursor(Qt.PointingHandCursor)
        lbl1.setGeometry ( screenw-450, 150, 150, 40)
        lbl1.mousePressEvent=self.closeclick

    def setStaysOnTop(self, staysOnTop):
        if staysOnTop:
            self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(self.windowFlags() & ~ QtCore.Qt.WindowStaysOnTopHint)

    def closeEvent(self):
        #Your desired functionality here
        rtt.stop()
        print('Close button pressed')
        os._exit(1)

    def nextclick(self, event):
        thread = threading.Thread(target=self.webb, args=("Thread-7",))
        thread.daemon = True                            # Daemonize thread
        thread.start()
        thread1 = threading.Thread(target=self.topcontent, args=("Thread-5",2,))
        thread1.daemon = True                            # Daemonize thread
        thread1.start()
        rtt.stop()
        time.sleep(3)
        os._exit(1)

    def closeclick(self, event):
        thread = threading.Thread(target=self.webb, args=("Thread-2",))
        thread.daemon = True                            # Daemonize thread
        thread.start()
        rtt.stop()
        time.sleep(2)
        os._exit(1)

    def topcontent(self,threadName,delay):
        time.sleep(delay)
        os.system('python3 '+os.getcwd()+'/mamaro/QA1.py')
    def webb(self,threadName):
        os.system('python3 '+os.getcwd()+'/mamaro/mainview.py')

    def counter(self):
        self.totalcou+=1
        print(str(self.totalcou))
        if self.totalcou==5:
            thread = threading.Thread(target=self.webb, args=("Thread-7",))
            thread.daemon = True                            # Daemonize thread
            thread.start()
            thread1 = threading.Thread(target=self.topcontent, args=("Thread-5",2,))
            thread1.daemon = True                            # Daemonize thread
            thread1.start()
            time.sleep(3)
            print("stop counter")
            rtt.stop()
            os._exit(1)




app = QApplication(sys.argv)
w = MainWindow()
w.show()
sys.exit(app.exec())
