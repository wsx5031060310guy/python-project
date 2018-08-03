import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from datetime import datetime, timedelta, date
import pymysql.cursors
import urllib.request, json
import _thread
import time
import decimal
from threading import Timer
from tkinter import*
import requests


# root = Tk()
# mousetime=0
# def current_position():
#     return [root.winfo_pointerx(), root.winfo_pointery()]
# pos1 = current_position()
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
    #global value
    # Connect to the database
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
    weatherlist=[]
    contentlist = []
    company_index=0
    widgets = []
    GPS_lat=0
    GPS_lng=0
    #total_time=60*20
    stopva=False
    killqatime=0
    #global value
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)
        loadUi(os.getcwd()+'/mamaro/GUI/main.ui', self)
        ##set fullscreen
        self.showFullScreen()
        ##fix size
        #self.setFixedSize(self.sizeHint())
        print("kill videoplayer")
        os.system("sudo kill -9 `pgrep -f videoplayer.py`")
        print("kill videoplayerloop")
        os.system("sudo kill -9 `pgrep -f videoplayerloop.py`")
        print("kill vlc")
        os.system("sudo kill -9 `pgrep -f vlc`")
        try:
            with open(os.getcwd()+"/mamaro/config.text", "r+") as f:
                data = f.readlines()
                lines=data[0].split(",")
                self.roomid=int(lines[0])
        except:
            pass
        #QWidget.setGeometry (int x, int y, int w, int h)
        print(str(self.roomid))
        self.getdata(self)
        self.getweatherdata(self)

        global rt
        rt = RepeatedTimer(1, self.counter) # it auto-starts, no need of rt.start()

        screenw=1920
        screenh=1080

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        app.aboutToQuit.connect(self.closeEvent)


        self.setStyleSheet("QMainWindow {background: 'white';}");


        image_path=os.getcwd()+"/mamaro/style/img/mamaro_console_logo_1.png"
        image_profile = QtGui.QImage(image_path) #QImage object
        #image_profile = image_profile.scaled(150,150, aspectRatioMode=QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation) # To scale image for example and keep its Aspect Ration

        self.lefttopicon.setPixmap(QtGui.QPixmap.fromImage(image_profile))
        self.lefttopicon.setScaledContents(True)
        self.lefttopicon.setGeometry ( 100, 20, 180, 140)
        #self.lefttopicon.resize(self.lefttopicon.sizeHint());


        image_path=os.getcwd()+"/mamaro/style/img/mamaro_console_2_1.jpg"
        image_profile = QtGui.QImage(image_path) #QImage object
        #image_profile = image_profile.scaled(250,250, aspectRatioMode=QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation) # To scale image for example and keep its Aspect Ration

        self.middle.setPixmap(QtGui.QPixmap.fromImage(image_profile))
        self.middle.setScaledContents(True)
        self.middle.setGeometry ( 0, 180, 1920, 700)

        image_path=os.getcwd()+"/mamaro/style/img/back5.png"
        image_profile = QtGui.QImage(image_path) #QImage object
        self.smallmiddle.setPixmap(QtGui.QPixmap.fromImage(image_profile))
        self.smallmiddle.setScaledContents(True)
        self.smallmiddle.setGeometry ( 100, 280, 1720, 500)

        nowdate=datetime.now().strftime('%m/%d(%a)')
        self.datela.setText(nowdate)
        self.datela.setFont(QtGui.QFont("Times", 20))
        self.datela.setStyleSheet('color:rgb(117, 114, 106 )')
        self.datela.setGeometry ( 930, 40, 100, 100)
        self.datela.resize(self.datela.sizeHint());

        nowtime=datetime.now().strftime('%H:%M')
        self.timela.setText(nowtime)
        self.timela.setFont(QtGui.QFont("Times", 35,weight=QtGui.QFont.Bold))
        self.timela.setStyleSheet('color:rgb(117, 114, 106 )')
        self.timela.setGeometry ( 920, 70, 100, 100)
        self.timela.resize(self.timela.sizeHint());

        self.counterla_2.setText("ご利用可能な残り時間")
        self.counterla_2.setFont(QtGui.QFont("Times", 18,weight=QtGui.QFont.Bold))
        self.counterla_2.setStyleSheet('color:rgb(117, 114, 106 )')
        self.counterla_2.setGeometry ( 860, 900, 100, 100)
        self.counterla_2.resize(self.counterla_2.sizeHint());

        total=60*20
        try:
            with open(os.getcwd()+"/mamaro/counter.text", "r+") as f:
                data = f.readlines()
                lines=data[0].split()
                total=int(lines[0])

        except:
            with open(os.getcwd()+'/mamaro/counter.text','w'): pass
            pass

        print(str(total))
        min=int(total/60)
        sec=total%60
        mint=str(min)
        sect=str(sec)
        if min<10:
            mint="0"+str(min)
        if sec<10:
            sect="0"+str(sec)
        self.counterla.setText(mint+" min "+sect+" sec")
        self.counterla.setFont(QtGui.QFont("Times", 40,weight=QtGui.QFont.Bold))
        self.counterla.setStyleSheet('color:rgb(117, 114, 106 )')
        self.counterla.setGeometry ( 830, 930, 100, 100)
        self.counterla.resize(self.counterla.sizeHint());


        self.rightbottom.setText("Created by")
        self.rightbottom.setFont(QtGui.QFont("Times", 13))
        self.rightbottom.setStyleSheet('color:rgb(117, 114, 106 )')
        self.rightbottom.setGeometry ( 1550, 970, 100, 100)
        self.rightbottom.resize(self.rightbottom.sizeHint());
        #MainWindow.function(self)


        image_path=os.getcwd()+"/mamaro/style/img/Trim_logo_grey.png"
        image_profile = QtGui.QImage(image_path) #QImage object
        self.rightbottom_2.setPixmap(QtGui.QPixmap.fromImage(image_profile))
        self.rightbottom_2.setScaledContents(True)
        self.rightbottom_2.setGeometry ( 1650, 920, 120, 120)



        ####weather####
        if len(self.weatherlist)>0:
            windex=0
            for i in range(len(self.weatherlist)):
                # print(self.weatherlist[i].temp)
                # print(self.weatherlist[i].icon)
                # print(self.weatherlist[i].datetime)
                nowdate=datetime.now().strftime('%Y-%m-%d')
                nowtime=datetime.now().strftime('%H:%M:%S:%f')
                d0 = datetime.strptime(nowdate+" "+nowtime, '%Y-%m-%d %H:%M:%S:%f')
                d1 = datetime.strptime(self.weatherlist[i].datetime, '%Y-%m-%d %H:%M:%S')
                if d1>d0:
                    windex=i-1
                    print(windex)
                    break

            if windex<0:
                windex=0

            image_path=os.getcwd()+"/mamaro/style/img/weather/"+self.weatherlist[windex].icon+".png"
            image_profile = QtGui.QImage(image_path) #QImage object

            self.weathericon.setPixmap(QtGui.QPixmap.fromImage(image_profile))
            self.weathericon.setScaledContents(True)
            self.weathericon.setGeometry ( 1450, 10, 65, 65)

            self.weathertime.setText("NOW")
            self.weathertime.setFont(QtGui.QFont("Times", 13))
            self.weathertime.setStyleSheet('color:rgb(117, 114, 106 )')
            self.weathertime.setGeometry ( 1463, 85, 65, 65)
            self.weathertime.resize(self.weathertime.sizeHint());

            self.weathertemp.setText(self.weatherlist[windex].temp+"°")
            self.weathertemp.setFont(QtGui.QFont("Times", 20))
            self.weathertemp.setStyleSheet('color:rgb(117, 114, 106 )')
            self.weathertemp.setGeometry ( 1467, 120, 65, 65)
            self.weathertemp.resize(self.weathertemp.sizeHint());
            windex+=1


            image_path=os.getcwd()+"/mamaro/style/img/weather_line.png"
            image_profile = QtGui.QImage(image_path) #QImage object
            self.weatherline.setPixmap(QtGui.QPixmap.fromImage(image_profile))
            self.weatherline.setScaledContents(True)
            self.weatherline.setGeometry ( 1530, 10, 2, 150)


            image_path=os.getcwd()+"/mamaro/style/img/weather/"+self.weatherlist[windex].icon+".png"
            image_profile = QtGui.QImage(image_path) #QImage object
            self.weathericon_2.setPixmap(QtGui.QPixmap.fromImage(image_profile))
            self.weathericon_2.setScaledContents(True)
            self.weathericon_2.setGeometry ( 1550, 10, 65, 65)

            d1 = datetime.strptime(self.weatherlist[windex].datetime, '%Y-%m-%d %H:%M:%S')
            datestr=""
            if d1.hour>=12:
                datestr=str(d1.hour)+"PM"
            else:
                datestr=str(d1.hour)+"AM"

            self.weathertime_2.setText(datestr)
            self.weathertime_2.setFont(QtGui.QFont("Times", 13))
            self.weathertime_2.setStyleSheet('color:rgb(117, 114, 106 )')
            self.weathertime_2.setGeometry ( 1563, 85, 65, 65)
            self.weathertime_2.resize(self.weathertime_2.sizeHint());

            self.weathertemp_2.setText(self.weatherlist[windex].temp+"°")
            self.weathertemp_2.setFont(QtGui.QFont("Times", 20))
            self.weathertemp_2.setStyleSheet('color:rgb(117, 114, 106 )')
            self.weathertemp_2.setGeometry ( 1567, 120, 65, 65)
            self.weathertemp_2.resize(self.weathertemp_2.sizeHint());
            windex+=1


            image_path=os.getcwd()+"/mamaro/style/img/weather/"+self.weatherlist[windex].icon+".png"
            image_profile = QtGui.QImage(image_path) #QImage object
            self.weathericon_3.setPixmap(QtGui.QPixmap.fromImage(image_profile))
            self.weathericon_3.setScaledContents(True)
            self.weathericon_3.setGeometry ( 1640, 10, 65, 65)

            d1 = datetime.strptime(self.weatherlist[windex].datetime, '%Y-%m-%d %H:%M:%S')
            datestr=""
            if d1.hour>=12:
                datestr=str(d1.hour)+"PM"
            else:
                datestr=str(d1.hour)+"AM"

            self.weathertime_3.setText(datestr)
            self.weathertime_3.setFont(QtGui.QFont("Times", 13))
            self.weathertime_3.setStyleSheet('color:rgb(117, 114, 106 )')
            self.weathertime_3.setGeometry ( 1653, 85, 65, 65)
            self.weathertime_3.resize(self.weathertime_3.sizeHint());

            self.weathertemp_3.setText(self.weatherlist[windex].temp+"°")
            self.weathertemp_3.setFont(QtGui.QFont("Times", 20))
            self.weathertemp_3.setStyleSheet('color:rgb(117, 114, 106 )')
            self.weathertemp_3.setGeometry ( 1657, 120, 65, 65)
            self.weathertemp_3.resize(self.weathertemp_3.sizeHint());
            windex+=1


            image_path=os.getcwd()+"/mamaro/style/img/weather/"+self.weatherlist[windex].icon+".png"
            image_profile = QtGui.QImage(image_path) #QImage object
            self.weathericon_4.setPixmap(QtGui.QPixmap.fromImage(image_profile))
            self.weathericon_4.setScaledContents(True)
            self.weathericon_4.setGeometry ( 1730, 10, 65, 65)

            d1 = datetime.strptime(self.weatherlist[windex].datetime, '%Y-%m-%d %H:%M:%S')
            datestr=""
            if d1.hour>=12:
                datestr=str(d1.hour)+"PM"
            else:
                datestr=str(d1.hour)+"AM"

            self.weathertime_4.setText(datestr)
            self.weathertime_4.setFont(QtGui.QFont("Times", 13))
            self.weathertime_4.setStyleSheet('color:rgb(117, 114, 106 )')
            self.weathertime_4.setGeometry ( 1743, 85, 65, 65)
            self.weathertime_4.resize(self.weathertime_4.sizeHint());

            self.weathertemp_4.setText(self.weatherlist[windex].temp+"°")
            self.weathertemp_4.setFont(QtGui.QFont("Times", 20))
            self.weathertemp_4.setStyleSheet('color:rgb(117, 114, 106 )')
            self.weathertemp_4.setGeometry ( 1747, 120, 65, 65)
            self.weathertemp_4.resize(self.weathertemp_4.sizeHint());
            windex+=1


            image_path=os.getcwd()+"/mamaro/style/img/weather/"+self.weatherlist[windex].icon+".png"
            image_profile = QtGui.QImage(image_path) #QImage object
            self.weathericon_5.setPixmap(QtGui.QPixmap.fromImage(image_profile))
            self.weathericon_5.setScaledContents(True)
            self.weathericon_5.setGeometry ( 1820, 10, 65, 65)

            d1 = datetime.strptime(self.weatherlist[windex].datetime, '%Y-%m-%d %H:%M:%S')
            datestr=""
            if d1.hour>=12:
                datestr=str(d1.hour)+"PM"
            else:
                datestr=str(d1.hour)+"AM"

            self.weathertime_5.setText(datestr)
            self.weathertime_5.setFont(QtGui.QFont("Times", 13))
            self.weathertime_5.setStyleSheet('color:rgb(117, 114, 106 )')
            self.weathertime_5.setGeometry ( 1833, 85, 65, 65)
            self.weathertime_5.resize(self.weathertime_5.sizeHint());

            self.weathertemp_5.setText(self.weatherlist[windex].temp+"°")
            self.weathertemp_5.setFont(QtGui.QFont("Times", 20))
            self.weathertemp_5.setStyleSheet('color:rgb(117, 114, 106 )')
            self.weathertemp_5.setGeometry ( 1837, 120, 65, 65)
            self.weathertemp_5.resize(self.weathertemp_5.sizeHint());
        else:
            self.weathericon.setText("")
            self.weathertime.setText("")
            self.weathertemp.setText("")
            self.weatherline.setText("")
            self.weathericon_2.setText("")
            self.weathertime_2.setText("")
            self.weathertemp_2.setText("")
            self.weathericon_3.setText("")
            self.weathertime_3.setText("")
            self.weathertemp_3.setText("")
            self.weathericon_4.setText("")
            self.weathertime_4.setText("")
            self.weathertemp_4.setText("")
            self.weathericon_5.setText("")
            self.weathertime_5.setText("")
            self.weathertemp_5.setText("")

        ####weather####


        ####middle content####
        image_path=os.getcwd()+"/mamaro/style/img/left2.png"
        image_profile = QtGui.QImage(image_path) #QImage object
        self.middleleft.setPixmap(QtGui.QPixmap.fromImage(image_profile))
        self.middleleft.setScaledContents(True)
        self.middleleft.setGeometry ( 130, 500, 25, 50)
        self.middleleft.setCursor(Qt.PointingHandCursor)
        self.middleleft.mousePressEvent=self.leftclick

        image_path=os.getcwd()+"/mamaro/style/img/right2.png"
        image_profile = QtGui.QImage(image_path) #QImage object
        self.middleright.setPixmap(QtGui.QPixmap.fromImage(image_profile))
        self.middleright.setScaledContents(True)
        self.middleright.setGeometry ( 1770, 500, 25, 50)
        self.middleright.setCursor(Qt.PointingHandCursor)
        self.middleright.mousePressEvent=self.rightclick


        image_path=self.contentlist[0].icon
        image_profile = QtGui.QImage(image_path) #QImage object
        self.middleicon.setPixmap(QtGui.QPixmap.fromImage(image_profile))
        self.middleicon.setScaledContents(True)
        self.middleicon.setGeometry ( 270, 350, 350, 350)

        self.middletitle.setText(self.contentlist[0].title)
        self.middletitle.setFont(QtGui.QFont("Times", 40))
        self.middletitle.setStyleSheet('color:rgb(255, 255, 255 )')
        self.middletitle.setGeometry ( 700, 390, 700, 200)
        self.middletitle.setAlignment(QtCore.Qt.AlignTop)

        self.middledes.setText(self.contentlist[0].des)
        self.middledes.setFont(QtGui.QFont("Times", 20))
        self.middledes.setStyleSheet('color:rgb(255, 255, 255 )')
        self.middledes.setGeometry ( 700, 480, 1000, 500)
        self.middledes.setWordWrap(True)
        self.middledes.setAlignment(QtCore.Qt.AlignTop)


        lbl1 = QtWidgets.QLabel('contentcover', self)
        lbl1.setText("")
        lbl1.setCursor(Qt.PointingHandCursor)
        lbl1.setGeometry ( 220, 350, 1500, 380)
        lbl1.mousePressEvent=self.contentclick

        image_path=os.getcwd()+"/mamaro/style/img/circle1.png"
        image_profile = QtGui.QImage(image_path) #QImage object

        if len(self.contentlist)%2==0:
            for i in range(len(self.contentlist)):
                lbl1 = QtWidgets.QLabel('content'+str(i), self)
                lbl1.setPixmap(QtGui.QPixmap.fromImage(image_profile))
                lbl1.setScaledContents(True)
                lbl1.setGeometry ( ((screenw/2)+10)-(20*((len(self.contentlist)/2)-i ) ), 740, 10, 10)
                self.widgets.append(lbl1)
        else:
            for i in range(len(self.contentlist)):
                lbl1 = QtWidgets.QLabel('content'+str(i), self)
                lbl1.setPixmap(QtGui.QPixmap.fromImage(image_profile))
                lbl1.setScaledContents(True)
                lbl1.setGeometry ( ((screenw/2)+20)-(20*((len(self.contentlist)/2)-i ) ), 740, 10, 10)
                self.widgets.append(lbl1)
        image_path=os.getcwd()+"/mamaro/style/img/circle.png"
        image_profile = QtGui.QImage(image_path) #QImage object
        self.widgets[0].setPixmap(QtGui.QPixmap.fromImage(image_profile))
        self.widgets[0].setScaledContents(True)



    def counter(self):


        self.killqatime+=1
        if self.killqatime==4:
            #kill QA
            os.system("sudo kill -9 `pgrep -f QA.py`")
        total=60*20
        try:
            with open(os.getcwd()+"/mamaro/counter.text", "r+") as f:
                data = f.readlines()
                lines=data[0].split()
                total=int(lines[0])

        except:
            with open(os.getcwd()+'/mamaro/counter.text','w'): pass
            pass

        total-=1
        #write date time
        with open(os.getcwd()+"/mamaro/counter.text", "w+") as f:
            f.write(str(total)+"\n")

        print(str(total))
        min=int(total/60)
        sec=total%60
        mint=str(min)
        sect=str(sec)
        if min<10:
            mint="0"+str(min)
        if sec<10:
            sect="0"+str(sec)
        self.counterla.setText(mint+" min "+sect+" sec")
        nowdate=datetime.now().strftime('%m/%d(%a)')

        nowtime=datetime.now().strftime('%H:%M')
        self.timela.setText(nowtime)



    def topcontent( self,threadName,delay):
        time.sleep(delay)
        if check_internet():
            os.system('python3 '+os.getcwd()+'/mamaro/window.py')
    def webb( self,threadName,url):
        if url=="QA":
            os.system('python3 '+os.getcwd()+'/mamaro/QA1.py')
        elif url=="Beacon":
            os.system('python3 '+os.getcwd()+'/mamaro/testblueview1.py')
        elif url=="QR":
            pass
        else:
            if check_internet():
                os.system("google-chrome --kiosk "+url)

    def find(name, path):
        for root, dirs, files in os.walk(path):
            if name in files:
                return os.path.join(root, name)
        return "null"
    def leftclick(self, event):
        image_path=os.getcwd()+"/mamaro/style/img/circle1.png"
        image_profile = QtGui.QImage(image_path) #QImage object
        self.widgets[self.company_index].setPixmap(QtGui.QPixmap.fromImage(image_profile))
        self.widgets[self.company_index].setScaledContents(True)
        self.company_index-=1
        if self.company_index<0:
            self.company_index=len(self.contentlist)-1

        print(self.company_index)
        # if self.company_index==0:
        image_path=self.contentlist[self.company_index].icon
        image_profile = QtGui.QImage(image_path) #QImage object
        self.middleicon.setPixmap(QtGui.QPixmap.fromImage(image_profile))


        self.middletitle.setText(self.contentlist[self.company_index].title)

        self.middledes.setText(self.contentlist[self.company_index].des)

        image_path=os.getcwd()+"/mamaro/style/img/circle.png"
        image_profile = QtGui.QImage(image_path) #QImage object
        self.widgets[self.company_index].setPixmap(QtGui.QPixmap.fromImage(image_profile))
        self.widgets[self.company_index].setScaledContents(True)

    def rightclick(self, event):
        image_path=os.getcwd()+"/mamaro/style/img/circle1.png"
        image_profile = QtGui.QImage(image_path) #QImage object
        self.widgets[self.company_index].setPixmap(QtGui.QPixmap.fromImage(image_profile))
        self.widgets[self.company_index].setScaledContents(True)
        self.company_index+=1
        if self.company_index>=len(self.contentlist):
            self.company_index=0

        print(self.company_index)
        # if self.company_index==0:
        image_path=self.contentlist[self.company_index].icon
        image_profile = QtGui.QImage(image_path) #QImage object
        self.middleicon.setPixmap(QtGui.QPixmap.fromImage(image_profile))



        self.middletitle.setText(self.contentlist[self.company_index].title)

        self.middledes.setText(self.contentlist[self.company_index].des)

        image_path=os.getcwd()+"/mamaro/style/img/circle.png"
        image_profile = QtGui.QImage(image_path) #QImage object
        self.widgets[self.company_index].setPixmap(QtGui.QPixmap.fromImage(image_profile))
        self.widgets[self.company_index].setScaledContents(True)

    def contentclick(self, event):
        _thread.start_new_thread( self.webb, ("Thread-2", self.contentlist[self.company_index].url, ) )
        if self.contentlist[self.company_index].url=="QA":
            pass
        elif self.contentlist[self.company_index].url=="QR":
            pass
        elif self.contentlist[self.company_index].url=="Beacon":
            pass
        else:
            _thread.start_new_thread( self.topcontent, ("Thread-1",3, ) )

        # os.system('python3 window.py')
        # os.system("google-chrome --kiosk "+self.contentlist[self.company_index].url)

    def Convert(self):
        ##kill special python script
        os.system("sudo kill -9 `pgrep -f window.py`")

        if self.comboBox.currentIndex() == 0 :
            self.textEdit_2.setPlainText( str(float(self.textEdit.toPlainText())/30) )

        else:
            self.textEdit_2.setPlainText( str(float(self.textEdit.toPlainText())*30) )

    def setzero(self):
        if len(self.textEdit_2.toPlainText()) == 0:
            self.textEdit_2.setPlainText('0')

    def closeEvent(self, event):
        #Your desired functionality here
        rt.stop()
        print('Close button pressed')
        sys.exit(0)

    def hide_layout(layout):
        layout.hide()

    def show_layout(layout):
        layout.show()

    def function(self):
        image_path=os.getcwd()+"/mamaro/style/img/mamaro_console_logo_1.png" #path to your image file
        self.show_frame_in_display(image_path)

    def show_frame_in_display(self,image_path):
        frame = QtWidgets.QWidget() #Replace it with any frame you will putting this label_image on it
        label = QtWidgets.QLabel(frame)
        image_profile = QtGui.QImage(image_path) #QImage object
        image_profile = image_profile.scaled(250,250, aspectRatioMode=QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation) # To scale image for example and keep its Aspect Ration
        label.setPixmap(QtGui.QPixmap.fromImage(image_profile))
        hbox = QtWidgets.QHBoxLayout(self)
        hbox.addWidget(label)
        self.setLayout(hbox)

    def load_image(self, image):
        """
        Call this to load a new image from the provide QImage into
        this HomographyView's scene. The image's top left corner will
        be placed at (0,0) in the scene.
        """
        self.scene_image = image
        new_scene = HomographyScene(self)
        pmap = QtGui.QPixmap().fromImage(image)
        pmapitem = new_scene.addPixmap(pmap)
        new_scene.register_pixmap(pmapitem)
        new_scene.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(0, 0, 0)))
        self.setScene(new_scene)
        self.fitInView(0, 0, pmap.width(), pmap.height(), Qt.KeepAspectRatio)
        self.show()
        self.image_loaded = True

    def getdata(self, event):
        #get data

        try:
            with self.connection.cursor() as cursor:
                with self.connection.cursor() as cursor:
                    sql = "SELECT `b`.`company_icon`,`b`.`company_name`,`b`.`company_des`,`b`.`company_url` FROM `nursing_room_connect_company` as `a` inner join `nursing_room_company` as `b` on `a`.`nursing_room_company_id`=`b`.`id` WHERE `a`.`nursing_room_id`=%s"
                    cursor.execute(sql, (self.roomid,))
                    result = cursor.fetchall()
                    for res in result:
                        self.contentlist.append(company(res['company_icon'],res['company_name'],res['company_des'],res['company_url']))
                        # print(res)
                        # print(res['company'])
            with self.connection.cursor() as cursor:
                with self.connection.cursor() as cursor:
                    sql = "SELECT * FROM `nursing_room` WHERE `id`=%s"
                    cursor.execute(sql, (self.roomid,))
                    result = cursor.fetchall()
                    for res in result:
                        self.GPS_lat=res['GPS_lat']
                        self.GPS_lng=res['GPS_lng']
        except:
            print("mainview get data fail")
            pass
        finally:
            try:
                self.connection.close()
            except:
                pass
        self.contentlist.append(company(os.getcwd()+"/mamaro/style/img/QA/170815_2.png","アンケートにご協力ください","qa","QA"))
        self.contentlist.append(company(os.getcwd()+"/mamaro/style/img/Trim_icon.png","company","text","website url"))
        self.contentlist.append(company(os.getcwd()+"/mamaro/style/img/QRadvice.png","ご意見・ご感想","advice","QR"))

        for i in range(len(self.contentlist)-3):
            try:
                instart=self.contentlist[i].icon.rfind('/')
                filena=self.contentlist[i].icon[instart+1:]
                che=True
                for root, dirs, files in os.walk(os.getcwd()+"/mamaro/style/img/"):
                    if filena in files:
                        che=False

                if che:
                    print("download")
                    urllib.request.urlretrieve(self.contentlist[i].icon, os.getcwd()+"/mamaro/style/img/"+filena)
                    self.contentlist[i].icon=os.getcwd()+"/mamaro/style/img/"+filena
                else:
                    print("no download")
                    self.contentlist[i].icon=os.getcwd()+"/mamaro/style/img/"+filena

            except:
                pass

        #contentlist.append()
        # for i in range(len(self.contentlist)):
        #     print(self.contentlist[i].icon)
    def getweatherdata(self,event):
        txtdate="1992-05-07 12:00:00:00"
        try:
            with open(os.getcwd()+"/mamaro/weather.text", "r+") as f:
                data = f.readlines()
                lines=data[0].split()

                txtdate=lines[0]+" "+lines[1]

        except:
            with open(os.getcwd()+'/mamaro/weather.text','w'): pass
            pass

        print(txtdate)
            #f.write("I'm a new line!")

        # #clear all text file
        # with open(os.getcwd()+'/mamaro/weather.text','w'): pass
        #test
        #nowdate="2018-05-07"
        nowdate=datetime.now().strftime('%Y-%m-%d')
        nowtime=datetime.now().strftime('%H:%M:%S:%f')
        d0 = datetime.strptime(nowdate+" "+nowtime, '%Y-%m-%d %H:%M:%S:%f')
        d1 = datetime.strptime(txtdate, '%Y-%m-%d %H:%M:%S:%f')
        delta = d0 - d1
        #print (delta.microseconds / 1000)
        self.weatherlist=[]
        #self.weatherlist.append(weather_info(res['company_icon'],res['company_name'],res['company_des'],res['company_url']))
        print (delta.days)
        if check_internet():
            if delta.days>3:
                #write date time
                with open(os.getcwd()+"/mamaro/weather.text", "w+") as f:
                    f.write(nowdate+" "+nowtime+"\n")
                #get weather data
                with urllib.request.urlopen("http://api.openweathermap.org/data/2.5/forecast?lat=" + str(self.GPS_lat) + "&lon=" + str(self.GPS_lng) + "&units=imperial&appid=id") as url:
                    data = json.loads(url.read().decode())
                    #print(data)
                    for resl in data["list"]:
                        with open(os.getcwd()+"/mamaro/weather.text", "a") as f:
                            #te=Decimal(float(resl["main"]["temp"])-32).quantize(Decimal('0'), rounding=ROUND_HALF_UP)
                            te=float(resl["main"]["temp"])-32
                            tempcc=decimal.Decimal((te*5)/9).quantize(decimal.Decimal('0'), rounding=decimal.ROUND_HALF_UP)

                            f.write(str(tempcc)+"\n")
                            dweb = datetime.strptime(resl["dt_txt"], '%Y-%m-%d %H:%M:%S')
                            dweb+=timedelta(hours=9)
                            f.write(resl["weather"][0]["icon"]+"\n")
                            f.write(str(dweb)+"\n")


                        self.weatherlist.append(weather_info(resl["weather"][0]["icon"],str(dweb),str(tempcc)))


                        # print(resl["main"]["temp"])
                        # print(resl["dt_txt"])
            else:
                with open(os.getcwd()+"/mamaro/weather.text", "r+") as f:
                    data = f.readlines()
                    lines=[]
                    for line in data:
                        words = line.split()
                        for word in words:
                            lines.append(word)

                    del lines[0]
                    del lines[0]
                    for i in range(len(lines)):
                        if i>0 and i%4==0:
                            self.weatherlist.append(weather_info(lines[i-3],lines[i-2]+" "+lines[i-1],lines[i-4]))



class company(object):
    """__init__() functions as the class constructor"""
    def __init__(self, icon=None, title=None, des=None,url=None):
        self.icon = icon
        self.title = title
        self.des = des
        self.url=url

class weather_info(object):
    """__init__() functions as the class constructor"""
    def __init__(self, icon=None, datetime=None, temp=None):
        self.icon = icon
        self.datetime = datetime
        self.temp = temp

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.setWindowTitle('test')
    QtWidgets.qApp.setApplicationDisplayName('main')
    w.show()
    sys.exit(app.exec_())
