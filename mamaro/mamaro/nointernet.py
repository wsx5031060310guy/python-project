import os
import sys
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from threading import Timer
import threading
import time

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
        screenw=1920
        screenh=1080
        self.setGeometry(0,0,screenw,screenh)

        global rt
        rt = RepeatedTimer(1, self.counter) # it auto-starts, no need of rt.start()

        image_path=os.getcwd()+"/mamaro/style/img/internetNotConnectedView.png"
        image_profile = QtGui.QImage(image_path) #QImage object

        lbl1 = QtWidgets.QLabel('contentcover', self)
        lbl1.setText("")
        lbl1.setPixmap(QtGui.QPixmap.fromImage(image_profile))
        lbl1.setScaledContents(True)
        lbl1.setGeometry ( 0, 0, screenw, screenh)

        app.aboutToQuit.connect(self.closeEvent)
        # self.label = QLabel('Test', self)                        # test, if it's really backgroundimage
        # self.label.setGeometry(50,50,200,50)

        self.show()
        # super(MainWindow, self).__init__(parent)
        # self.setStaysOnTop(True)
        # ##set fullscreen
        # #self.showFullScreen()
        # ##fix size
        # #self.setFixedSize(self.sizeHint())
        # screenw=1920
        # screenh=1080
        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        # self.setGeometry ( 0, 0, screenw, screenh)
        # self.setStyleSheet("QMainWindow {background: 'black';}")



    def setStaysOnTop(self, staysOnTop):
        if staysOnTop:
            self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(self.windowFlags() & ~ QtCore.Qt.WindowStaysOnTopHint)

    def closeEvent(self):
        #Your desired functionality here
        rt.stop()
        print('Close button pressed')
        os._exit(1)

    def topcontent(self,threadName,delay):
        time.sleep(delay)
        os.system('python3 '+os.getcwd()+'/mamaro/videocover.py')
    def webb(self,threadName):
        os.system('python3 '+os.getcwd()+'/mamaro/videoplayerloop.py')

    def counter(self):
        self.totalcou+=1
        print(str(self.totalcou))
        if self.totalcou==5:
            thread = threading.Thread(target=self.webb, args=("Thread-777",))
            thread.daemon = True                            # Daemonize thread
            thread.start()
            thread1 = threading.Thread(target=self.topcontent, args=("Thread-555",1,))
            thread1.daemon = True                            # Daemonize thread
            thread1.start()
            time.sleep(2)
            print("stop counter")
            rt.stop()
            os._exit(1)

        total=60*20
        checkreadfile=True
        try:
            with open(os.getcwd()+"/mamaro/counter.text", "r+") as f:
                data = f.readlines()
                lines=data[0].split()
                total=int(lines[0])
                checkreadfile=True
        except:
            print("read counter fail")
            checkreadfile=False
            pass

        if checkreadfile:
            total-=1
            try:
                #write date time
                with open(os.getcwd()+"/mamaro/counter.text", "w+") as f:
                    f.write(str(total)+"\n")
            except:
                print("write counter fail")
                pass



if __name__ == "__main__":

    app = QApplication(sys.argv)
    oMainwindow = MainWindow()
    sys.exit(app.exec_())
