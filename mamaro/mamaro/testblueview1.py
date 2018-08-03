import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QSizePolicy
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen
import time
import pymysql.cursors
import requests
import urllib.request
from numpy import arange, sin, pi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from threading import Timer
from datetime import datetime, timedelta, date
import logging
import traceback

class ExceptHookHandler(object):
    ## @detail 构造函数
    #  @param logFile: log的输入地址
    #  @param mainFrame: 是否需要在主窗口中弹出提醒
    def __init__(self, logFile, mainFrame = None):
        self.__LogFile = logFile
        self.__MainFrame = mainFrame

        self.__Logger = self.__BuildLogger()
        #重定向异常捕获
        sys.excepthook = self.__HandleException

    ## @detail 创建logger类
    def __BuildLogger(self):
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        logger.addHandler(logging.FileHandler(self.__LogFile))
        return logger

    ## @detail 捕获及输出异常类
    #  @param excType: 异常类型
    #  @param excValue: 异常对象
    #  @param tb: 异常的trace back
    def __HandleException(self, excType, excValue, tb):
        # first logger
        try:
            currentTime = datetime.datetime.now()
            self.__Logger.info('Timestamp: %s'%(currentTime.strftime("%Y-%m-%d %H:%M:%S")))
            self.__Logger.error("Uncaught exception：", exc_info=(excType, excValue, tb))
            self.__Logger.info('\n')
        except:
            pass

        # then call the default handler
        sys.__excepthook__(excType, excValue, tb)

        err_msg = ''.join(traceback.format_exception(excType, excValue, tb))
        err_msg += '\n Your App happen an exception, please contact administration.'
        print(err_msg)
        # Here collecting traceback and some log files to be sent for debugging.
        # But also possible to handle the error and continue working.
        # dlg = wx.MessageDialog(None, err_msg, 'Administration', wx.OK | wx.ICON_ERROR)
        # dlg.ShowModal()
        # dlg.Destroy()



class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        # We want the axes cleared every time plot() is called
        self.axes.hold(False)

        self.compute_initial_figure()

        #
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass

class MyStaticMplCanvas(MyMplCanvas):
    """Simple canvas with a sine plot."""
    def compute_initial_figure(self):
        t = arange(0.0, 3.0, 0.01)
        s = sin(2*pi*t)
        self.axes.plot(t, s)

global x,cou,y
x = [0, 1, 2, 3, 4, 5, 6, 7, 8]
y = [0, 0, 0, 0, 0, 0, 0, 0, 0]
cou=8

class MyDynamicMplCanvas(MyMplCanvas):
    """A canvas that updates itself every second with a new plot."""

    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)
        # timer = QtCore.QTimer(self)
        # timer.timeout.connect(self.update_figure)
        # timer.start(2000)

    def compute_initial_figure(self):
        self.axes.plot(x, y, 'r')

    # def update_figure(self):
    #     global x,cou,y
    #     # Build a list of 4 random integers between 0 and 10 (both inclusive)
    #     #get ble data
    #     ret=""
    #     try:
    #         with open(os.getcwd()+"/mamaro/beacon_value.text", "r+") as f:
    #             data = f.readlines()
    #             lines=data[0].replace('\n',"")
    #             line=lines.split(",")
    #             # ww=line[0]
    #             # if line[0]=="":
    #             #     ww="0"
    #             # tem=line[1]
    #             # if line[1]=="":
    #             #     tem="0"
    #             hb=line[2]
    #             if line[2]=="":
    #                 hb="0"
    #             # hh=line[3]
    #             # if line[3]=="":
    #             #     hh="0"
    #             # ret+=ww+" kg\n"
    #             # ret+=tem+" °C\n"
    #             ret+=hb+" BPM\n"
    #             y.append(float(hb))
    #             del y[0]
    #             # ret+=hh+" cm\n"
    #
    #     except:
    #         print("error with beacon value text")
    #         pass
    #     #get ble data
    #     cou+=1
    #     #l = [random.randint(0, 10) for i in range(4)]
    #     #y.append(random.randint(0, 10))
    #     x.append(cou)
    #     del x[0]
    #
    #
    #     self.axes.plot(x, y, 'r')
    #     self.draw()

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

