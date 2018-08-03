#! /usr/bin/python

import sys
import os.path
import os
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QMainWindow, QWidget, QFrame, QSlider, QHBoxLayout, QPushButton, \
    QVBoxLayout, QAction, QFileDialog, QApplication
from PyQt5 import QtCore, QtGui, QtWidgets
import vlc
from threading import Timer
from datetime import datetime, timedelta, date
import pymysql.cursors
import threading
import time
import requests
import urllib.request
import urllib
from requests import get  # to make GET request
import operator

def check_internet():
    url='http://www.google.com/'
    try:
        urllib.request.urlopen(url, timeout=1)
        return True
    except urllib.request.URLError as err:
        return False

def webb(threadName):
    if check_internet():
        print("start QA")
        os.system('python3 '+os.getcwd()+'/mamaro/QA.py')
    else:
        print("start no internet")
        os.system('python3 '+os.getcwd()+'/mamaro/nointernet.py')

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

class Player(QMainWindow):
    """A simple Media Player using VLC and Qt
    """
    def __init__(self, master=None):
        QMainWindow.__init__(self, master)
        self.setWindowTitle("Media Player")
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        screenw=1920
        screenh=1080
        self.setGeometry ( 0, 0, screenw, screenh)


        # creating a basic vlc instance
        self.instance = vlc.Instance()
        # creating an empty vlc media player
        self.mediaplayer = self.instance.media_player_new()
        self.mediaplayer.video_set_mouse_input(False)

        self.createUI()
        self.isPaused = False

        global rt
        rt = RepeatedTimer(1, self.counter) # it auto-starts, no need of rt.start()

    def closeEvent(self, event):
        #Your desired functionality here
        rt.stop()
        print('Close button pressed')
        os._exit(1)

    def createUI(self):

        """Set up the user interface, signals & slots
        """
        self.widget = QWidget(self)
        self.setCentralWidget(self.widget)
        self.widget.setStyleSheet("background: '#EEEEEE';")


        image_path=os.getcwd()+"/mamaro/babybedPNG/login0.png"
        image_profile = QtGui.QImage(image_path) #QImage object

        lbl1 = QtWidgets.QLabel('bluetoothstate', self)
        lbl1.setObjectName('bluetoothstate')
        lbl1.setPixmap(QtGui.QPixmap.fromImage(image_profile))
        lbl1.setScaledContents(True)
        lbl1.setGeometry ( 48, 38, 195, 120)
        lbl1.resize(lbl1.sizeHint());

        #create background
        lbl1 = QtWidgets.QLabel('back1', self)
        lbl1.setObjectName('back1')
        lbl1.setText("")
        lbl1.setFont(QtGui.QFont("ms gothic", 28))
        lbl1.setStyleSheet("background: 'white';")
        lbl1.setGeometry ( 0, 120, 297, 296)


        lbl1 = QtWidgets.QLabel('back2', self)
        lbl1.setObjectName('back2')
        lbl1.setText("")
        lbl1.setFont(QtGui.QFont("ms gothic", 28))
        lbl1.setStyleSheet("background: 'white';")
        lbl1.setGeometry ( 0, 420, 297, 296)


        lbl1 = QtWidgets.QLabel('back3', self)
        lbl1.setObjectName('back3')
        lbl1.setText("")
        lbl1.setFont(QtGui.QFont("ms gothic", 28))
        lbl1.setStyleSheet("background: 'white';")
        lbl1.setGeometry ( 0, 720, 297, 296)
        #create background


        #create icon
        image_path=os.getcwd()+"/mamaro/babybedPNG/height0.png"
        image_profile = QtGui.QImage(image_path) #QImage object

        lbl1 = QtWidgets.QLabel('heighticon', self)
        lbl1.setObjectName('heighticon')
        lbl1.setPixmap(QtGui.QPixmap.fromImage(image_profile))
        lbl1.setScaledContents(True)
        lbl1.setStyleSheet("background: 'white';")
        lbl1.setGeometry ( 91, 180, 115, 104)



        image_path=os.getcwd()+"/mamaro/babybedPNG/weight0.png"
        image_profile = QtGui.QImage(image_path) #QImage object

        lbl1 = QtWidgets.QLabel('weighticon', self)
        lbl1.setObjectName('weighticon')
        lbl1.setPixmap(QtGui.QPixmap.fromImage(image_profile))
        lbl1.setScaledContents(True)
        lbl1.setStyleSheet("background: 'white';")
        lbl1.setGeometry ( 91, 480, 115, 104)



        image_path=os.getcwd()+"/mamaro/babybedPNG/temp0.png"
        image_profile = QtGui.QImage(image_path) #QImage object

        lbl1 = QtWidgets.QLabel('tempicon', self)
        lbl1.setObjectName('tempicon')
        lbl1.setPixmap(QtGui.QPixmap.fromImage(image_profile))
        lbl1.setScaledContents(True)
        lbl1.setStyleSheet("background: 'white';")
        lbl1.setGeometry ( 91, 780, 115, 104)
        # lbl1.resize(lbl1.sizeHint());

        #create text
        lbl1 =None

        lbl1 = QtWidgets.QLabel('heighttext', self)
        lbl1.setObjectName('heighttext')
        lbl1.setText("")
        lbl1.setFont(QtGui.QFont("ms gothic", 28))
        lbl1.setStyleSheet("color:#9EA2A2;")
        #lbl1.setAlignment(QtCore.Qt.AlignTop)
        lbl1.setAlignment(QtCore.Qt.AlignCenter)
        lbl1.setGeometry ( 91, 314, 115, 46)


        lbl1 = QtWidgets.QLabel('weighttext', self)
        lbl1.setObjectName('weighttext')
        lbl1.setText("")
        lbl1.setFont(QtGui.QFont("ms gothic", 28))
        lbl1.setStyleSheet("color:#9EA2A2;")
        #lbl1.setAlignment(QtCore.Qt.AlignTop)
        lbl1.setAlignment(QtCore.Qt.AlignCenter)
        lbl1.setGeometry ( 91, 614, 115, 52)

        lbl1 = QtWidgets.QLabel('temptext', self)
        lbl1.setObjectName('temptext')
        lbl1.setText("")
        lbl1.setFont(QtGui.QFont("ms gothic", 28))
        lbl1.setStyleSheet("color:#9EA2A2;")
        #lbl1.setAlignment(QtCore.Qt.AlignTop)
        lbl1.setAlignment(QtCore.Qt.AlignCenter)
        lbl1.setGeometry ( 91, 914, 115, 46)



        lbl1 = QtWidgets.QLabel('contentcover', self)
        lbl1.setObjectName('contentcover')
        lbl1.setText("")
        lbl1.setCursor(Qt.PointingHandCursor)
        lbl1.setGeometry ( 0, 0, 297, 1080)

        lbl1.mousePressEvent=self.contentclick

        # In this widget, the video will be drawn
        if sys.platform == "darwin": # for MacOS
            from PyQt5.QtWidgets import QMacCocoaViewContainer
            videoframe = QMacCocoaViewContainer(0)
        else:
            videoframe = QtWidgets.QFrame(self)
        self.palette = videoframe.palette()
        self.palette.setColor (QPalette.Window,
                               QColor(0,0,0))
        videoframe.setObjectName('videoview')
        videoframe.setPalette(self.palette)
        videoframe.setAutoFillBackground(True)
        videoframe.mousePressEvent=self.contentclick
        videoframe.setGeometry(QtCore.QRect(298, 0, 1622, 1080))



        global connection,roomid,readcheck,playlist,sorted_x,totalfile,oneloopindex,totalindexx,checkonetime,strings2,cou
        self.OpenFile(strings2[cou])
        insertdata(sorted_x[cou].DBindex,sorted_x[cou].playindex,totalindexx)
        cou+=1
        totalindexx+=1
        print(self.mediaplayer.get_state())



    global clickmem,checkcountwork
    clickmem=True
    checkcountwork=True
    global backx,itemx,videow,bluestatew,videox
    backx=0
    itemx=91
    videow=1622
    bluestatew=48
    videox=298
    def contentclick(self, event):

        global clickmem,checkcountwork

        #hide and show
        if clickmem:
            lbl1 = self.findChild(QtWidgets.QFrame, "videoview")
            lbl1.setGeometry(QtCore.QRect(0, 0, 1920, 1080))

            lbl1 = self.findChild(QtWidgets.QLabel, "weighticon")
            lbl1.hide()
            lbl1 = self.findChild(QtWidgets.QLabel, "weighttext")
            lbl1.hide()
            lbl1 = self.findChild(QtWidgets.QLabel, "heighticon")
            lbl1.hide()
            lbl1 = self.findChild(QtWidgets.QLabel, "heighttext")
            lbl1.hide()
            lbl1 = self.findChild(QtWidgets.QLabel, "tempicon")
            lbl1.hide()
            lbl1 = self.findChild(QtWidgets.QLabel, "temptext")
            lbl1.hide()
            lbl1 = self.findChild(QtWidgets.QLabel, "bluetoothstate")
            lbl1.hide()
            lbl1 = self.findChild(QtWidgets.QLabel, "back1")
            lbl1.hide()
            lbl1 = self.findChild(QtWidgets.QLabel, "back2")
            lbl1.hide()
            lbl1 = self.findChild(QtWidgets.QLabel, "back3")
            lbl1.hide()

            lbl1 = self.findChild(QtWidgets.QLabel, "contentcover")
            lbl1.hide()

            clickmem=False
        else:
            lbl1 = self.findChild(QtWidgets.QFrame, "videoview")
            lbl1.setGeometry(QtCore.QRect(298, 0, 1622, 1080))

            lbl1 = self.findChild(QtWidgets.QLabel, "weighticon")
            lbl1.show()
            lbl1 = self.findChild(QtWidgets.QLabel, "weighttext")
            lbl1.show()
            lbl1 = self.findChild(QtWidgets.QLabel, "heighticon")
            lbl1.show()
            lbl1 = self.findChild(QtWidgets.QLabel, "heighttext")
            lbl1.show()
            lbl1 = self.findChild(QtWidgets.QLabel, "tempicon")
            lbl1.show()
            lbl1 = self.findChild(QtWidgets.QLabel, "temptext")
            lbl1.show()
            lbl1 = self.findChild(QtWidgets.QLabel, "bluetoothstate")
            lbl1.show()
            lbl1 = self.findChild(QtWidgets.QLabel, "back1")
            lbl1.show()
            lbl1 = self.findChild(QtWidgets.QLabel, "back2")
            lbl1.show()
            lbl1 = self.findChild(QtWidgets.QLabel, "back3")
            lbl1.show()

            lbl1 = self.findChild(QtWidgets.QLabel, "contentcover")
            lbl1.show()
            clickmem=True


    def slidercounter(self):
        global clickmem,backx,itemx,videow,bluestatew,videox,checkcountwork,rtt
        if clickmem:
            videox-=1
            backx-=1
            bluestatew-=1
            videow+=1
            itemx-=1
            if videow==1921:
                clickmem=False
                checkcountwork=True
                rtt.stop()
            lbl1 = self.findChild(QtWidgets.QFrame, "videoview")
            lbl1.setGeometry(QtCore.QRect(videox, 0, videow, 1080))
            lbl1 = self.findChild(QtWidgets.QLabel, "heighticon")
            lbl1.setGeometry ( itemx, 180, 115, 104)
            lbl1 = self.findChild(QtWidgets.QLabel, "heighttext")
            lbl1.setGeometry ( itemx, 314, 115, 46)
            lbl1 = self.findChild(QtWidgets.QLabel, "weighticon")
            lbl1.setGeometry ( itemx, 480, 115, 104)
            lbl1 = self.findChild(QtWidgets.QLabel, "weighttext")
            lbl1.setGeometry ( itemx, 614, 115, 52)
            lbl1 = self.findChild(QtWidgets.QLabel, "tempicon")
            lbl1.setGeometry ( itemx, 780, 115, 104)
            lbl1 = self.findChild(QtWidgets.QLabel, "temptext")
            lbl1.setGeometry ( itemx, 914, 115, 46)
            lbl1 = self.findChild(QtWidgets.QLabel, "bluetoothstate")
            lbl1.hide()
            lbl1 = self.findChild(QtWidgets.QLabel, "back1")
            lbl1.setGeometry ( backx, 120, 297, 296)
            lbl1 = self.findChild(QtWidgets.QLabel, "back2")
            lbl1.setGeometry ( backx, 420, 297, 296)
            lbl1 = self.findChild(QtWidgets.QLabel, "back3")
            lbl1.setGeometry ( backx, 720, 297, 296)
            lbl1 = self.findChild(QtWidgets.QLabel, "contentcover")
            lbl1.hide()
        else:
            videox+=1
            backx+=1
            bluestatew+=1
            videow-=1
            itemx+=1
            if videow==1621:
                clickmem=True
                checkcountwork=True
                rtt.stop()
            lbl1 = self.findChild(QtWidgets.QFrame, "videoview")
            lbl1.setGeometry(QtCore.QRect(videox, 0, videow, 1080))
            lbl1 = self.findChild(QtWidgets.QLabel, "heighticon")
            lbl1.setGeometry ( itemx, 180, 115, 104)
            lbl1 = self.findChild(QtWidgets.QLabel, "heighttext")
            lbl1.setGeometry ( itemx, 314, 115, 46)
            lbl1 = self.findChild(QtWidgets.QLabel, "weighticon")
            lbl1.setGeometry ( itemx, 480, 115, 104)
            lbl1 = self.findChild(QtWidgets.QLabel, "weighttext")
            lbl1.setGeometry ( itemx, 614, 115, 52)
            lbl1 = self.findChild(QtWidgets.QLabel, "tempicon")
            lbl1.setGeometry ( itemx, 780, 115, 104)
            lbl1 = self.findChild(QtWidgets.QLabel, "temptext")
            lbl1.setGeometry ( itemx, 914, 115, 46)
            lbl1 = self.findChild(QtWidgets.QLabel, "bluetoothstate")
            lbl1.show()
            lbl1 = self.findChild(QtWidgets.QLabel, "back1")
            lbl1.setGeometry ( backx, 120, 297, 296)
            lbl1 = self.findChild(QtWidgets.QLabel, "back2")
            lbl1.setGeometry ( backx, 420, 297, 296)
            lbl1 = self.findChild(QtWidgets.QLabel, "back3")
            lbl1.setGeometry ( backx, 720, 297, 296)
            lbl1 = self.findChild(QtWidgets.QLabel, "contentcover")
            lbl1.show()



    def PlayPause(self):
        """Toggle play/pause status
        """
        if self.mediaplayer.is_playing():
            self.mediaplayer.pause()
            #self.playbutton.setText("Play")
            self.isPaused = True
        else:
            if self.mediaplayer.play() == -1:
                self.OpenFile()
                return
            self.mediaplayer.play()
            #self.playbutton.setText("Pause")
            #self.timer.start()
            self.isPaused = False

    def Stop(self):
        """Stop player
        """
        self.mediaplayer.stop()
        self.playbutton.setText("Play")

    def OpenFile(self, filename=None):
        """Open a media file in a MediaPlayer
        """
        if filename is None:
            filename = QFileDialog.getOpenFileName(self, "Open File", os.path.expanduser('~'))[0]
        if not filename:
            return

        # create the media
        if sys.version < '3':
            filename = unicode(filename)
        self.media = self.instance.media_new(filename)
        # put the media in the media player
        self.mediaplayer.set_media(self.media)

        # parse the metadata of the file
        self.media.parse()
        # set the title of the track as window title
        self.setWindowTitle(self.media.get_meta(0))

        # the media player has to be 'connected' to the QFrame
        # (otherwise a video would be displayed in it's own window)
        # this is platform specific!
        # you have to give the id of the QFrame (or similar object) to
        # vlc, different platforms have different functions for this
        widget = self.findChild(QtWidgets.QFrame, "videoview")
        if sys.platform.startswith('linux'): # for Linux using the X Server
            self.mediaplayer.set_xwindow(widget.winId())
        elif sys.platform == "win32": # for Windows
            self.mediaplayer.set_hwnd(widget.winId())
        elif sys.platform == "darwin": # for MacOS
            self.mediaplayer.set_nsobject(int(widget.winId()))
        self.PlayPause()

    def setVolume(self, Volume):
        """Set the volume
        """
        self.mediaplayer.audio_set_volume(Volume)

    def setPosition(self, position):
        """Set the position
        """
        # setting the position to where the slider was dragged
        self.mediaplayer.set_position(position / 1000.0)
        # the vlc MediaPlayer needs a float value between 0 and 1, Qt
        # uses integer variables, so you need a factor; the higher the
        # factor, the more precise are the results
        # (1000 should be enough)

    def counter(self):
        global connection,roomid,readcheck,playlist,sorted_x,totalfile,oneloopindex,totalindexx,checkonetime,strings2,cou
        try:
            #media_ply.set_fullscreen(True)
            if self.mediaplayer.get_state() == vlc.State.Playing:
                pass
            if self.mediaplayer.get_state() == vlc.State.Ended:
                if cou != len(strings2):
                    print(cou)
                    try:
                        with open(os.getcwd()+"/mamaro/playindex.text", "w+") as f:
                            f.write(str(totalindexx)+"\n")
                    except:
                        pass
                    self.mediaplayer.set_mrl(strings2[cou])
                    insertdata(sorted_x[cou].DBindex,sorted_x[cou].playindex,totalindexx)
                    cou+=1
                    totalindexx+=1
                    self.mediaplayer.play()
                else:
                    #print("end")
                    if checkonetime:
                        checkonetime=False
                        thread = threading.Thread(target=webb, args=("Thread-123",))
                        thread.daemon = True                            # Daemonize thread
                        thread.start()
                        time.sleep(3)
                        os._exit(1)

        except KeyboardInterrupt:
            # clean up
            raise
        """updates the user interface"""

        global checkcountwork

        nowdatetime=datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
        print(nowdatetime)
        #global x,cou,y
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
                if checkcountwork:
                    if ww=="0":
                        image_path=os.getcwd()+"/mamaro/babybedPNG/weight0.png"
                        image_profile = QtGui.QImage(image_path) #QImage object
                        lbl1 = self.findChild(QtWidgets.QLabel, "weighticon")
                        lbl1.setPixmap(QtGui.QPixmap.fromImage(image_profile))

                        lbl1 = self.findChild(QtWidgets.QLabel, "weighttext")
                        lbl1.setText("")
                        countdata+=1
                    else:
                        image_path=os.getcwd()+"/mamaro/babybedPNG/weight1.png"
                        image_profile = QtGui.QImage(image_path) #QImage object
                        lbl1 = self.findChild(QtWidgets.QLabel, "weighticon")
                        lbl1.setPixmap(QtGui.QPixmap.fromImage(image_profile))

                        lbl1 = self.findChild(QtWidgets.QLabel, "weighttext")
                        lbl1.setText(ww+"kg")
                    if tem=="0":
                        image_path=os.getcwd()+"/mamaro/babybedPNG/temp0.png"
                        image_profile = QtGui.QImage(image_path) #QImage object
                        lbl1 = self.findChild(QtWidgets.QLabel, "tempicon")
                        lbl1.setPixmap(QtGui.QPixmap.fromImage(image_profile))

                        lbl1 = self.findChild(QtWidgets.QLabel, "temptext")
                        lbl1.setText("")
                        countdata+=1
                    else:
                        image_path=os.getcwd()+"/mamaro/babybedPNG/temp1.png"
                        image_profile = QtGui.QImage(image_path) #QImage object
                        lbl1 = self.findChild(QtWidgets.QLabel, "tempicon")
                        lbl1.setPixmap(QtGui.QPixmap.fromImage(image_profile))

                        lbl1 = self.findChild(QtWidgets.QLabel, "temptext")
                        lbl1.setText(tem+"°C")
                if hb=="0":
                    countdata+=1


                if hh=="0":
                    image_path=os.getcwd()+"/mamaro/babybedPNG/login0.png"
                    image_profile = QtGui.QImage(image_path) #QImage object
                    lbl1 = self.findChild(QtWidgets.QLabel, "bluetoothstate")
                    lbl1.setPixmap(QtGui.QPixmap.fromImage(image_profile))

                    image_path=os.getcwd()+"/mamaro/babybedPNG/height0.png"
                    image_profile = QtGui.QImage(image_path) #QImage object
                    lbl1 = self.findChild(QtWidgets.QLabel, "heighticon")
                    lbl1.setPixmap(QtGui.QPixmap.fromImage(image_profile))

                    lbl1 = self.findChild(QtWidgets.QLabel, "heighttext")
                    lbl1.setText("")
                else:
                    image_path=os.getcwd()+"/mamaro/babybedPNG/login1.png"
                    image_profile = QtGui.QImage(image_path) #QImage object
                    lbl1 = self.findChild(QtWidgets.QLabel, "bluetoothstate")
                    lbl1.setPixmap(QtGui.QPixmap.fromImage(image_profile))

                    image_path=os.getcwd()+"/mamaro/babybedPNG/height1.png"
                    image_profile = QtGui.QImage(image_path) #QImage object
                    lbl1 = self.findChild(QtWidgets.QLabel, "heighticon")
                    lbl1.setPixmap(QtGui.QPixmap.fromImage(image_profile))

                    lbl1 = self.findChild(QtWidgets.QLabel, "heighttext")
                    lbl1.setText(hh+"cm")

                ret+=ww+" kg\n"

                ret+=tem+" °C\n"

                # ret+=hb+" bpm\n"
                # lbl1 = self.findChild(QtWidgets.QLabel, "hrlabel")
                # lbl1.setText(hb+" bpm")
                ret+=hh+" cm\n"

                # y.append(float(hb))
                # del y[0]

        except:
            print("error with beacon value text")
            pass
