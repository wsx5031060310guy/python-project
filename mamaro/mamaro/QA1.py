import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen
import time
import pymysql.cursors
import requests
import urllib.request

class Button(QtWidgets.QPushButton):

    def enterEvent(self, QEvent):
        # here the code for mouse hover
        self.setStyleSheet("background-color: rgba(135,222,188,255);border: none")
        pass

    def leaveEvent(self, QEvent):
        # here the code for mouse leave
        self.setStyleSheet("background-color: rgba(240,240,240,255);border: none")
        pass
class backButton(QtWidgets.QPushButton):

    def enterEvent(self, QEvent):
        # here the code for mouse hover
        self.setStyleSheet("background-color: rgba(135,222,188,255);border: none;border-radius: 50%;")
        pass

    def leaveEvent(self, QEvent):
        # here the code for mouse leave
        self.setStyleSheet("background-color: rgba(240,240,240,255);border: none;border-radius: 50%;")
        pass

class choiceButton(QtWidgets.QPushButton):
    DBname=""
    checkclick=True
    def enterEvent(self, QEvent):
        # here the code for mouse hover
        if self.checkclick:
            self.setStyleSheet("background-color: rgba(135,222,188,255);border: none;border-radius: 8px;")
        pass

    def leaveEvent(self, QEvent):
        # here the code for mouse leave
        if self.checkclick:
            self.setStyleSheet("background-color: rgba(240,240,240,255);border: none;border-radius: 8px;")
        pass