def check_internet():
    url='http://www.google.com/'
    try:
        urllib.request.urlopen(url, timeout=1)
        return True
    except urllib.request.URLError as err:
        return False

class MainWindow(QMainWindow):
    #controllist=[]
    connection=None

    if check_internet():
        try:
            connection = pymysql.connect(host='host',
            user='username',
            password='password',
            db='DBname',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor)
        except:
            pass

    roomid=14

    def paintEvent(self, event=None):
        painter = QPainter(self)

        painter.setOpacity(0.7)
        painter.setBrush(Qt.black)
        painter.setPen(QPen(Qt.black))
        painter.drawRect(self.rect())
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        #self.setStaysOnTop(True)
        ##set fullscreen
        #self.showFullScreen()
        ##fix size
        #self.setFixedSize(self.sizeHint())

        try:
            with open(os.getcwd()+"/mamaro/config.text", "r+") as f:
                data = f.readlines()
                lines=data[0].split(",")
                self.roomid=int(lines[0])
        except:
            pass
        print(str(self.roomid))
        screenw=1920
        screenh=1080

        global rt
        rt = RepeatedTimer(1, self.counter) # it auto-starts, no need of rt.start()

        self.setGeometry ( 0, 0, screenw, screenh)




        lbl1 = QtWidgets.QLabel('content1', self)
        lbl1.setObjectName('content1')
        lbl1.setText("")
        lbl1.setStyleSheet("background: 'white';")
        lbl1.setGeometry ( 150, 100, screenw-300, screenh-200)

        self.main_widget = QWidget(self)
        dc = MyDynamicMplCanvas(self.main_widget, width=16, height=3, dpi=100)
        #l.addWidget(sc)

        self.canvas = dc
        self.canvas.setParent(lbl1)

        self.canvas.move(5,400)

        #self.controllist.append(lbl1)

        ##language view
        image_path=os.getcwd()+"/mamaro/style/img/closebutton.png"
        image_profile = QtGui.QImage(image_path) #QImage object
        lbl1 = QtWidgets.QLabel('close', self)
        lbl1.setObjectName('close')
        lbl1.setPixmap(QtGui.QPixmap.fromImage(image_profile))
        lbl1.setScaledContents(True)
        lbl1.setCursor(Qt.PointingHandCursor)
        lbl1.setGeometry ( screenw-150-60, 150, 30, 30)
        lbl1.mousePressEvent=self.closeclick

        ####baby information####
        babyinfosize=150
        image_path=os.getcwd()+"/mamaro/style/img/weight.png"
        image_profile = QtGui.QImage(image_path) #QImage object
        lbl1 = QtWidgets.QLabel('weighticon', self)
        lbl1.setObjectName('weighticon')
        lbl1.setPixmap(QtGui.QPixmap.fromImage(image_profile))
        lbl1.setScaledContents(True)
        lbl1.setGeometry ( ((screenw/2)-400)-(babyinfosize/2)+20, 250, babyinfosize, babyinfosize)
        #self.weighticon.setCursor(Qt.PointingHandCursor)

        image_path=os.getcwd()+"/mamaro/style/img/height.png"
        image_profile = QtGui.QImage(image_path) #QImage object
        lbl1 = QtWidgets.QLabel('heighticon', self)
        lbl1.setObjectName('heighticon')
        lbl1.setPixmap(QtGui.QPixmap.fromImage(image_profile))
        lbl1.setScaledContents(True)
        lbl1.setGeometry ( (screenw/2)-(babyinfosize/2)+20, 250, babyinfosize, babyinfosize)

        image_path=os.getcwd()+"/mamaro/style/img/temperature.png"
        image_profile = QtGui.QImage(image_path) #QImage object
        lbl1 = QtWidgets.QLabel('tempicon', self)
        lbl1.setObjectName('tempicon')
        lbl1.setPixmap(QtGui.QPixmap.fromImage(image_profile))
        lbl1.setScaledContents(True)
        lbl1.setGeometry ( ((screenw/2)+400)-(babyinfosize/2)+20, 250, babyinfosize, babyinfosize)

        lbl1 = QtWidgets.QLabel('weightlabel', self)
        lbl1.setObjectName('weightlabel')
        lbl1.setText("0 kg")
        lbl1.setFont(QtGui.QFont("Times", 40))
        lbl1.setStyleSheet('color:rgb(117, 114, 106 )')
        lbl1.setGeometry ( ((screenw/2)-400)-(babyinfosize/2)+20, 420, 400, 400)
        lbl1.setAlignment(QtCore.Qt.AlignTop)

        lbl1 = QtWidgets.QLabel('heightlabel', self)
        lbl1.setObjectName('heightlabel')
        lbl1.setText("0 cm")
        lbl1.setFont(QtGui.QFont("Times", 40))
        lbl1.setStyleSheet('color:rgb(117, 114, 106 )')
        lbl1.setGeometry ( (screenw/2)-(babyinfosize/2)+20, 420, 400, 400)
        lbl1.setAlignment(QtCore.Qt.AlignTop)

        lbl1 = QtWidgets.QLabel('templabel', self)
        lbl1.setObjectName('templabel')
        lbl1.setText("0 °C")
        lbl1.setFont(QtGui.QFont("Times", 40))
        lbl1.setStyleSheet('color:rgb(117, 114, 106 )')
        lbl1.setGeometry ( ((screenw/2)+400)-(babyinfosize/2)+20, 420, 400, 400)
        lbl1.setAlignment(QtCore.Qt.AlignTop)

        lbl1 = QtWidgets.QLabel('hrlabel', self)
        lbl1.setObjectName('hrlabel')
        lbl1.setText("0 bpm")
        lbl1.setFont(QtGui.QFont("Times", 40))
        lbl1.setStyleSheet('color:rgb(117, 114, 106 )')
        lbl1.setGeometry ( (screenw/2)-(babyinfosize/2)+20, 800, 400, 400)
        lbl1.setAlignment(QtCore.Qt.AlignTop)

        image_path=os.getcwd()+"/mamaro/style/img/blueoff.png"
        image_profile = QtGui.QImage(image_path) #QImage object
        lbl1 = QtWidgets.QLabel('bluetoothstate', self)
        lbl1.setObjectName('bluetoothstate')
        lbl1.setPixmap(QtGui.QPixmap.fromImage(image_profile))
        lbl1.setScaledContents(True)
        lbl1.setGeometry ( 180, 890, 60, 60)

        lbl1 = QtWidgets.QLabel('userbluelabel', self)
        lbl1.setObjectName('userbluelabel')
        lbl1.setText("User")
        lbl1.setFont(QtGui.QFont("Times", 20))
        lbl1.setStyleSheet('color:rgb(117, 114, 106 )')
        lbl1.setGeometry ( 185, 850, 100, 100)
        lbl1.setAlignment(QtCore.Qt.AlignTop)

        lbl1 = QtWidgets.QLabel('babybedbluelabel', self)
        lbl1.setObjectName('babybedbluelabel')
        lbl1.setText("BabyBed")
        lbl1.setFont(QtGui.QFont("Times", 20))
        lbl1.setStyleSheet('color:rgb(117, 114, 106 )')
        lbl1.setGeometry ( 1630, 850, 100, 100)
        lbl1.setAlignment(QtCore.Qt.AlignTop)

        image_path=os.getcwd()+"/mamaro/style/img/blueoff.png"
        image_profile = QtGui.QImage(image_path) #QImage object
        lbl1 = QtWidgets.QLabel('bluetoothstatebaby', self)
        lbl1.setObjectName('bluetoothstatebaby')
        lbl1.setPixmap(QtGui.QPixmap.fromImage(image_profile))
        lbl1.setScaledContents(True)
        lbl1.setGeometry ( 1650, 890, 60, 60)

        ####baby information####



    def closeclick(self,event):
        os._exit(1)

    def counter(self):
        nowdatetime=datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
        print(nowdatetime)
        global x,cou,y
        #get ble data
        ret=""
        countdata=0
        try:
            with open(os.getcwd()+"/mamaro/beacon_value.text", "r+") as f:
                data = f.readlines()
                lines=data[0].replace('\n',"")
                line=lines.split(",")
                ww=line[0]
                if line[0]=="":
                    ww="0"
                tem=line[1]
                if line[1]=="":
                    tem="0"
                hb=line[2]
                if line[2]=="":
                    hb="0"
                hh=line[3]
                if line[3]=="":
                    hh="0"
                if ww=="0":
                    countdata+=1
                if tem=="0":
                    countdata+=1
                if hb=="0":
                    countdata+=1

                if countdata==3:
                    image_path=os.getcwd()+"/mamaro/style/img/blueoff.png"
                    image_profile = QtGui.QImage(image_path) #QImage object
                    lbl1 = self.findChild(QtWidgets.QLabel, "bluetoothstatebaby")
                    lbl1.setPixmap(QtGui.QPixmap.fromImage(image_profile))
                else:
                    image_path=os.getcwd()+"/mamaro/style/img/blue.png"
                    image_profile = QtGui.QImage(image_path) #QImage object
                    lbl1 = self.findChild(QtWidgets.QLabel, "bluetoothstatebaby")
                    lbl1.setPixmap(QtGui.QPixmap.fromImage(image_profile))

                if hh=="0":
                    image_path=os.getcwd()+"/mamaro/style/img/blueoff.png"
                    image_profile = QtGui.QImage(image_path) #QImage object
                    lbl1 = self.findChild(QtWidgets.QLabel, "bluetoothstate")
                    lbl1.setPixmap(QtGui.QPixmap.fromImage(image_profile))
                else:
                    image_path=os.getcwd()+"/mamaro/style/img/blue.png"
                    image_profile = QtGui.QImage(image_path) #QImage object
                    lbl1 = self.findChild(QtWidgets.QLabel, "bluetoothstate")
                    lbl1.setPixmap(QtGui.QPixmap.fromImage(image_profile))
                ret+=ww+" kg\n"
                lbl1 = self.findChild(QtWidgets.QLabel, "weightlabel")
                lbl1.setText(ww+" kg")
                ret+=tem+" °C\n"
                lbl1 = self.findChild(QtWidgets.QLabel, "templabel")
                lbl1.setText(tem+" °C")
                ret+=hb+" bpm\n"
                lbl1 = self.findChild(QtWidgets.QLabel, "hrlabel")
                lbl1.setText(hb+" bpm")
                ret+=hh+" cm\n"
                lbl1 = self.findChild(QtWidgets.QLabel, "heightlabel")
                lbl1.setText(hh+" cm")
                y.append(float(hb))
                del y[0]

        except:
            print("error with beacon value text")
            pass
        cou+=1
        x.append(cou)
        del x[0]
        self.canvas.axes.plot(x, y, 'r')
        self.canvas.draw()

    def setStaysOnTop(self, staysOnTop):
        if staysOnTop:
            self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(self.windowFlags() & ~ QtCore.Qt.WindowStaysOnTopHint)

    def closeEvent(self):
        #Your desired functionality here
        print('Close button pressed')
        os._exit(1)

sys.excepthook = ExceptHookHandler(os.getcwd()+"/errorlog.text")
app = QApplication(sys.argv)
w = MainWindow()
w.setWindowFlags(Qt.FramelessWindowHint)
w.setAttribute(Qt.WA_NoSystemBackground, True)
w.setAttribute(Qt.WA_TranslucentBackground, True)
#w.setWindowOpacity(0.5)
w.show()
sys.exit(app.exec())