def insertdata(videoid,playindex,totalindex):
    #insert data
    print("insert")
    print(str(videoid))
    print(str(playindex))
    print(str(totalindex))
    try:
        with connection.cursor() as cursor:
            with connection.cursor() as cursor:
                sql = "INSERT INTO `nursing_room_video_play_detail` (`nursing_room_id`,`nursing_room_video_info_id`,`update_time`,`play_index`,`total_play_index`) VALUES (%s,%s,NOW(),%s,%s)"
                cursor.execute(sql, (str(roomid),str(videoid),str(playindex),str(totalindex)))
                connection.commit()
    except:
        print("videoplayer insert video play time fail")
        pass


class video_info(object):
    """__init__() functions as the class constructor"""
    def __init__(self, playindex=None, filename=None, DBindex=None, check=None):
        self.playindex = playindex
        self.filename = filename
        self.DBindex = DBindex
        self.check=check
def closeEvent():
    #Your desired functionality here
    print('Close button pressed')
    os._exit(1)

global connection,roomid,readcheck,playlist,sorted_x,totalfile,oneloopindex,totalindexx,strings2,checkonetime,cou
connection=None
try:
    connection = pymysql.connect(host='host',
    user='username',
    password='password',
    db='DBname',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor)
except:
    print("connect fail")
    connection=None
    pass