class iconButton(QtWidgets.QToolButton):
    DBname=""
    def enterEvent(self, QEvent):
        # here the code for mouse hover
        self.setStyleSheet("background-color: rgba(135,222,188,255);border: none;border-radius: 8px;padding-top: 40px;")
        pass

    def leaveEvent(self, QEvent):
        # here the code for mouse leave
        self.setStyleSheet("background-color: rgba(240,240,240,255);border: none;border-radius: 8px;padding-top: 40px;")
        pass
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
    viewindex=0
    dblanguage="日本語"
    dbbabyyearmonthlist=["0 歳 0 〜 3 ヶ月","0 歳 3 〜 6 ヶ月","0 歳 6 〜 9 ヶ月","0 歳 9 〜 12 ヶ月","1 歳 0 〜 3 ヶ月","1 歳 3 〜 6 ヶ月","1 歳 6 〜 9 ヶ月","1 歳 9 〜 12 ヶ月","2 歳 以上"]
    dbbabyyearmonth=0
    dbparentlist=["ママ","パパ","その他"]
    dbparent=0
    Q2choice=""
    Q3choice=""
    Q4choice=""
    Q5choicelist=[0,0,0,0,0,0,0,0]
    Q5choice=""
    Q6choice=""
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
        print("kill QA")
        os.system("sudo kill -9 `pgrep -f QA.py`")
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
        self.setGeometry ( 0, 0, screenw, screenh)

        lbl1 = QtWidgets.QLabel('content1', self)
        lbl1.setObjectName('content1')
        lbl1.setText("")
        lbl1.setStyleSheet("background: 'white';")
        lbl1.setGeometry ( 150, 100, screenw-300, screenh-200)
        lbl1.mousePressEvent=self.conentclick
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

        image_path=os.getcwd()+"/mamaro/style/img/QA/170815_3.png"
        image_profile = QtGui.QImage(image_path) #QImage object
        lbl1 = QtWidgets.QLabel('lan1', self)
        lbl1.setObjectName('lan1')
        lbl1.setPixmap(QtGui.QPixmap.fromImage(image_profile))
        lbl1.setScaledContents(True)
        lbl1.setGeometry ( 500, 400, 150, 150)

        lbl1 = QtWidgets.QLabel('lan2', self)
        lbl1.setObjectName('lan2')
        lbl1.setFont(QtGui.QFont("ms gothic", 35))
        lbl1.setText("言語 (language)")
        lbl1.setAlignment(QtCore.Qt.AlignTop)
        lbl1.setGeometry ( 700, 470, 400, 300)

        comboBox = QtWidgets.QComboBox(self)
        comboBox.setObjectName('lan3')
        comboBox.setStyleSheet("text-align: center;")
        comboBox.setFont(QtGui.QFont("ms gothic", 30))
        comboBox.addItem("日本語")
        comboBox.addItem("English")
        comboBox.addItem("繁體中文")
        comboBox.addItem("简体中文")
        comboBox.addItem("Vietnamese")
        comboBox.setGeometry ( 1100, 450, 300, 90)

        comboBox.activated[str].connect(self.style_choice)

        lbl1 = Button('nextbutton', self)
        lbl1.setObjectName('nextbutton')
        lbl1.setText("次へ")
        lbl1.setFont(QtGui.QFont("ms gothic", 30))
        lbl1.setStyleSheet("background-color: rgba(240,240,240,255);border: none")
        lbl1.setGeometry ( (screenw/2)-(300/2), 850, 300, 100)
        lbl1.setFocusPolicy(QtCore.Qt.NoFocus)
        lbl1.setCursor(Qt.PointingHandCursor)
        lbl1.clicked.connect(self.nextclick)

        lbl1 = backButton('backbutton', self)
        lbl1.setObjectName('backbutton')
        lbl1.setText("戻る")
        lbl1.setFont(QtGui.QFont("ms gothic", 20))
        lbl1.setStyleSheet("background-color: rgba(240,240,240,255);border: none;border-radius: 50%;")
        lbl1.setGeometry ( 200, 850, 100, 100)
        lbl1.setFocusPolicy(QtCore.Qt.NoFocus)
        lbl1.setCursor(Qt.PointingHandCursor)
        lbl1.clicked.connect(self.backclick)
        lbl1.hide()

        ##language view

        ##top view
        lbl1 = QtWidgets.QLabel('toppan', self)
        lbl1.setObjectName('toppan')
        lbl1.setText("")
        lbl1.setStyleSheet("background: #6AD5AC;")
        lbl1.setGeometry ( 150, 100, screenw-300, 130)
        lbl1.hide()

        lbl1 = QtWidgets.QLabel('toptext', self)
        lbl1.setObjectName('toptext')
        lbl1.setText("利用されるお子さまについて教えてください。")
        lbl1.setFont(QtGui.QFont("ms gothic", 30))
        lbl1.setAlignment(QtCore.Qt.AlignCenter)
        lbl1.setStyleSheet("color: 'white';text-align: center;")
        lbl1.setGeometry ( 250, 100, screenw-500, 130)
        lbl1.hide()

        lbl1 = QtWidgets.QLabel('toptext1', self)
        lbl1.setObjectName('toptext1')
        lbl1.setText("Q  1 / 5")
        lbl1.setFont(QtGui.QFont("ms gothic", 30))
        lbl1.setStyleSheet("color: 'white';text-align: center;")
        lbl1.setGeometry ( 200, 100, 200, 130)
        lbl1.hide()

        lbl1 = QtWidgets.QLabel('toptext2', self)
        lbl1.setObjectName('toptext2')
        lbl1.setText("利用されるお子さまについて教えてください。")
        lbl1.setFont(QtGui.QFont("ms gothic", 30))
        lbl1.setAlignment(QtCore.Qt.AlignCenter)
        lbl1.setStyleSheet("color: 'white';text-align: center;")
        lbl1.setGeometry ( 250, 70, screenw-500, 130)
        lbl1.hide()

        lbl1 = QtWidgets.QLabel('toptext3', self)
        lbl1.setObjectName('toptext3')
        lbl1.setText("利用されるお子さまについて教えてください。")
        lbl1.setFont(QtGui.QFont("ms gothic", 30))
        lbl1.setAlignment(QtCore.Qt.AlignCenter)
        lbl1.setStyleSheet("color: 'white';text-align: center;")
        lbl1.setGeometry ( 250, 130, screenw-500, 130)
        lbl1.hide()

        image_path=os.getcwd()+"/mamaro/style/img/closebutton1.png"
        image_profile = QtGui.QImage(image_path) #QImage object
        lbl1 = QtWidgets.QLabel('topclose', self)
        lbl1.setObjectName('topclose')
        lbl1.setPixmap(QtGui.QPixmap.fromImage(image_profile))
        lbl1.setScaledContents(True)
        lbl1.setCursor(Qt.PointingHandCursor)
        lbl1.setGeometry ( screenw-150-60, 150, 30, 30)
        lbl1.mousePressEvent=self.closeclick
        lbl1.hide()
        ##top view
        ##Q1 view
        image_path=os.getcwd()+"/mamaro/style/img/QA/new1.png"
        image_profile = QtGui.QImage(image_path) #QImage object
        lbl1 = QtWidgets.QLabel('Q1_1', self)
        lbl1.setObjectName('Q1_1')
        lbl1.setPixmap(QtGui.QPixmap.fromImage(image_profile))
        lbl1.setScaledContents(True)
        lbl1.setCursor(Qt.PointingHandCursor)
        lbl1.setGeometry ( (screenw/2)-450, 300, 200, 200)
        lbl1.hide()

        lbl1 = QtWidgets.QLabel('Q1_2', self)
        lbl1.setObjectName('Q1_2')
        lbl1.setText("お子さまのご年齢は")
        lbl1.setFont(QtGui.QFont("ms gothic", 30))
        lbl1.setAlignment(QtCore.Qt.AlignTop)
        lbl1.setGeometry ( screenw/2-100, 300, 500, 130)
        lbl1.hide()

        comboBox = QtWidgets.QComboBox(self)
        comboBox.setObjectName('Q1_3')
        comboBox.setStyleSheet("text-align: center;")
        comboBox.setFont(QtGui.QFont("ms gothic", 30))
        comboBox.addItem("0 歳 0 〜 3 ヶ月")
        comboBox.addItem("0 歳 3 〜 6 ヶ月")
        comboBox.addItem("0 歳 6 〜 9 ヶ月")
        comboBox.addItem("0 歳 9 〜 12 ヶ月")
        comboBox.addItem("1 歳 0 〜 3 ヶ月")
        comboBox.addItem("1 歳 3 〜 6 ヶ月")
        comboBox.addItem("1 歳 6 〜 9 ヶ月")
        comboBox.addItem("1 歳 9 〜 12 ヶ月")
        comboBox.addItem("2 歳 以上")
        comboBox.setGeometry ( screenw/2-100, 370, 500, 90)

        comboBox.activated[str].connect(self.style_choice1)
        comboBox.hide()

        image_path=os.getcwd()+"/mamaro/style/img/QA/170815_5.png"
        image_profile = QtGui.QImage(image_path) #QImage object
        lbl1 = QtWidgets.QLabel('Q1_4', self)
        lbl1.setObjectName('Q1_4')
        lbl1.setPixmap(QtGui.QPixmap.fromImage(image_profile))
        lbl1.setScaledContents(True)
        lbl1.setCursor(Qt.PointingHandCursor)
        lbl1.setGeometry ( (screenw/2)-450, 600, 200, 200)
        lbl1.hide()

        lbl1 = QtWidgets.QLabel('Q1_5', self)
        lbl1.setObjectName('Q1_5')
        lbl1.setText("お子さまとの関係")
        lbl1.setFont(QtGui.QFont("ms gothic", 30))
        lbl1.setAlignment(QtCore.Qt.AlignTop)
        lbl1.setGeometry ( screenw/2-100, 600, 500, 130)
        lbl1.hide()

        comboBox = QtWidgets.QComboBox(self)
        comboBox.setObjectName('Q1_6')
        comboBox.setStyleSheet("text-align: center;")
        comboBox.setFont(QtGui.QFont("ms gothic", 30))
        comboBox.addItem("ママ")
        comboBox.addItem("パパ")
        comboBox.addItem("その他")
        comboBox.setGeometry ( screenw/2-100, 670, 500, 90)

        comboBox.activated[str].connect(self.style_choice2)
        comboBox.hide()
        ##Q1 view
        ##Q2 view choiceButton
        lbl1 = choiceButton('Q2button_1', self)
        lbl1.setObjectName('Q2button_1')
        lbl1.setText("はじめて")
        lbl1.DBname="はじめて"
        lbl1.setFont(QtGui.QFont("ms gothic", 30))
        lbl1.setStyleSheet("background-color: rgba(240,240,240,255);border: none;border-radius: 8px;")
        lbl1.setGeometry ( (screenw/2)-(400/2)-420, 350, 400, 400)
        lbl1.setFocusPolicy(QtCore.Qt.NoFocus)
        lbl1.setCursor(Qt.PointingHandCursor)
        lbl1.clicked.connect(self.Q2click)
        lbl1.hide()

        lbl1 = choiceButton('Q2button_2', self)
        lbl1.setObjectName('Q2button_2')
        lbl1.setText("2 ～ 9回")
        lbl1.DBname="2 ～ 9回"
        lbl1.setFont(QtGui.QFont("ms gothic", 30))
        lbl1.setStyleSheet("background-color: rgba(240,240,240,255);border: none;border-radius: 8px;")
        lbl1.setGeometry ( (screenw/2)-(400/2), 350, 400, 400)
        lbl1.setFocusPolicy(QtCore.Qt.NoFocus)
        lbl1.setCursor(Qt.PointingHandCursor)
        lbl1.clicked.connect(self.Q2click)
        lbl1.hide()

        lbl1 = choiceButton('Q2button_3', self)
        lbl1.setObjectName('Q2button_3')
        lbl1.setText("10回以上")
        lbl1.DBname="10回以上"
        lbl1.setFont(QtGui.QFont("ms gothic", 30))
        lbl1.setStyleSheet("background-color: rgba(240,240,240,255);border: none;border-radius: 8px;")
        lbl1.setGeometry (  (screenw/2)-(400/2)+420, 350, 400, 400)
        lbl1.setFocusPolicy(QtCore.Qt.NoFocus)
        lbl1.setCursor(Qt.PointingHandCursor)
        lbl1.clicked.connect(self.Q2click)
        lbl1.hide()
        ##Q2 view
        ##Q3 view iconButton
        Q3size=300
        Q3top=250
        Q3imgsize=110

        lbl1 = iconButton(self)
        lbl1.setObjectName('Q3button_1')
        lbl1.setText("施設の案内")
        lbl1.DBname="施設の案内"
        lbl1.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        lbl1.setFont(QtGui.QFont("ms gothic", 20))
        lbl1.setStyleSheet("background-color: rgba(240,240,240,255);border: none;border-radius: 8px;padding-top: 40px;")
        lbl1.setIcon(QtGui.QIcon(os.getcwd()+"/mamaro/style/img/QA/170815_8.png"))
        lbl1.setIconSize(QtCore.QSize(Q3imgsize,Q3imgsize))
        lbl1.setGeometry ( (screenw/2)-(Q3size/2)-(Q3size+20), Q3top, Q3size, Q3size)
        lbl1.setFocusPolicy(QtCore.Qt.NoFocus)
        lbl1.setCursor(Qt.PointingHandCursor)
        #lbl1.setOrientation(QtCore.Qt.Horizontal)
        lbl1.clicked.connect(self.Q3click)
        lbl1.hide()

        lbl1 = iconButton(self)
        lbl1.setObjectName('Q3button_2')
        lbl1.setText("通りがかりに")
        lbl1.DBname="通りがかりに"
        lbl1.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        lbl1.setFont(QtGui.QFont("ms gothic", 20))
        lbl1.setStyleSheet("background-color: rgba(240,240,240,255);border: none;border-radius: 8px;padding-top: 40px;")
        lbl1.setIcon(QtGui.QIcon(os.getcwd()+"/mamaro/style/img/QA/170815_17.png"))
        lbl1.setIconSize(QtCore.QSize(Q3imgsize,Q3imgsize))
        lbl1.setGeometry ( (screenw/2)-(Q3size/2), Q3top, Q3size, Q3size)
        lbl1.setFocusPolicy(QtCore.Qt.NoFocus)
        lbl1.setCursor(Qt.PointingHandCursor)
        lbl1.clicked.connect(self.Q3click)
        lbl1.hide()

        lbl1 = iconButton( self)
        lbl1.setObjectName('Q3button_3')
        lbl1.setText("Babymap")
        lbl1.DBname="Babymap"
        lbl1.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        lbl1.setFont(QtGui.QFont("ms gothic", 20))
        lbl1.setStyleSheet("background-color: rgba(240,240,240,255);border: none;border-radius: 8px;padding-top: 40px;")
        lbl1.setIcon(QtGui.QIcon(os.getcwd()+"/mamaro/style/img/QA/170815_16.png"))
        lbl1.setIconSize(QtCore.QSize(Q3imgsize,Q3imgsize))
        lbl1.setGeometry (  (screenw/2)-(Q3size/2)+(Q3size+20), Q3top, Q3size, Q3size)
        lbl1.setFocusPolicy(QtCore.Qt.NoFocus)
        lbl1.setCursor(Qt.PointingHandCursor)
        lbl1.clicked.connect(self.Q3click)
        lbl1.hide()

        Q3top=570

        lbl1 = iconButton(self)
        lbl1.setObjectName('Q3button_4')
        lbl1.setText("知人から")
        lbl1.DBname="知人から"
        lbl1.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        lbl1.setFont(QtGui.QFont("ms gothic", 20))
        lbl1.setStyleSheet("background-color: rgba(240,240,240,255);border: none;border-radius: 8px;padding-top: 40px;")
        lbl1.setIcon(QtGui.QIcon(os.getcwd()+"/mamaro/style/img/QA/170815_15.png"))
        lbl1.setIconSize(QtCore.QSize(Q3imgsize,Q3imgsize))
        lbl1.setGeometry ( (screenw/2)-(Q3size/2)-(Q3size+20), Q3top, Q3size, Q3size)
        lbl1.setFocusPolicy(QtCore.Qt.NoFocus)
        lbl1.setCursor(Qt.PointingHandCursor)
        lbl1.clicked.connect(self.Q3click)
        lbl1.hide()

        lbl1 = iconButton(self)
        lbl1.setObjectName('Q3button_5')
        lbl1.setText("ネットニュース")
        lbl1.DBname="ネットニュース"
        lbl1.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        lbl1.setFont(QtGui.QFont("ms gothic", 20))
        lbl1.setStyleSheet("background-color: rgba(240,240,240,255);border: none;border-radius: 8px;padding-top: 40px;")
        lbl1.setIcon(QtGui.QIcon(os.getcwd()+"/mamaro/style/img/QA/170815_13.png"))
        lbl1.setIconSize(QtCore.QSize(Q3imgsize,Q3imgsize))
        lbl1.setGeometry ( (screenw/2)-(Q3size/2), Q3top, Q3size, Q3size)
        lbl1.setFocusPolicy(QtCore.Qt.NoFocus)
        lbl1.setCursor(Qt.PointingHandCursor)
        lbl1.clicked.connect(self.Q3click)
        lbl1.hide()

        lbl1 = iconButton(self)
        lbl1.setObjectName('Q3button_6')
        lbl1.setText("その他")
        lbl1.DBname="その他"
        lbl1.setFont(QtGui.QFont("ms gothic", 25))
        lbl1.setStyleSheet("background-color: rgba(240,240,240,255);border: none;border-radius: 8px;padding-top: 40px;")
        lbl1.setGeometry (  (screenw/2)-(Q3size/2)+(Q3size+20), Q3top, Q3size, Q3size)
        lbl1.setFocusPolicy(QtCore.Qt.NoFocus)
        lbl1.setCursor(Qt.PointingHandCursor)
        lbl1.clicked.connect(self.Q3click)
        lbl1.hide()
        ##Q3 view
        ##Q4 view
        lbl1 = choiceButton('Q4button_1', self)
        lbl1.setObjectName('Q4button_1')
        lbl1.setText("利用している")
        lbl1.DBname="利用している"
        lbl1.setFont(QtGui.QFont("ms gothic", 30))
        lbl1.setStyleSheet("background-color: rgba(240,240,240,255);border: none;border-radius: 8px;")
        lbl1.setGeometry ( (screenw/2)-(400/2)-420, 350, 400, 400)
        lbl1.setFocusPolicy(QtCore.Qt.NoFocus)
        lbl1.setCursor(Qt.PointingHandCursor)
        lbl1.clicked.connect(self.Q4click)
        lbl1.hide()

        lbl1 = choiceButton('Q4button_2', self)
        lbl1.setObjectName('Q4button_2')
        lbl1.setText("知っている")
        lbl1.DBname="知っている"
        lbl1.setFont(QtGui.QFont("ms gothic", 30))
        lbl1.setStyleSheet("background-color: rgba(240,240,240,255);border: none;border-radius: 8px;")
        lbl1.setGeometry ( (screenw/2)-(400/2), 350, 400, 400)
        lbl1.setFocusPolicy(QtCore.Qt.NoFocus)
        lbl1.setCursor(Qt.PointingHandCursor)
        lbl1.clicked.connect(self.Q4click)
        lbl1.hide()

        lbl1 = choiceButton('Q4button_3', self)
        lbl1.setObjectName('Q4button_3')
        lbl1.setText("知らなかった")
        lbl1.DBname="知らなかった"
        lbl1.setFont(QtGui.QFont("ms gothic", 30))
        lbl1.setStyleSheet("background-color: rgba(240,240,240,255);border: none;border-radius: 8px;")
        lbl1.setGeometry (  (screenw/2)-(400/2)+420, 350, 400, 400)
        lbl1.setFocusPolicy(QtCore.Qt.NoFocus)
        lbl1.setCursor(Qt.PointingHandCursor)
        lbl1.clicked.connect(self.Q4click)
        lbl1.hide()
        ##Q4 view
        ##Q5 view

        Q5wsize=600
        Q5hsize=130
        Q5top=250

        lbl1 = choiceButton('Q5button_1', self)
        lbl1.setObjectName('Q5button_1')
        lbl1.setText("個室の安心感")
        lbl1.DBname="個室の安心感"
        lbl1.setFont(QtGui.QFont("ms gothic", 30))
        lbl1.setStyleSheet("background-color: rgba(240,240,240,255);border: none;border-radius: 8px;")
        lbl1.setGeometry ( (screenw/2)-Q5wsize-10, Q5top, Q5wsize, Q5hsize)
        lbl1.setFocusPolicy(QtCore.Qt.NoFocus)
        lbl1.setCursor(Qt.PointingHandCursor)
        lbl1.clicked.connect(self.Q5click)
        lbl1.hide()

        Q5top+=(Q5hsize+20)
        lbl1 = choiceButton('Q5button_2', self)
        lbl1.setObjectName('Q5button_2')
        lbl1.setText("居心地の良さ")
        lbl1.DBname="居心地の良さ"
        lbl1.setFont(QtGui.QFont("ms gothic", 30))
        lbl1.setStyleSheet("background-color: rgba(240,240,240,255);border: none;border-radius: 8px;")
        lbl1.setGeometry ( (screenw/2)-Q5wsize-10, Q5top, Q5wsize, Q5hsize)
        lbl1.setFocusPolicy(QtCore.Qt.NoFocus)
        lbl1.setCursor(Qt.PointingHandCursor)
        lbl1.clicked.connect(self.Q5click)
        lbl1.hide()

        Q5top+=(Q5hsize+20)
        lbl1 = choiceButton('Q5button_3', self)
        lbl1.setObjectName('Q5button_3')
        lbl1.setText("情報が取得できる")
        lbl1.DBname="情報が取得できる"
        lbl1.setFont(QtGui.QFont("ms gothic", 30))
        lbl1.setStyleSheet("background-color: rgba(240,240,240,255);border: none;border-radius: 8px;")
        lbl1.setGeometry ( (screenw/2)-Q5wsize-10, Q5top, Q5wsize, Q5hsize)
        lbl1.setFocusPolicy(QtCore.Qt.NoFocus)
        lbl1.setCursor(Qt.PointingHandCursor)
        lbl1.clicked.connect(self.Q5click)
        lbl1.hide()

        Q5top+=(Q5hsize+20)
        lbl1 = choiceButton('Q5button_4', self)
        lbl1.setObjectName('Q5button_4')
        lbl1.setText("デザイン")
        lbl1.DBname="デザイン"
        lbl1.setFont(QtGui.QFont("ms gothic", 30))
        lbl1.setStyleSheet("background-color: rgba(240,240,240,255);border: none;border-radius: 8px;")
        lbl1.setGeometry ( (screenw/2)-Q5wsize-10, Q5top, Q5wsize, Q5hsize)
        lbl1.setFocusPolicy(QtCore.Qt.NoFocus)
        lbl1.setCursor(Qt.PointingHandCursor)
        lbl1.clicked.connect(self.Q5click)
        lbl1.hide()

        Q5top=250

        lbl1 = choiceButton('Q5button_5', self)
        lbl1.setObjectName('Q5button_5')
        lbl1.setText("座りやすさ")
        lbl1.DBname="座りやすさ"
        lbl1.setFont(QtGui.QFont("ms gothic", 30))
        lbl1.setStyleSheet("background-color: rgba(240,240,240,255);border: none;border-radius: 8px;")
        lbl1.setGeometry ( (screenw/2)+10, Q5top, Q5wsize, Q5hsize)
        lbl1.setFocusPolicy(QtCore.Qt.NoFocus)
        lbl1.setCursor(Qt.PointingHandCursor)
        lbl1.clicked.connect(self.Q5click)
        lbl1.hide()

        Q5top+=(Q5hsize+20)
        lbl1 = choiceButton('Q5button_6', self)
        lbl1.setObjectName('Q5button_6')
        lbl1.setText("広さ")
        lbl1.DBname="広さ"
        lbl1.setFont(QtGui.QFont("ms gothic", 30))
        lbl1.setStyleSheet("background-color: rgba(240,240,240,255);border: none;border-radius: 8px;")
        lbl1.setGeometry ( (screenw/2)+10, Q5top, Q5wsize, Q5hsize)
        lbl1.setFocusPolicy(QtCore.Qt.NoFocus)
        lbl1.setCursor(Qt.PointingHandCursor)
        lbl1.clicked.connect(self.Q5click)
        lbl1.hide()

        Q5top+=(Q5hsize+20)
        lbl1 = choiceButton('Q5button_7', self)
        lbl1.setObjectName('Q5button_7')
        lbl1.setText("設置場所")
        lbl1.DBname="設置場所"
        lbl1.setFont(QtGui.QFont("ms gothic", 30))
        lbl1.setStyleSheet("background-color: rgba(240,240,240,255);border: none;border-radius: 8px;")
        lbl1.setGeometry ( (screenw/2)+10, Q5top, Q5wsize, Q5hsize)
        lbl1.setFocusPolicy(QtCore.Qt.NoFocus)
        lbl1.setCursor(Qt.PointingHandCursor)
        lbl1.clicked.connect(self.Q5click)
        lbl1.hide()

        Q5top+=(Q5hsize+20)
        lbl1 = choiceButton('Q5button_8', self)
        lbl1.setObjectName('Q5button_8')
        lbl1.setText("その他")
        lbl1.DBname="その他"
        lbl1.setFont(QtGui.QFont("ms gothic", 30))
        lbl1.setStyleSheet("background-color: rgba(240,240,240,255);border: none;border-radius: 8px;")
        lbl1.setGeometry ( (screenw/2)+10, Q5top, Q5wsize, Q5hsize)
        lbl1.setFocusPolicy(QtCore.Qt.NoFocus)
        lbl1.setCursor(Qt.PointingHandCursor)
        lbl1.clicked.connect(self.Q5click)
        lbl1.hide()
        ##Q5 view
        ##Q6 view
        Q6wsize=800
        Q6hsize=130
        Q6top=250

        lbl1 = choiceButton('Q6button_1', self)
        lbl1.setObjectName('Q6button_1')
        lbl1.setText("大変満足している")
        lbl1.DBname="大変満足している"
        lbl1.setFont(QtGui.QFont("ms gothic", 30))
        lbl1.setStyleSheet("background-color: rgba(240,240,240,255);border: none;border-radius: 8px;")
        lbl1.setGeometry ( (screenw/2)-(Q6wsize/2), Q6top, Q6wsize, Q6hsize)
        lbl1.setFocusPolicy(QtCore.Qt.NoFocus)
        lbl1.setCursor(Qt.PointingHandCursor)
        lbl1.clicked.connect(self.Q6click)
        lbl1.hide()

        Q6top+=(Q6hsize+20)
        lbl1 = choiceButton('Q6button_2', self)
        lbl1.setObjectName('Q6button_2')
        lbl1.setText("満足している")
        lbl1.DBname="満足している"
        lbl1.setFont(QtGui.QFont("ms gothic", 30))
        lbl1.setStyleSheet("background-color: rgba(240,240,240,255);border: none;border-radius: 8px;")
        lbl1.setGeometry ( (screenw/2)-(Q6wsize/2), Q6top, Q6wsize, Q6hsize)
        lbl1.setFocusPolicy(QtCore.Qt.NoFocus)
        lbl1.setCursor(Qt.PointingHandCursor)
        lbl1.clicked.connect(self.Q6click)
        lbl1.hide()

        Q6top+=(Q6hsize+20)
        lbl1 = choiceButton('Q6button_3', self)
        lbl1.setObjectName('Q6button_3')
        lbl1.setText("普通")
        lbl1.DBname="普通"
        lbl1.setFont(QtGui.QFont("ms gothic", 30))
        lbl1.setStyleSheet("background-color: rgba(240,240,240,255);border: none;border-radius: 8px;")
        lbl1.setGeometry ( (screenw/2)-(Q6wsize/2), Q6top, Q6wsize, Q6hsize)
        lbl1.setFocusPolicy(QtCore.Qt.NoFocus)
        lbl1.setCursor(Qt.PointingHandCursor)
        lbl1.clicked.connect(self.Q6click)
        lbl1.hide()

        Q6top+=(Q6hsize+20)
        lbl1 = choiceButton('Q6button_4', self)
        lbl1.setObjectName('Q6button_4')
        lbl1.setText("あまり満足していない")
        lbl1.DBname="あまり満足していない"
        lbl1.setFont(QtGui.QFont("ms gothic", 30))
        lbl1.setStyleSheet("background-color: rgba(240,240,240,255);border: none;border-radius: 8px;")
        lbl1.setGeometry ( (screenw/2)-(Q6wsize/2), Q6top, Q6wsize, Q6hsize)
        lbl1.setFocusPolicy(QtCore.Qt.NoFocus)
        lbl1.setCursor(Qt.PointingHandCursor)
        lbl1.clicked.connect(self.Q6click)
        lbl1.hide()
        ##Q6 view
        ##thanks view
        thankstop=200
        thanksw=1000

        lbl1 = QtWidgets.QLabel('thanks1', self)
        lbl1.setObjectName('thanks1')
        lbl1.setText("ア ン ケ ー ト に ご 協 力 い た だ き")
        lbl1.setFont(QtGui.QFont("ms gothic", 30))
        lbl1.setAlignment(QtCore.Qt.AlignCenter)
        lbl1.setStyleSheet("color: rgba(255,255,255,255);")
        lbl1.setGeometry ( screenw/2-(thanksw/2), thankstop, thanksw, 130)
        lbl1.mousePressEvent=self.insertclick
        lbl1.hide()


        thankstop+=150
        lbl1 = QtWidgets.QLabel('thanks2', self)
        lbl1.setObjectName('thanks2')
        lbl1.setText("あ り が と う ご ざ い ま し た 。")
        lbl1.setFont(QtGui.QFont("ms gothic", 30))
        lbl1.setAlignment(QtCore.Qt.AlignCenter)
        lbl1.setStyleSheet("color: rgba(255,255,255,255);")
        lbl1.setGeometry ( screenw/2-(thanksw/2), thankstop, thanksw, 130)
        lbl1.mousePressEvent=self.insertclick
        lbl1.hide()

        thanksw=screenw-500
        thankstop+=150
        image_path=os.getcwd()+"/mamaro/style/img/QA/QAbabymap.png"
        image_profile = QtGui.QImage(image_path) #QImage object
        lbl1 = QtWidgets.QLabel('thanks3', self)
        lbl1.setObjectName('thanks3')
        lbl1.setPixmap(QtGui.QPixmap.fromImage(image_profile))
        lbl1.setScaledContents(True)
        lbl1.setCursor(Qt.PointingHandCursor)
        lbl1.setGeometry ( (screenw/2)-(thanksw/2), thankstop, thanksw, 450)
        lbl1.mousePressEvent=self.insertclick
        lbl1.hide()
        ##thanks view

        #
        # lbl1 = QtWidgets.QPushButton('content2', self)
        # lbl1.setObjectName('content2')
        # lbl1.setText("")
        # lbl1.setStyleSheet("background: 'white';")
        # lbl1.setGeometry ( 300, 300, 100, 100)
        # lbl1.setFocusPolicy(QtCore.Qt.NoFocus)
        # lbl1.clicked.connect(self.nextclick)
        #
        # lbl1 = QtWidgets.QPushButton('content4', self)
        # lbl1.setObjectName('content4')
        # lbl1.setText("")
        # lbl1.setStyleSheet("background: 'black';")
        # lbl1.setGeometry ( 600, 600, 100, 100)
        # lbl1.setFocusPolicy(QtCore.Qt.NoFocus)
        # lbl1.clicked.connect(self.nextclick)
        #
        # #lbl1.mousePressEvent=self.nextclick
        # #self.controllist.append(lbl1)
        #
        # lbl1 = QtWidgets.QLabel('content3', self)
        # lbl1.setObjectName('content3')
        # lbl1.setText("")
        # #lbl1.setStyleSheet("background: 'black';")
        # lbl1.setGeometry ( 400, 400, 150, 150)
        # #self.controllist.append(lbl1)
    def conentclick(self,event):
        if self.viewindex==7:
            #insert data to DB
            print("insert")
            for i in range(len(self.Q5choicelist)):
                if self.Q5choicelist[i]==1:
                    widget = self.findChild(QtWidgets.QPushButton, "Q5button_"+str(i+1))
                    self.Q5choice+=widget.DBname+","
            try:
                with self.connection.cursor() as cursor:
                    with self.connection.cursor() as cursor:
                        sql = "INSERT INTO `nursing_room_QA1` (`nursing_room_id`,`language`,`Q1_baby_year_month`,`Q1_parent`,`Q2_choice`,`Q3_choice`,`Q4_choice`,`Q5_choice`,`Q6_choice`,`insert_time`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,NOW())"
                        cursor.execute(sql, (self.roomid,self.dblanguage,self.dbbabyyearmonthlist[self.dbbabyyearmonth],self.dbparentlist[self.dbparent],self.Q2choice,self.Q3choice,self.Q4choice,self.Q5choice,self.Q6choice,))
                        self.connection.commit()
            except:
                print("QA1 insert data fail")
                pass
            finally:
                try:
                    self.connection.close()
                except:
                    pass

            os._exit(1)
    def insertclick(self,event):
        print("insert")
        for i in range(len(self.Q5choicelist)):
            if self.Q5choicelist[i]==1:
                widget = self.findChild(QtWidgets.QPushButton, "Q5button_"+str(i+1))
                self.Q5choice+=widget.DBname+","
        try:
            with self.connection.cursor() as cursor:
                with self.connection.cursor() as cursor:
                    sql = "INSERT INTO `nursing_room_QA1` (`nursing_room_id`,`language`,`Q1_baby_year_month`,`Q1_parent`,`Q2_choice`,`Q3_choice`,`Q4_choice`,`Q5_choice`,`Q6_choice`,`insert_time`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,NOW())"
                    cursor.execute(sql, (self.roomid,self.dblanguage,self.dbbabyyearmonthlist[self.dbbabyyearmonth],self.dbparentlist[self.dbparent],self.Q2choice,self.Q3choice,self.Q4choice,self.Q5choice,self.Q6choice,))
                    self.connection.commit()
        except:
            print("QA1 insert data fail")
            pass
        finally:
            try:
                self.connection.close()
            except:
                pass
        os._exit(1)

    def closeclick(self,event):
        if self.viewindex==7:
            for i in range(len(self.Q5choicelist)):
                if self.Q5choicelist[i]==1:
                    widget = self.findChild(QtWidgets.QPushButton, "Q5button_"+str(i+1))
                    self.Q5choice+=widget.DBname+","
            #insert data to DB
            print("insert")
            try:
                with self.connection.cursor() as cursor:
                    with self.connection.cursor() as cursor:
                        sql = "INSERT INTO `nursing_room_QA1` (`nursing_room_id`,`language`,`Q1_baby_year_month`,`Q1_parent`,`Q2_choice`,`Q3_choice`,`Q4_choice`,`Q5_choice`,`Q6_choice`,`insert_time`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,NOW())"
                        cursor.execute(sql, (self.roomid,self.dblanguage,self.dbbabyyearmonthlist[self.dbbabyyearmonth],self.dbparentlist[self.dbparent],self.Q2choice,self.Q3choice,self.Q4choice,self.Q5choice,self.Q6choice,))
                        self.connection.commit()
            except:
                print("QA1 insert data fail")
                pass
            finally:
                try:
                    self.connection.close()
                except:
                    pass
        os._exit(1)

        #self.setStyleSheet("QMainWindow {background: 'black';}");
    def style_choice2(self, text):
        self.dbparent=self.sender().currentIndex()
        print(text)


    def style_choice1(self, text):
        self.dbbabyyearmonth=self.sender().currentIndex()
        print(text)

    def style_choice(self, text):
        #change language

        self.dblanguage=text
        print(text)

        #######language
        # self.findChild(QtWidgets.QLabel, "toptext")
        # self.findChild(QtWidgets.QPushButton, "Q4button_1")
        # self.findChild(QtWidgets.QToolButton, "Q3button_1")
        # comboBox.addItem("日本語")
        # comboBox.addItem("English")
        # comboBox.addItem("繁體中文")
        # comboBox.addItem("简体中文")
        # comboBox.addItem("Vietnamese")

        # lbl1 = self.findChild(QtWidgets.QLabel, "toptext")
        # lbl1.setText("利用されるお子さまについて教えてください。")
        #
        # lbl1 = self.findChild(QtWidgets.QLabel, "toptext2")
        # lbl1.setText("利用されるお子さまについて教えてください。")
        #
        # lbl1 = self.findChild(QtWidgets.QLabel, "toptext3")
        # lbl1.setText("利用されるお子さまについて教えてください。")
        if text=="日本語":
            lbl1 = self.findChild(QtWidgets.QPushButton, "nextbutton")
            lbl1.setText("次へ")
            lbl1 = self.findChild(QtWidgets.QPushButton, "backbutton")
            lbl1.setText("戻る")
            lbl1 = self.findChild(QtWidgets.QLabel, "lan2")
            lbl1.setText("言語 (language)")


            lbl1 = self.findChild(QtWidgets.QLabel, "Q1_2")
            lbl1.setText("お子さまのご年齢は")
            comboBox = self.findChild(QtWidgets.QComboBox, "Q1_3")
            comboBox.clear()
            comboBox.addItem("0 歳 0 〜 3 ヶ月")
            comboBox.addItem("0 歳 3 〜 6 ヶ月")
            comboBox.addItem("0 歳 6 〜 9 ヶ月")
            comboBox.addItem("0 歳 9 〜 12 ヶ月")
            comboBox.addItem("1 歳 0 〜 3 ヶ月")
            comboBox.addItem("1 歳 3 〜 6 ヶ月")
            comboBox.addItem("1 歳 6 〜 9 ヶ月")
            comboBox.addItem("1 歳 9 〜 12 ヶ月")
            comboBox.addItem("2 歳 以上")
            lbl1 = self.findChild(QtWidgets.QLabel, "Q1_5")
            lbl1.setText("お子さまとの関係")
            comboBox = self.findChild(QtWidgets.QComboBox, "Q1_6")
            comboBox.clear()
            comboBox.addItem("ママ")
            comboBox.addItem("パパ")
            comboBox.addItem("その他")
            lbl1 = self.findChild(QtWidgets.QPushButton, "Q2button_1")
            lbl1.setText("はじめて")
            lbl1 = self.findChild(QtWidgets.QPushButton, "Q2button_2")
            lbl1.setText("2 ～ 9回")
            lbl1 = self.findChild(QtWidgets.QPushButton, "Q2button_3")
            lbl1.setText("10回以上")
            lbl1 = self.findChild(QtWidgets.QToolButton, "Q3button_1")
            lbl1.setText("施設の案内")
            lbl1 = self.findChild(QtWidgets.QToolButton, "Q3button_2")
            lbl1.setText("通りがかりに")
            lbl1 = self.findChild(QtWidgets.QToolButton, "Q3button_3")
            lbl1.setText("Babymap")
            lbl1 = self.findChild(QtWidgets.QToolButton, "Q3button_4")
            lbl1.setText("知人から")
            lbl1 = self.findChild(QtWidgets.QToolButton, "Q3button_5")
            lbl1.setText("ネットニュース")
            lbl1 = self.findChild(QtWidgets.QToolButton, "Q3button_6")
            lbl1.setText("その他")
            lbl1 = self.findChild(QtWidgets.QPushButton, "Q4button_1")
            lbl1.setText("利用している")
            lbl1 = self.findChild(QtWidgets.QPushButton, "Q4button_2")
            lbl1.setText("知っている")
            lbl1 = self.findChild(QtWidgets.QPushButton, "Q4button_3")
            lbl1.setText("知らなかった")
            lbl1 = self.findChild(QtWidgets.QPushButton, "Q5button_1")
            lbl1.setText("個室の安心感")
            lbl1 = self.findChild(QtWidgets.QPushButton, "Q5button_2")
            lbl1.setText("居心地の良さ")
            lbl1 = self.findChild(QtWidgets.QPushButton, "Q5button_3")
            lbl1.setText("情報が取得できる")
            lbl1 = self.findChild(QtWidgets.QPushButton, "Q5button_4")
            lbl1.setText("デザイン")
            lbl1 = self.findChild(QtWidgets.QPushButton, "Q5button_5")
            lbl1.setText("座りやすさ")
            lbl1 = self.findChild(QtWidgets.QPushButton, "Q5button_6")
            lbl1.setText("広さ")
            lbl1 = self.findChild(QtWidgets.QPushButton, "Q5button_7")
            lbl1.setText("設置場所")
            lbl1 = self.findChild(QtWidgets.QPushButton, "Q5button_8")
            lbl1.setText("その他")
            lbl1 = self.findChild(QtWidgets.QPushButton, "Q6button_1")
            lbl1.setText("大変満足している")
            lbl1 = self.findChild(QtWidgets.QPushButton, "Q6button_2")
            lbl1.setText("満足している")
            lbl1 = self.findChild(QtWidgets.QPushButton, "Q6button_3")
            lbl1.setText("普通")
            lbl1 = self.findChild(QtWidgets.QPushButton, "Q6button_4")
            lbl1.setText("あまり満足していない")

            lbl1 = self.findChild(QtWidgets.QLabel, "thanks1")
            lbl1.setText("ア ン ケ ー ト に ご 協 力 い た だ き")
            lbl1 = self.findChild(QtWidgets.QLabel, "thanks2")
            lbl1.setText("あ り が と う ご ざ い ま し た 。")
        elif text=="English":
            lbl1 = self.findChild(QtWidgets.QPushButton, "nextbutton")
            lbl1.setText("Next")
            lbl1 = self.findChild(QtWidgets.QPushButton, "backbutton")
            lbl1.setText("Back")
            lbl1 = self.findChild(QtWidgets.QLabel, "lan2")
            lbl1.setText("Language")

            lbl1 = self.findChild(QtWidgets.QLabel, "Q1_2")
            lbl1.setText("How old is your child?")
            comboBox = self.findChild(QtWidgets.QComboBox, "Q1_3")
            comboBox.clear()
            comboBox.addItem("0 〜 3 months")
            comboBox.addItem("3 〜 6 months")
            comboBox.addItem("6 〜 9 months")
            comboBox.addItem("9 〜 12 months")
            comboBox.addItem("12 〜 15 months")
            comboBox.addItem("15 〜 18 months")
            comboBox.addItem("18 〜 21 months")
            comboBox.addItem("21 〜 24 months")
            comboBox.addItem("Over 2 years")
            lbl1 = self.findChild(QtWidgets.QLabel, "Q1_5")
            lbl1.setText("Relationship with child")
            comboBox = self.findChild(QtWidgets.QComboBox, "Q1_6")
            comboBox.clear()
            comboBox.addItem("Mother")
            comboBox.addItem("Father")
            comboBox.addItem("Other")
            lbl1 = self.findChild(QtWidgets.QPushButton, "Q2button_1")
            lbl1.setText("1st Time")
            lbl1 = self.findChild(QtWidgets.QPushButton, "Q2button_2")
            lbl1.setText("2nd - 9th Time")
            lbl1 = self.findChild(QtWidgets.QPushButton, "Q2button_3")
            lbl1.setText("10th Time or More")
            lbl1 = self.findChild(QtWidgets.QToolButton, "Q3button_1")
            lbl1.setText("Facility Information")
            lbl1 = self.findChild(QtWidgets.QToolButton, "Q3button_2")
            lbl1.setText("Word of Mouth")
            lbl1 = self.findChild(QtWidgets.QToolButton, "Q3button_3")
            lbl1.setText("Babymap")
            lbl1 = self.findChild(QtWidgets.QToolButton, "Q3button_4")
            lbl1.setText("From Acquaintance")
            lbl1 = self.findChild(QtWidgets.QToolButton, "Q3button_5")
            lbl1.setText("Internet News")
            lbl1 = self.findChild(QtWidgets.QToolButton, "Q3button_6")
            lbl1.setText("Other")
            lbl1 = self.findChild(QtWidgets.QPushButton, "Q4button_1")
            lbl1.setText("Currently Using")
            lbl1 = self.findChild(QtWidgets.QPushButton, "Q4button_2")
            lbl1.setText("Yes")
            lbl1 = self.findChild(QtWidgets.QPushButton, "Q4button_3")
            lbl1.setText("No")
            lbl1 = self.findChild(QtWidgets.QPushButton, "Q5button_1")
            lbl1.setText("Privacy")
            lbl1 = self.findChild(QtWidgets.QPushButton, "Q5button_2")
            lbl1.setText("Coziness")
            lbl1 = self.findChild(QtWidgets.QPushButton, "Q5button_3")
            lbl1.setText("Available Information")
            lbl1 = self.findChild(QtWidgets.QPushButton, "Q5button_4")
            lbl1.setText("Design")
            lbl1 = self.findChild(QtWidgets.QPushButton, "Q5button_5")
            lbl1.setText("Comfortable Chair")
            lbl1 = self.findChild(QtWidgets.QPushButton, "Q5button_6")
            lbl1.setText("Spacious")
            lbl1 = self.findChild(QtWidgets.QPushButton, "Q5button_7")
            lbl1.setText("Location ")
            lbl1 = self.findChild(QtWidgets.QPushButton, "Q5button_8")
            lbl1.setText("Other")
            lbl1 = self.findChild(QtWidgets.QPushButton, "Q6button_1")
            lbl1.setText("Very Satisfied")
            lbl1 = self.findChild(QtWidgets.QPushButton, "Q6button_2")
            lbl1.setText("Satisfied")
            lbl1 = self.findChild(QtWidgets.QPushButton, "Q6button_3")
            lbl1.setText("Somewhat Satisfied")
            lbl1 = self.findChild(QtWidgets.QPushButton, "Q6button_4")
            lbl1.setText("Not Satisfied")

            lbl1 = self.findChild(QtWidgets.QLabel, "thanks1")
            lbl1.setText("Please answer this survey")
            lbl1 = self.findChild(QtWidgets.QLabel, "thanks2")
            lbl1.setText("Thank you very much")
        elif text=="繁體中文":
            lbl1 = self.findChild(QtWidgets.QPushButton, "nextbutton")
            lbl1.setText("下一個")
            lbl1 = self.findChild(QtWidgets.QPushButton, "backbutton")
            lbl1.setText("返回")
            lbl1 = self.findChild(QtWidgets.QLabel, "lan2")
            lbl1.setText("語言 (language)")

            lbl1 = self.findChild(QtWidgets.QLabel, "Q1_2")
            lbl1.setText("您的孩子年齡是")
            comboBox = self.findChild(QtWidgets.QComboBox, "Q1_3")
            comboBox.clear()
            comboBox.addItem("0 歲 0 〜 3 個月")
            comboBox.addItem("0 歲 3 〜 6 個月")
            comboBox.addItem("0 歲 6 〜 9 個月")
            comboBox.addItem("0 歲 9 〜 12 個月")
            comboBox.addItem("1 歲 0 〜 3 個月")
            comboBox.addItem("1 歲 3 〜 6 個月")
            comboBox.addItem("1 歲 6 〜 9 個月")
            comboBox.addItem("1 歲 9 〜 12 個月")
            comboBox.addItem("2 歲 以上")
            lbl1 = self.findChild(QtWidgets.QLabel, "Q1_5")
            lbl1.setText("您和孩子的關係")
            comboBox = self.findChild(QtWidgets.QComboBox, "Q1_6")
            comboBox.clear()
            comboBox.addItem("媽媽")
            comboBox.addItem("爸爸")
            comboBox.addItem("其他")
            lbl1 = self.findChild(QtWidgets.QPushButton, "Q2button_1")
            lbl1.setText("初次")
            lbl1 = self.findChild(QtWidgets.QPushButton, "Q2button_2")
            lbl1.setText("2 ～ 9次")
            lbl1 = self.findChild(QtWidgets.QPushButton, "Q2button_3")
            lbl1.setText("10次以上")
            lbl1 = self.findChild(QtWidgets.QToolButton, "Q3button_1")
            lbl1.setText("設施的向導")
            lbl1 = self.findChild(QtWidgets.QToolButton, "Q3button_2")
            lbl1.setText("在街上")
            lbl1 = self.findChild(QtWidgets.QToolButton, "Q3button_3")
            lbl1.setText("Babymap")
            lbl1 = self.findChild(QtWidgets.QToolButton, "Q3button_4")
            lbl1.setText("從熟人")
            lbl1 = self.findChild(QtWidgets.QToolButton, "Q3button_5")
            lbl1.setText("網路新聞")
            lbl1 = self.findChild(QtWidgets.QToolButton, "Q3button_6")
            lbl1.setText("其他")
            lbl1 = self.findChild(QtWidgets.QPushButton, "Q4button_1")
            lbl1.setText("正在使用")
            lbl1 = self.findChild(QtWidgets.QPushButton, "Q4button_2")
            lbl1.setText("知道")
            lbl1 = self.findChild(QtWidgets.QPushButton, "Q4button_3")
            lbl1.setText("不知道")
            lbl1 = self.findChild(QtWidgets.QPushButton, "Q5button_1")
            lbl1.setText("房間的安全感")
            lbl1 = self.findChild(QtWidgets.QPushButton, "Q5button_2")
            lbl1.setText("舒適感")
            lbl1 = self.findChild(QtWidgets.QPushButton, "Q5button_3")
            lbl1.setText("能取得訊息")
            lbl1 = self.findChild(QtWidgets.QPushButton, "Q5button_4")
            lbl1.setText("設計感")
            lbl1 = self.findChild(QtWidgets.QPushButton, "Q5button_5")
            lbl1.setText("座椅舒適")
            lbl1 = self.findChild(QtWidgets.QPushButton, "Q5button_6")
            lbl1.setText("寬敞")
            lbl1 = self.findChild(QtWidgets.QPushButton, "Q5button_7")
            lbl1.setText("設置的地點")
            lbl1 = self.findChild(QtWidgets.QPushButton, "Q5button_8")
            lbl1.setText("其他")
            lbl1 = self.findChild(QtWidgets.QPushButton, "Q6button_1")
            lbl1.setText("非常滿意")
            lbl1 = self.findChild(QtWidgets.QPushButton, "Q6button_2")
            lbl1.setText("滿意")
            lbl1 = self.findChild(QtWidgets.QPushButton, "Q6button_3")
            lbl1.setText("普通")
            lbl1 = self.findChild(QtWidgets.QPushButton, "Q6button_4")
            lbl1.setText("不是很滿意")

            lbl1 = self.findChild(QtWidgets.QLabel, "thanks1")
            lbl1.setText("謝 謝 協 助")
            lbl1 = self.findChild(QtWidgets.QLabel, "thanks2")
            lbl1.setText("填 寫 問 卷")
        elif text=="简体中文":
            lbl1 = self.findChild(QtWidgets.QPushButton, "nextbutton")
            lbl1.setText("下一个")
            lbl1 = self.findChild(QtWidgets.QPushButton, "backbutton")
            lbl1.setText("返回")
            lbl1 = self.findChild(QtWidgets.QLabel, "lan2")
            lbl1.setText("语言 (language)")


            lbl1 = self.findChild(QtWidgets.QLabel, "Q1_2")
            lbl1.setText("您的孩子年龄是")
            comboBox = self.findChild(QtWidgets.QComboBox, "Q1_3")
            comboBox.clear()
            comboBox.addItem("0 岁 0 〜 3 个月")
            comboBox.addItem("0 岁 3 〜 6 个月")
            comboBox.addItem("0 岁 6 〜 9 个月")
            comboBox.addItem("0 岁 9 〜 12 个月")
            comboBox.addItem("1 岁 0 〜 3 个月")
            comboBox.addItem("1 岁 3 〜 6 个月")
            comboBox.addItem("1 岁 6 〜 9 个月")
            comboBox.addItem("1 岁 9 〜 12 个月")
            comboBox.addItem("2 岁 以上")
            lbl1 = self.findChild(QtWidgets.QLabel, "Q1_5")
            lbl1.setText("您和孩子的关系")
            comboBox = self.findChild(QtWidgets.QComboBox, "Q1_6")
            comboBox.clear()
            comboBox.addItem("妈妈")
            comboBox.addItem("爸爸")
            comboBox.addItem("其他")
            lbl1 = self.findChild(QtWidgets.QPushButton, "Q2button_1")
            lbl1.setText("初次")
            lbl1 = self.findChild(QtWidgets.QPushButton, "Q2button_2")
            lbl1.setText("2 ～ 9次")
            lbl1 = self.findChild(QtWidgets.QPushButton, "Q2button_3")
            lbl1.setText("10次​​以上")
            lbl1 = self.findChild(QtWidgets.QToolButton, "Q3button_1")
            lbl1.setText("设施的向导")
            lbl1 = self.findChild(QtWidgets.QToolButton, "Q3button_2")
            lbl1.setText("在街上")
            lbl1 = self.findChild(QtWidgets.QToolButton, "Q3button_3")
            lbl1.setText("Babymap")
            lbl1 = self.findChild(QtWidgets.QToolButton, "Q3button_4")
            lbl1.setText("从熟人")
            lbl1 = self.findChild(QtWidgets.QToolButton, "Q3button_5")
            lbl1.setText("网上新闻")
            lbl1 = self.findChild(QtWidgets.QToolButton, "Q3button_6")
            lbl1.setText("其他")
            lbl1 = self.findChild(QtWidgets.QPushButton, "Q4button_1")
            lbl1.setText("正在使用")
            lbl1 = self.findChild(QtWidgets.QPushButton, "Q4button_2")
            lbl1.setText("知道")
            lbl1 = self.findChild(QtWidgets.QPushButton, "Q4button_3")
            lbl1.setText("不知道")
            lbl1 = self.findChild(QtWidgets.QPushButton, "Q5button_1")
            lbl1.setText("房间的安全感")
            lbl1 = self.findChild(QtWidgets.QPushButton, "Q5button_2")
            lbl1.setText("舒适感")
            lbl1 = self.findChild(QtWidgets.QPushButton, "Q5button_3")
            lbl1.setText("能取得讯息")
            lbl1 = self.findChild(QtWidgets.QPushButton, "Q5button_4")
            lbl1.setText("设计感")
            lbl1 = self.findChild(QtWidgets.QPushButton, "Q5button_5")
            lbl1.setText("座椅舒适")
            lbl1 = self.findChild(QtWidgets.QPushButton, "Q5button_6")
            lbl1.setText("宽敞")
            lbl1 = self.findChild(QtWidgets.QPushButton, "Q5button_7")
            lbl1.setText("设置的地点")
            lbl1 = self.findChild(QtWidgets.QPushButton, "Q5button_8")
            lbl1.setText("其他")
            lbl1 = self.findChild(QtWidgets.QPushButton, "Q6button_1")
            lbl1.setText("非常满意")
            lbl1 = self.findChild(QtWidgets.QPushButton, "Q6button_2")
            lbl1.setText("满意")
            lbl1 = self.findChild(QtWidgets.QPushButton, "Q6button_3")
            lbl1.setText("普通")
            lbl1 = self.findChild(QtWidgets.QPushButton, "Q6button_4")
            lbl1.setText("不是很满意")

            lbl1 = self.findChild(QtWidgets.QLabel, "thanks1")
            lbl1.setText("谢 谢 协 助")
            lbl1 = self.findChild(QtWidgets.QLabel, "thanks2")
            lbl1.setText("填 写 问 卷")
        elif text=="Vietnamese":
            lbl1 = self.findChild(QtWidgets.QPushButton, "nextbutton")
            lbl1.setText("Tiếp theo")
            lbl1 = self.findChild(QtWidgets.QPushButton, "backbutton")
            lbl1.setText("Trở lại")
            lbl1 = self.findChild(QtWidgets.QLabel, "lan2")
            lbl1.setText("Ngôn ngữ")


            lbl1 = self.findChild(QtWidgets.QLabel, "Q1_2")
            lbl1.setText("Tuổi của con bạn là")
            comboBox = self.findChild(QtWidgets.QComboBox, "Q1_3")
            comboBox.clear()
            comboBox.addItem("0 tuổi 0 〜 3 tháng")
            comboBox.addItem("0 tuổi 3 〜 6 tháng")
            comboBox.addItem("0 tuổi 6 〜 9 tháng")
            comboBox.addItem("0 tuổi 9 〜 12 tháng")
            comboBox.addItem("1 tuổi 0 〜 3 tháng")
            comboBox.addItem("1 tuổi 3 〜 6 tháng")
            comboBox.addItem("1 tuổi 6 〜 9 tháng")
            comboBox.addItem("1 tuổi 9 〜 12 tháng")
            comboBox.addItem("2 năm trở lên")
            lbl1 = self.findChild(QtWidgets.QLabel, "Q1_5")
            lbl1.setText("Bạn là bố hay mẹ")
            comboBox = self.findChild(QtWidgets.QComboBox, "Q1_6")
            comboBox.clear()
            comboBox.addItem("Mẹ")
            comboBox.addItem("Bố")
            comboBox.addItem("khác")
            lbl1 = self.findChild(QtWidgets.QPushButton, "Q2button_1")
            lbl1.setText("Lần đầu tiên")
            lbl1 = self.findChild(QtWidgets.QPushButton, "Q2button_2")
            lbl1.setText("Dưới 10 lần")
            lbl1 = self.findChild(QtWidgets.QPushButton, "Q2button_3")
            lbl1.setText("Trên 10 lần")
            lbl1 = self.findChild(QtWidgets.QToolButton, "Q3button_1")
            lbl1.setText("Bảng chỉ dẫn")
            lbl1 = self.findChild(QtWidgets.QToolButton, "Q3button_2")
            lbl1.setText("Tình cờ thấy")
            lbl1 = self.findChild(QtWidgets.QToolButton, "Q3button_3")
            lbl1.setText("Babymap")
            lbl1 = self.findChild(QtWidgets.QToolButton, "Q3button_4")
            lbl1.setText("Từ người quen")
            lbl1 = self.findChild(QtWidgets.QToolButton, "Q3button_5")
            lbl1.setText("Từ internet")
            lbl1 = self.findChild(QtWidgets.QToolButton, "Q3button_6")
            lbl1.setText("Khác")
            lbl1 = self.findChild(QtWidgets.QPushButton, "Q4button_1")
            lbl1.setText("Tôi đã dùng")
            lbl1 = self.findChild(QtWidgets.QPushButton, "Q4button_2")
            lbl1.setText("Tôi biết")
            lbl1 = self.findChild(QtWidgets.QPushButton, "Q4button_3")
            lbl1.setText("Tôi không biết.")
            lbl1 = self.findChild(QtWidgets.QPushButton, "Q5button_1")
            lbl1.setText("Sự riêng tư")
            lbl1 = self.findChild(QtWidgets.QPushButton, "Q5button_2")
            lbl1.setText("Sự ấm cúng, thoải mái")
            lbl1 = self.findChild(QtWidgets.QPushButton, "Q5button_3")
            lbl1.setText("Có thể xem thông tin")
            lbl1 = self.findChild(QtWidgets.QPushButton, "Q5button_4")
            lbl1.setText("Thiết kế")
            lbl1 = self.findChild(QtWidgets.QPushButton, "Q5button_5")
            lbl1.setText("Ngồi thoải mái")
            lbl1 = self.findChild(QtWidgets.QPushButton, "Q5button_6")
            lbl1.setText("Kích thước hợp lý")
            lbl1 = self.findChild(QtWidgets.QPushButton, "Q5button_7")
            lbl1.setText("Vị trí lắp đặt thuận tiện")
            lbl1 = self.findChild(QtWidgets.QPushButton, "Q5button_8")
            lbl1.setText("Khác")
            lbl1 = self.findChild(QtWidgets.QPushButton, "Q6button_1")
            lbl1.setText("Tôi rất hài lòng.")
            lbl1 = self.findChild(QtWidgets.QPushButton, "Q6button_2")
            lbl1.setText("Tôi hài lòng.")
            lbl1 = self.findChild(QtWidgets.QPushButton, "Q6button_3")
            lbl1.setText("Bình thường.")
            lbl1 = self.findChild(QtWidgets.QPushButton, "Q6button_4")
            lbl1.setText("Tôi không hài lòng.")

            lbl1 = self.findChild(QtWidgets.QLabel, "thanks1")
            lbl1.setText("Hãy cùng chúng tôi làm mamaro trở lên tốt hơn nữa.")
            lbl1 = self.findChild(QtWidgets.QLabel, "thanks2")
            lbl1.setText("Cảm ơn bạn rất nhiều.")
        #######language


        #QtGui.QApplication.setStyle(QtGui.QStyleFactory.create(text))
    def Q6click(self):
        print("Q6 to end")
        # print(self.sender().objectName())
        # print(self.sender().text())
        self.Q6choice=self.sender().DBname
        self.viewindex+=1
        widget = self.findChild(QtWidgets.QLabel, "toptext")
        widget.hide()

        widget = self.findChild(QtWidgets.QLabel, "toptext1")
        widget.hide()

        #Q6 view
        widget = self.findChild(QtWidgets.QPushButton, "Q6button_1")
        widget.hide()
        widget = self.findChild(QtWidgets.QPushButton, "Q6button_2")
        widget.hide()
        widget = self.findChild(QtWidgets.QPushButton, "Q6button_3")
        widget.hide()
        widget = self.findChild(QtWidgets.QPushButton, "Q6button_4")
        widget.hide()

        #back buttonbackbutton
        widget = self.findChild(QtWidgets.QPushButton, "backbutton")
        widget.hide()
        #top view hide
        widget = self.findChild(QtWidgets.QLabel, "toppan")
        widget.hide()

        widget = self.findChild(QtWidgets.QLabel, "content1")
        widget.setStyleSheet("background: #6AD5AC;")

        widget = self.findChild(QtWidgets.QLabel, "thanks1")
        widget.show()
        widget = self.findChild(QtWidgets.QLabel, "thanks2")
        widget.show()
        widget = self.findChild(QtWidgets.QLabel, "thanks3")
        widget.show()





    def Q5click(self):
        print("Q5 to Q6")
        # print(self.sender().objectName())
        # print(self.sender().text())
        #self.Q4choice=self.sender().text()
        print(self.sender().objectName().rfind('_'))
        strindex=self.sender().objectName()[self.sender().objectName().rfind('_')+1:]
        print(strindex)
        if self.Q5choicelist[int(strindex)-1]==1:
            self.Q5choicelist[int(strindex)-1]=0
            self.sender().checkclick=True
        else:
            self.Q5choicelist[int(strindex)-1]=1
            self.sender().checkclick=False
            self.sender().setStyleSheet("background-color: rgba(135,222,188,255);border: none;border-radius: 8px;")


        print(self.Q5choicelist)

        #self.viewindex+=1

    def Q4click(self):
        print("Q4 to Q5")
        # print(self.sender().objectName())
        # print(self.sender().text())
        self.Q4choice=self.sender().DBname
        self.viewindex+=1
        widget = self.findChild(QtWidgets.QLabel, "toptext2")
        widget.show()
        widget = self.findChild(QtWidgets.QLabel, "toptext3")
        widget.show()
        if self.dblanguage=="日本語":
            widget = self.findChild(QtWidgets.QLabel, "toptext2")
            widget.setText("mamaroで" + '"' + "気に入っているポイント" + '"')
            widget = self.findChild(QtWidgets.QLabel, "toptext3")
            widget.setText("を教えてください。（複数選択可）")
        elif self.dblanguage=="English":
            widget = self.findChild(QtWidgets.QLabel, "toptext2")
            widget.setText("Please let us know what you liked about mamaro")
            widget = self.findChild(QtWidgets.QLabel, "toptext3")
            widget.setText("(Multiple Selections possible)")
        elif self.dblanguage=="繁體中文":
            widget = self.findChild(QtWidgets.QLabel, "toptext2")
            widget.setText("請告訴我們您喜歡mamaro")
            widget = self.findChild(QtWidgets.QLabel, "toptext3")
            widget.setText("的哪些部分？（複數選擇）")
        elif self.dblanguage=="简体中文":
            widget = self.findChild(QtWidgets.QLabel, "toptext2")
            widget.setText("请告诉我们您喜欢mamaro")
            widget = self.findChild(QtWidgets.QLabel, "toptext3")
            widget.setText("的哪些部分？（复数选择）")
        elif self.dblanguage=="Vietnamese":
            widget = self.findChild(QtWidgets.QLabel, "toptext2")
            widget.setText("Điểm bạn thích ở mamaro.")
            widget = self.findChild(QtWidgets.QLabel, "toptext3")
            widget.setText("(có thể chọn nhiều câu trả lời)")


        widget = self.findChild(QtWidgets.QLabel, "toptext1")
        widget.setText("Q  4 / 5")

        #Q4 view
        widget = self.findChild(QtWidgets.QPushButton, "Q4button_1")
        widget.hide()
        widget = self.findChild(QtWidgets.QPushButton, "Q4button_2")
        widget.hide()
        widget = self.findChild(QtWidgets.QPushButton, "Q4button_3")
        widget.hide()

        #Q5 view
        widget = self.findChild(QtWidgets.QPushButton, "Q5button_1")
        widget.show()
        widget = self.findChild(QtWidgets.QPushButton, "Q5button_2")
        widget.show()
        widget = self.findChild(QtWidgets.QPushButton, "Q5button_3")
        widget.show()
        widget = self.findChild(QtWidgets.QPushButton, "Q5button_4")
        widget.show()
        widget = self.findChild(QtWidgets.QPushButton, "Q5button_5")
        widget.show()
        widget = self.findChild(QtWidgets.QPushButton, "Q5button_6")
        widget.show()
        widget = self.findChild(QtWidgets.QPushButton, "Q5button_7")
        widget.show()
        widget = self.findChild(QtWidgets.QPushButton, "Q5button_8")
        widget.show()

        #next button
        widget = self.findChild(QtWidgets.QPushButton, "nextbutton")
        widget.show()

    def Q3click(self):
        print("Q3 to Q4")
        # print(self.sender().objectName())
        # print(self.sender().text())
        self.Q3choice=self.sender().DBname
        self.viewindex+=1

        widget = self.findChild(QtWidgets.QLabel, "toptext")
        widget.hide()

        widget = self.findChild(QtWidgets.QLabel, "toptext2")
        widget.show()
        widget = self.findChild(QtWidgets.QLabel, "toptext3")
        widget.show()

        if self.dblanguage=="日本語":
            widget = self.findChild(QtWidgets.QLabel, "toptext2")
            widget.setText("mamaroの空室状況をBabymapというアプリで")
            widget = self.findChild(QtWidgets.QLabel, "toptext3")
            widget.setText("調べることができるのを知っていましたか？")
        elif self.dblanguage=="English":
            widget = self.findChild(QtWidgets.QLabel, "toptext2")
            widget.setText("Did you know that you can check the availability")
            widget = self.findChild(QtWidgets.QLabel, "toptext3")
            widget.setText("of mamaro on an application called Babymap?")
        elif self.dblanguage=="繁體中文":
            widget = self.findChild(QtWidgets.QLabel, "toptext2")
            widget.setText("您知道從Babymap可以")
            widget = self.findChild(QtWidgets.QLabel, "toptext3")
            widget.setText("得知mamaro的使用狀況嗎？")
        elif self.dblanguage=="简体中文":
            widget = self.findChild(QtWidgets.QLabel, "toptext2")
            widget.setText("您知道从Babymap可以")
            widget = self.findChild(QtWidgets.QLabel, "toptext3")
            widget.setText("得知mamaro的使用状况吗？")
        elif self.dblanguage=="Vietnamese":
            widget = self.findChild(QtWidgets.QLabel, "toptext2")
            widget.setText("Bạn có biết rằng bạn có thể kiểm tra mamaro")
            widget = self.findChild(QtWidgets.QLabel, "toptext3")
            widget.setText("có người dùng hay không trong Babymap?")

        widget = self.findChild(QtWidgets.QLabel, "toptext1")
        widget.setText("Q  3 / 5")

        #Q3 view
        widget = self.findChild(QtWidgets.QToolButton, "Q3button_1")
        widget.hide()
        widget = self.findChild(QtWidgets.QToolButton, "Q3button_2")
        widget.hide()
        widget = self.findChild(QtWidgets.QToolButton, "Q3button_3")
        widget.hide()
        widget = self.findChild(QtWidgets.QToolButton, "Q3button_4")
        widget.hide()
        widget = self.findChild(QtWidgets.QToolButton, "Q3button_5")
        widget.hide()
        widget = self.findChild(QtWidgets.QToolButton, "Q3button_6")
        widget.hide()

        #Q4 view
        widget = self.findChild(QtWidgets.QPushButton, "Q4button_1")
        widget.show()
        widget = self.findChild(QtWidgets.QPushButton, "Q4button_2")
        widget.show()
        widget = self.findChild(QtWidgets.QPushButton, "Q4button_3")
        widget.show()



    def Q2click(self):
        print("Q2 to Q3")
        # print(self.sender().objectName())
        # print(self.sender().text())
        self.Q2choice=self.sender().DBname
        self.viewindex+=1

        widget = self.findChild(QtWidgets.QLabel, "toptext1")
        widget.setText("Q  2 / 5")

        if self.dblanguage=="日本語":
            widget = self.findChild(QtWidgets.QLabel, "toptext")
            widget.setText("mamaroをどのようにして知りましたか？")
        elif self.dblanguage=="English":
            widget = self.findChild(QtWidgets.QLabel, "toptext")
            widget.setText("How did you hear about mamaro?")
        elif self.dblanguage=="繁體中文":
            widget = self.findChild(QtWidgets.QLabel, "toptext")
            widget.setText("您是怎麼知道mamaro的？")
        elif self.dblanguage=="简体中文":
            widget = self.findChild(QtWidgets.QLabel, "toptext")
            widget.setText("您是怎么知道mamaro的？")
        elif self.dblanguage=="Vietnamese":
            widget = self.findChild(QtWidgets.QLabel, "toptext")
            widget.setText("Bạn biết về mamaro từ đâu?")

        #Q2 view
        widget = self.findChild(QtWidgets.QPushButton, "Q2button_1")
        widget.hide()
        widget = self.findChild(QtWidgets.QPushButton, "Q2button_2")
        widget.hide()
        widget = self.findChild(QtWidgets.QPushButton, "Q2button_3")
        widget.hide()

        #Q3 view
        widget = self.findChild(QtWidgets.QToolButton, "Q3button_1")
        widget.show()
        widget = self.findChild(QtWidgets.QToolButton, "Q3button_2")
        widget.show()
        widget = self.findChild(QtWidgets.QToolButton, "Q3button_3")
        widget.show()
        widget = self.findChild(QtWidgets.QToolButton, "Q3button_4")
        widget.show()
        widget = self.findChild(QtWidgets.QToolButton, "Q3button_5")
        widget.show()
        widget = self.findChild(QtWidgets.QToolButton, "Q3button_6")
        widget.show()

    def backclick(self):
        # print(self.sender().objectName())
        # print(self.sender().text())
        self.viewindex-=1
        if self.viewindex==0:
            print("Q1 to language")
            widget = self.findChild(QtWidgets.QLabel, "close")
            widget.show()
            widget = self.findChild(QtWidgets.QLabel, "lan1")
            widget.show()
            widget = self.findChild(QtWidgets.QLabel, "lan2")
            widget.show()
            widget = self.findChild(QtWidgets.QComboBox, "lan3")
            widget.show()

            #back buttonbackbutton
            widget = self.findChild(QtWidgets.QPushButton, "backbutton")
            widget.hide()
            #Q1 view show
            widget = self.findChild(QtWidgets.QLabel, "toppan")
            widget.hide()
            widget = self.findChild(QtWidgets.QLabel, "toptext")
            widget.hide()
            widget = self.findChild(QtWidgets.QLabel, "toptext1")
            widget.hide()
            widget = self.findChild(QtWidgets.QLabel, "topclose")
            widget.hide()
            widget = self.findChild(QtWidgets.QLabel, "Q1_1")
            widget.hide()
            widget = self.findChild(QtWidgets.QLabel, "Q1_2")
            widget.hide()
            widget = self.findChild(QtWidgets.QComboBox, "Q1_3")
            widget.hide()
            widget = self.findChild(QtWidgets.QLabel, "Q1_4")
            widget.hide()
            widget = self.findChild(QtWidgets.QLabel, "Q1_5")
            widget.hide()
            widget = self.findChild(QtWidgets.QComboBox, "Q1_6")
            widget.hide()
        elif self.viewindex==1:
            print("Q2 to Q1")
            #change text

            if self.dblanguage=="日本語":
                widget = self.findChild(QtWidgets.QLabel, "toptext")
                widget.setText("利用されるお子さまについて教えてください。")
            elif self.dblanguage=="English":
                widget = self.findChild(QtWidgets.QLabel, "toptext")
                widget.setText("Please tell us about your child")
            elif self.dblanguage=="繁體中文":
                widget = self.findChild(QtWidgets.QLabel, "toptext")
                widget.setText("請告訴我們使用這個設施的孩子資訊")
            elif self.dblanguage=="简体中文":
                widget = self.findChild(QtWidgets.QLabel, "toptext")
                widget.setText("请告诉我们使用这个设施的孩子资讯")
            elif self.dblanguage=="Vietnamese":
                widget = self.findChild(QtWidgets.QLabel, "toptext")
                widget.setText("Xin vui lòng cho tôi biết về con của bạn.")
            #Q1 view show
            widget = self.findChild(QtWidgets.QLabel, "toppan")
            widget.show()
            widget = self.findChild(QtWidgets.QLabel, "toptext")
            widget.show()
            widget = self.findChild(QtWidgets.QLabel, "toptext1")
            widget.show()
            widget = self.findChild(QtWidgets.QLabel, "topclose")
            widget.show()
            widget = self.findChild(QtWidgets.QLabel, "Q1_1")
            widget.show()
            widget = self.findChild(QtWidgets.QLabel, "Q1_2")
            widget.show()
            widget = self.findChild(QtWidgets.QComboBox, "Q1_3")
            widget.show()
            widget = self.findChild(QtWidgets.QLabel, "Q1_4")
            widget.show()
            widget = self.findChild(QtWidgets.QLabel, "Q1_5")
            widget.show()
            widget = self.findChild(QtWidgets.QComboBox, "Q1_6")
            widget.show()
            widget = self.findChild(QtWidgets.QLabel, "toptext1")
            widget.hide()

            #Q2 view
            widget = self.findChild(QtWidgets.QPushButton, "Q2button_1")
            widget.hide()
            widget = self.findChild(QtWidgets.QPushButton, "Q2button_2")
            widget.hide()
            widget = self.findChild(QtWidgets.QPushButton, "Q2button_3")
            widget.hide()
            widget = self.findChild(QtWidgets.QPushButton, "nextbutton")
            widget.show()
        elif self.viewindex==2:
            print("Q3 to Q2")
            #Q2 view
            widget = self.findChild(QtWidgets.QPushButton, "Q2button_1")
            widget.show()
            widget = self.findChild(QtWidgets.QPushButton, "Q2button_2")
            widget.show()
            widget = self.findChild(QtWidgets.QPushButton, "Q2button_3")
            widget.show()

            widget = self.findChild(QtWidgets.QLabel, "toptext1")
            widget.setText("Q  1 / 5")

            if self.dblanguage=="日本語":
                widget = self.findChild(QtWidgets.QLabel, "toptext")
                widget.setText("mamaroのご利用は何回目ですが？")
            elif self.dblanguage=="English":
                widget = self.findChild(QtWidgets.QLabel, "toptext")
                widget.setText("How many times have you used mamaro?")
            elif self.dblanguage=="繁體中文":
                widget = self.findChild(QtWidgets.QLabel, "toptext")
                widget.setText("使用mamaro的次數？")
            elif self.dblanguage=="简体中文":
                widget = self.findChild(QtWidgets.QLabel, "toptext")
                widget.setText("使用mamaro的次数？")
            elif self.dblanguage=="Vietnamese":
                widget = self.findChild(QtWidgets.QLabel, "toptext")
                widget.setText("Bạn đã sử dụng mamaro bao nhiêu lần?")

            #Q3 view
            widget = self.findChild(QtWidgets.QToolButton, "Q3button_1")
            widget.hide()
            widget = self.findChild(QtWidgets.QToolButton, "Q3button_2")
            widget.hide()
            widget = self.findChild(QtWidgets.QToolButton, "Q3button_3")
            widget.hide()
            widget = self.findChild(QtWidgets.QToolButton, "Q3button_4")
            widget.hide()
            widget = self.findChild(QtWidgets.QToolButton, "Q3button_5")
            widget.hide()
            widget = self.findChild(QtWidgets.QToolButton, "Q3button_6")
            widget.hide()
        elif self.viewindex==3:
            print("Q4 to Q3")

            widget = self.findChild(QtWidgets.QLabel, "toptext2")
            widget.hide()
            widget = self.findChild(QtWidgets.QLabel, "toptext3")
            widget.hide()

            widget = self.findChild(QtWidgets.QLabel, "toptext")
            widget.show()
            widget = self.findChild(QtWidgets.QLabel, "toptext1")
            widget.setText("Q  2 / 5")

            if self.dblanguage=="日本語":
                widget = self.findChild(QtWidgets.QLabel, "toptext")
                widget.setText("mamaroをどのようにして知りましたか？")
            elif self.dblanguage=="English":
                widget = self.findChild(QtWidgets.QLabel, "toptext")
                widget.setText("How did you hear about mamaro?")
            elif self.dblanguage=="繁體中文":
                widget = self.findChild(QtWidgets.QLabel, "toptext")
                widget.setText("您是怎麼知道mamaro的？")
            elif self.dblanguage=="简体中文":
                widget = self.findChild(QtWidgets.QLabel, "toptext")
                widget.setText("您是怎么知道mamaro的？")
            elif self.dblanguage=="Vietnamese":
                widget = self.findChild(QtWidgets.QLabel, "toptext")
                widget.setText("Bạn biết về mamaro từ đâu?")


            #Q3 view
            widget = self.findChild(QtWidgets.QToolButton, "Q3button_1")
            widget.show()
            widget = self.findChild(QtWidgets.QToolButton, "Q3button_2")
            widget.show()
            widget = self.findChild(QtWidgets.QToolButton, "Q3button_3")
            widget.show()
            widget = self.findChild(QtWidgets.QToolButton, "Q3button_4")
            widget.show()
            widget = self.findChild(QtWidgets.QToolButton, "Q3button_5")
            widget.show()
            widget = self.findChild(QtWidgets.QToolButton, "Q3button_6")
            widget.show()

            #Q4 view
            widget = self.findChild(QtWidgets.QPushButton, "Q4button_1")
            widget.hide()
            widget = self.findChild(QtWidgets.QPushButton, "Q4button_2")
            widget.hide()
            widget = self.findChild(QtWidgets.QPushButton, "Q4button_3")
            widget.hide()
        elif self.viewindex==4:
            print("Q5 to Q4")

            widget = self.findChild(QtWidgets.QLabel, "toptext1")
            widget.setText("Q  3 / 5")

            if self.dblanguage=="日本語":
                widget = self.findChild(QtWidgets.QLabel, "toptext2")
                widget.setText("mamaroの空室状況をBabymapというアプリで")
                widget = self.findChild(QtWidgets.QLabel, "toptext3")
                widget.setText("調べることができるのを知っていましたか？")
            elif self.dblanguage=="English":
                widget = self.findChild(QtWidgets.QLabel, "toptext2")
                widget.setText("Did you know that you can check the availability")
                widget = self.findChild(QtWidgets.QLabel, "toptext3")
                widget.setText("of mamaro on an application called Babymap?")
            elif self.dblanguage=="繁體中文":
                widget = self.findChild(QtWidgets.QLabel, "toptext2")
                widget.setText("您知道從Babymap可以")
                widget = self.findChild(QtWidgets.QLabel, "toptext3")
                widget.setText("得知mamaro的使用狀況嗎？")
            elif self.dblanguage=="简体中文":
                widget = self.findChild(QtWidgets.QLabel, "toptext2")
                widget.setText("您知道从Babymap可以")
                widget = self.findChild(QtWidgets.QLabel, "toptext3")
                widget.setText("得知mamaro的使用状况吗？")
            elif self.dblanguage=="Vietnamese":
                widget = self.findChild(QtWidgets.QLabel, "toptext2")
                widget.setText("Bạn có biết rằng bạn có thể kiểm tra mamaro")
                widget = self.findChild(QtWidgets.QLabel, "toptext3")
                widget.setText("có người dùng hay không trong Babymap?")

            #Q5 view
            widget = self.findChild(QtWidgets.QPushButton, "Q5button_1")
            widget.hide()
            widget = self.findChild(QtWidgets.QPushButton, "Q5button_2")
            widget.hide()
            widget = self.findChild(QtWidgets.QPushButton, "Q5button_3")
            widget.hide()
            widget = self.findChild(QtWidgets.QPushButton, "Q5button_4")
            widget.hide()
            widget = self.findChild(QtWidgets.QPushButton, "Q5button_5")
            widget.hide()
            widget = self.findChild(QtWidgets.QPushButton, "Q5button_6")
            widget.hide()
            widget = self.findChild(QtWidgets.QPushButton, "Q5button_7")
            widget.hide()
            widget = self.findChild(QtWidgets.QPushButton, "Q5button_8")
            widget.hide()

            #Q4 view
            widget = self.findChild(QtWidgets.QPushButton, "Q4button_1")
            widget.show()
            widget = self.findChild(QtWidgets.QPushButton, "Q4button_2")
            widget.show()
            widget = self.findChild(QtWidgets.QPushButton, "Q4button_3")
            widget.show()

            #next button
            widget = self.findChild(QtWidgets.QPushButton, "nextbutton")
            widget.hide()
        elif self.viewindex==5:
            widget = self.findChild(QtWidgets.QLabel, "toptext2")
            widget.show()
            widget = self.findChild(QtWidgets.QLabel, "toptext3")
            widget.show()
            widget = self.findChild(QtWidgets.QLabel, "toptext1")
            widget.setText("Q  4 / 5")

            #Q5 view
            widget = self.findChild(QtWidgets.QPushButton, "Q5button_1")
            widget.show()
            widget = self.findChild(QtWidgets.QPushButton, "Q5button_2")
            widget.show()
            widget = self.findChild(QtWidgets.QPushButton, "Q5button_3")
            widget.show()
            widget = self.findChild(QtWidgets.QPushButton, "Q5button_4")
            widget.show()
            widget = self.findChild(QtWidgets.QPushButton, "Q5button_5")
            widget.show()
            widget = self.findChild(QtWidgets.QPushButton, "Q5button_6")
            widget.show()
            widget = self.findChild(QtWidgets.QPushButton, "Q5button_7")
            widget.show()
            widget = self.findChild(QtWidgets.QPushButton, "Q5button_8")
            widget.show()
            #Q6 view
            widget = self.findChild(QtWidgets.QPushButton, "Q6button_1")
            widget.hide()
            widget = self.findChild(QtWidgets.QPushButton, "Q6button_2")
            widget.hide()
            widget = self.findChild(QtWidgets.QPushButton, "Q6button_3")
            widget.hide()
            widget = self.findChild(QtWidgets.QPushButton, "Q6button_4")
            widget.hide()
            widget = self.findChild(QtWidgets.QLabel, "toptext")
            widget.hide()

            #next button
            widget = self.findChild(QtWidgets.QPushButton, "nextbutton")
            widget.show()



    def nextclick(self):
        # print(self.sender().objectName())
        # print(self.sender().text())
        self.viewindex+=1
        if self.viewindex==1:
            print("language to Q1")
            widget = self.findChild(QtWidgets.QLabel, "close")
            widget.hide()
            widget = self.findChild(QtWidgets.QLabel, "lan1")
            widget.hide()
            widget = self.findChild(QtWidgets.QLabel, "lan2")
            widget.hide()
            widget = self.findChild(QtWidgets.QComboBox, "lan3")
            widget.hide()

            #change text
            if self.dblanguage=="日本語":
                widget = self.findChild(QtWidgets.QLabel, "toptext")
                widget.setText("利用されるお子さまについて教えてください。")
            elif self.dblanguage=="English":
                widget = self.findChild(QtWidgets.QLabel, "toptext")
                widget.setText("Please tell us about your child")
            elif self.dblanguage=="繁體中文":
                widget = self.findChild(QtWidgets.QLabel, "toptext")
                widget.setText("請告訴我們使用這個設施的孩子資訊")
            elif self.dblanguage=="简体中文":
                widget = self.findChild(QtWidgets.QLabel, "toptext")
                widget.setText("请告诉我们使用这个设施的孩子资讯")
            elif self.dblanguage=="Vietnamese":
                widget = self.findChild(QtWidgets.QLabel, "toptext")
                widget.setText("Xin vui lòng cho tôi biết về con của bạn.")
            #back buttonbackbutton
            widget = self.findChild(QtWidgets.QPushButton, "backbutton")
            widget.show()
            #Q1 view show
            widget = self.findChild(QtWidgets.QLabel, "toppan")
            widget.show()
            widget = self.findChild(QtWidgets.QLabel, "toptext")
            widget.show()
            widget = self.findChild(QtWidgets.QLabel, "toptext1")
            widget.show()
            widget = self.findChild(QtWidgets.QLabel, "topclose")
            widget.show()
            widget = self.findChild(QtWidgets.QLabel, "Q1_1")
            widget.show()
            widget = self.findChild(QtWidgets.QLabel, "Q1_2")
            widget.show()
            widget = self.findChild(QtWidgets.QComboBox, "Q1_3")
            widget.show()
            widget = self.findChild(QtWidgets.QLabel, "Q1_4")
            widget.show()
            widget = self.findChild(QtWidgets.QLabel, "Q1_5")
            widget.show()
            widget = self.findChild(QtWidgets.QComboBox, "Q1_6")
            widget.show()
        elif self.viewindex==2:
            print("Q1 to Q2")
            #Q1 view
            widget = self.findChild(QtWidgets.QLabel, "Q1_1")
            widget.hide()
            widget = self.findChild(QtWidgets.QLabel, "Q1_2")
            widget.hide()
            widget = self.findChild(QtWidgets.QComboBox, "Q1_3")
            widget.hide()
            widget = self.findChild(QtWidgets.QLabel, "Q1_4")
            widget.hide()
            widget = self.findChild(QtWidgets.QLabel, "Q1_5")
            widget.hide()
            widget = self.findChild(QtWidgets.QComboBox, "Q1_6")
            widget.hide()

            if self.dblanguage=="日本語":
                widget = self.findChild(QtWidgets.QLabel, "toptext")
                widget.setText("mamaroのご利用は何回目ですが？")
            elif self.dblanguage=="English":
                widget = self.findChild(QtWidgets.QLabel, "toptext")
                widget.setText("How many times have you used mamaro?")
            elif self.dblanguage=="繁體中文":
                widget = self.findChild(QtWidgets.QLabel, "toptext")
                widget.setText("使用mamaro的次數？")
            elif self.dblanguage=="简体中文":
                widget = self.findChild(QtWidgets.QLabel, "toptext")
                widget.setText("使用mamaro的次数？")
            elif self.dblanguage=="Vietnamese":
                widget = self.findChild(QtWidgets.QLabel, "toptext")
                widget.setText("Bạn đã sử dụng mamaro bao nhiêu lần?")
            widget = self.findChild(QtWidgets.QLabel, "toptext1")
            widget.show()

            #Q2 view
            widget = self.findChild(QtWidgets.QPushButton, "Q2button_1")
            widget.show()
            widget = self.findChild(QtWidgets.QPushButton, "Q2button_2")
            widget.show()
            widget = self.findChild(QtWidgets.QPushButton, "Q2button_3")
            widget.show()
            widget = self.findChild(QtWidgets.QPushButton, "nextbutton")
            widget.hide()
        elif self.viewindex==6:
            print("Q5 to Q6")
            check=False
            for i in range(len(self.Q5choicelist)):
                if self.Q5choicelist[i]==1:
                    check=True
                    break
            if check:
                print("pass")
                widget = self.findChild(QtWidgets.QLabel, "toptext2")
                widget.hide()
                widget = self.findChild(QtWidgets.QLabel, "toptext3")
                widget.hide()

                #Q5 view
                widget = self.findChild(QtWidgets.QPushButton, "Q5button_1")
                widget.hide()
                widget = self.findChild(QtWidgets.QPushButton, "Q5button_2")
                widget.hide()
                widget = self.findChild(QtWidgets.QPushButton, "Q5button_3")
                widget.hide()
                widget = self.findChild(QtWidgets.QPushButton, "Q5button_4")
                widget.hide()
                widget = self.findChild(QtWidgets.QPushButton, "Q5button_5")
                widget.hide()
                widget = self.findChild(QtWidgets.QPushButton, "Q5button_6")
                widget.hide()
                widget = self.findChild(QtWidgets.QPushButton, "Q5button_7")
                widget.hide()
                widget = self.findChild(QtWidgets.QPushButton, "Q5button_8")
                widget.hide()
                #Q6 view
                widget = self.findChild(QtWidgets.QPushButton, "Q6button_1")
                widget.show()
                widget = self.findChild(QtWidgets.QPushButton, "Q6button_2")
                widget.show()
                widget = self.findChild(QtWidgets.QPushButton, "Q6button_3")
                widget.show()
                widget = self.findChild(QtWidgets.QPushButton, "Q6button_4")
                widget.show()
                widget = self.findChild(QtWidgets.QLabel, "toptext")
                widget.show()
                widget = self.findChild(QtWidgets.QLabel, "toptext1")
                widget.setText("Q  5 / 5")

                if self.dblanguage=="日本語":
                    widget = self.findChild(QtWidgets.QLabel, "toptext")
                    widget.setText("mamaroの満足度を教えてください。")
                elif self.dblanguage=="English":
                    widget = self.findChild(QtWidgets.QLabel, "toptext")
                    widget.setText("Were you satisfied with mamaro?")
                elif self.dblanguage=="繁體中文":
                    widget = self.findChild(QtWidgets.QLabel, "toptext")
                    widget.setText("請告訴我們您對mamaro的滿意度")
                elif self.dblanguage=="简体中文":
                    widget = self.findChild(QtWidgets.QLabel, "toptext")
                    widget.setText("请告诉我们您对mamaro的满意度")
                elif self.dblanguage=="Vietnamese":
                    widget = self.findChild(QtWidgets.QLabel, "toptext")
                    widget.setText("Xin vui lòng cho tôi biết mức độ hài lòng của bạn với mamaro.")

                self.sender().hide()


            else:
                print("no pass")
                self.viewindex-=1
                self.sender().setStyleSheet("background-color: rgba(250,20,20,185);border: none;")




    def Q1nextclick(self):
        print(self.sender().objectName())
        print(self.sender().text())
        print("Q1")




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
w.setWindowFlags(Qt.FramelessWindowHint)
w.setAttribute(Qt.WA_NoSystemBackground, True)
w.setAttribute(Qt.WA_TranslucentBackground, True)
#w.setWindowOpacity(0.5)
w.show()
sys.exit(app.exec())