roomid=38
readcheck=True
playlist=[]
sorted_x=[]
totalfile=0
oneloopindex=1
totalindexx=1
checkonetime=True
strings2=list()
cou=0


if __name__ == "__main__":
    readcheck=True
    valuelist=[]
    try:
        with open(os.getcwd()+"/mamaro/config.text", "r+") as f:
            data = f.readlines()
            lines=data[0].split(",")
            roomid=int(lines[0])
    except:
        pass
    #QWidget.setGeometry (int x, int y, int w, int h)
    print(str(roomid))
    try:
        with open(os.getcwd()+"/mamaro/playconfig.text", "r+") as f:
            data = f.readlines()
            for lines in data:
                lines=lines.replace('\n',"")
                line=lines.split(",")
                for lin in line:
                    valuelist.append(str(lin))


    except:
        readcheck=False
        pass

    if readcheck:
        totalfile=valuelist[0]
        oneloopindex=valuelist[1]
        del valuelist[0]
        del valuelist[0]
        for i in range(len(valuelist)):
            if i>0 and (i+1)%3==0:
                playlist.append(video_info(valuelist[i-1],valuelist[i-2],valuelist[i]))


    sorted_x = sorted(playlist, key=operator.attrgetter('playindex'))
    search_folder = os.getcwd()+"/mamaro/video"
    localcou=0
    localvideo=[]
    for i in range(len(sorted_x)):
        sorted_x[i].check=False
    for root, dirs, files in os.walk(search_folder): # using the os.walk module to find the files.
        for name in files:
            localcou+=1
            localvideo.append(os.path.join(name))
            for i in range(len(sorted_x)):
                if sorted_x[i].filename == os.path.join(name):
                    sorted_x[i].check=True
            """Checking the videofile in the current directory and the sub-directories"""

    strings2 = list()
    for i in range(len(sorted_x)):
        if sorted_x[i].check==False:
            del sorted_x[i]
    for i in range(len(sorted_x)):
        if sorted_x[i].check:
            strings2.append(search_folder+"/"+sorted_x[i].filename)

    print(len(strings2))
    cou=0
    totalindexx=1
    try:
        with open(os.getcwd()+"/mamaro/playindex.text", "w+") as f:
            f.write(str(totalindexx)+"\n")
    except:
        pass

    app = QApplication(sys.argv)
    player = Player()
    player.show()
    player.resize(1920, 1080)
    #player.move(300, 0)
    if sys.argv[1:]:
        player.OpenFile(sys.argv[1])
    sys.exit(app.exec_())
