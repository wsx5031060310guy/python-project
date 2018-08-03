# import os
# import urllib
# import sys
# from requests import get  # to make GET request
# import operator
# import pymysql.cursors
# import serial
# import threading
# from threading import Timer
# from datetime import datetime, timedelta, date
# import re, uuid
# import urllib.request, json
# from firebase import firebase
# import psutil


import zipfile
import urllib.request
import os
from datetime import datetime
import pymysql.cursors
from threading import Timer
import threading
import time
import requests

def check_internet():
    url='http://www.google.com/'
    try:
        urllib.request.urlopen(url, timeout=1)
        return True
    except urllib.request.URLError as err:
        return False

global connection
connection=None
try:
    ##mysql config
    connection = pymysql.connect(host='host',
    user='username',
    password='password',
    db='DBname',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor)
    print(connection)
except:
    connection=None
    pass


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
couupdate=0
def counter():
    global couupdate,roomid,update_hour,update_minute,update_mode,updatecheck,updatecheckcou,connection
    #print(datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f'))
    couupdate+=1
    che=checksystemwork()
    if che==False:
        print("restart system")
        os.system("sudo kill -9 `pgrep -f usbcheck.py`")
        print("kill usbcheck")

        os.system("sudo kill -9 `pgrep -f checkmouse.py`")
        print("kill checkmouse")

        os.system("sudo kill -9 `pgrep -f videoplayer.py`")
        print("kill videoplayer")
        os.system("sudo kill -9 `pgrep -f videocover.py`")
        print("kill videocover")
        os.system("sudo kill -9 `pgrep -f videoplayerloop.py`")
        print("kill videoplayerloop")
        os.system("sudo kill -9 `pgrep -f sleep.py`")
        print("kill sleep")
        os.system("sudo kill -9 `pgrep -f lock.py`")
        print("kill lock")
        os.system("sudo kill -9 `pgrep -f window.py`")
        print("kill window")
        os.system("sudo kill -9 `pgrep -f mainview.py`")
        print("kill mainview")
        os.system("sudo kill -9 `pgrep -f timeout.py`")
        print("kill timeout")

        os.system("sudo kill -9 `pgrep -f chrome`")
        print("kill chrome")
        os.system("sudo kill -9 `pgrep -f vlc`")
        print("kill vlc")
        nowdatetime=datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
        try:
            with open(os.getcwd()+"/mamaro/syscheck.text", "w+") as f:
                f.write(nowdatetime+"\n")
        except:
            pass
        process_name= "usbcheck.py" # change this to the name of your process

        tmp = os.popen("ps -Af").read()
        if process_name not in tmp[:]:
            print ("start usbcheck.py")
            tpath=os.getcwd()+"/mamaro/"
            thread = threading.Thread(target=usbcheck, args=(tpath,1,))
            thread.daemon = True                            # Daemonize thread
            thread.start()

    if couupdate==150:
        ##check state of system reboot
        couupdate=0
        checkreboot="0"

        print(connection)
        try:
            connection = pymysql.connect(host='host',
            user='username',
            password='password',
            db='DBname',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor)
        except:
            connection=None
            pass

        try:
            with connection.cursor() as cursor:
                with connection.cursor() as cursor:
                    sql = "SELECT * FROM `nursing_room_power_state` WHERE `nursing_room_id`=%s"
                    cursor.execute(sql, (str(roomid),))
                    result = cursor.fetchall()
                    for res in result:
                        checkreboot=str(res['state'])
            with connection.cursor() as cursor:
                with connection.cursor() as cursor:
                    sql = "UPDATE `nursing_room_power_state` SET `doing_time`=NOW() WHERE `nursing_room_id`=%s"
                    cursor.execute(sql, (str(roomid),))
                    connection.commit()
        except:
            print ("DB connect fail")
            pass
        if checkreboot=="1":
            os.system('sudo reboot')

    # print(str(roomid))
    # print(str(update_hour))
    # print(str(update_minute))
    # print(str(update_mode))

    nowhourr=datetime.now().strftime('%H')
    nowhour=int(nowhourr)
    nowminn=datetime.now().strftime('%M')
    nowmin=int(nowminn)
    nowsecc=datetime.now().strftime('%S')
    nowsec=int(nowsecc)

    ##restart os every 7 am
    if str(nowhour)=="7" and str(nowmin)=="0" and int(nowsec)<2:
        os.system('sudo reboot')

    if str(update_mode)=="1":
        if str(update_hour)==str(nowhour) and str(update_minute)==str(nowmin) and int(nowsec)<2:
            print("update code start count")
            updatecheck=True

    if updatecheck:
        updatecheckcou+=1
    if updatecheckcou==3600:
        updatecheckcou=0
        updatecheck=False
        print("update code")
        os.system("sudo kill -9 `pgrep -f usbcheck.py`")
        print("kill usbcheck")

        os.system("sudo kill -9 `pgrep -f checkmouse.py`")
        print("kill checkmouse")

        os.system("sudo kill -9 `pgrep -f videoplayer.py`")
        print("kill videoplayer")
        os.system("sudo kill -9 `pgrep -f videocover.py`")
        print("kill videocover")
        os.system("sudo kill -9 `pgrep -f videoplayerloop.py`")
        print("kill videoplayerloop")
        os.system("sudo kill -9 `pgrep -f sleep.py`")
        print("kill sleep")
        os.system("sudo kill -9 `pgrep -f lock.py`")
        print("kill lock")
        os.system("sudo kill -9 `pgrep -f window.py`")
        print("kill window")
        os.system("sudo kill -9 `pgrep -f mainview.py`")
        print("kill mainview")
        os.system("sudo kill -9 `pgrep -f timeout.py`")
        print("kill timeout")

        os.system("sudo kill -9 `pgrep -f chrome`")
        print("kill chrome")
        os.system("sudo kill -9 `pgrep -f vlc`")
        print("kill vlc")
        zipurl=""
        zippassword=""
        try:
            with connection.cursor() as cursor:
                with connection.cursor() as cursor:
                    sql = "SELECT * FROM `nursing_room_code` WHERE `nursing_room_id`=%s"
                    cursor.execute(sql, (str(roomid),))
                    result = cursor.fetchall()
                    for res in result:
                        zipurl=res['url']
                        zippassword=res['password']

            with connection.cursor() as cursor:
                with connection.cursor() as cursor:
                    sql = "UPDATE `nursing_room_code` SET `update_time`=NOW() WHERE `nursing_room_id`=%s"
                    cursor.execute(sql, (str(roomid),))
                    connection.commit()

        except:
            print ("DB connect fail")
            pass
        tmpfile=datetime.now().strftime('%Y%m%d%H%M%S%f')
        try:
            urllib.request.urlretrieve(zipurl, os.getcwd()+"/download/"+tmpfile+".zip")


            zip_file = os.getcwd()+"/download/"+tmpfile+".zip"
            unzip=os.getcwd()+"/mamaro"
            with zipfile.ZipFile(zip_file,"r") as zip_ref:
                zip_ref.extractall(unzip,pwd=bytes(zippassword,'utf-8'))
        except:
            print ("get zip file fail")
            pass


        try:
            os.remove(zip_file)
        except:
            print ("Error delete file")
            pass

        process_name= "usbcheck.py" # change this to the name of your process

        tmp = os.popen("ps -Af").read()
        if process_name not in tmp[:]:
            print ("start usbcheck.py")
            tpath=os.getcwd()+"/mamaro/"
            thread = threading.Thread(target=usbcheck, args=(tpath,1,))
            thread.daemon = True                            # Daemonize thread
            thread.start()

def usbcheck(path,delay):
    print("delay "+str(delay))
    time.sleep(delay)
    print("start usbcheck")
    os.system('python3 '+str(path)+'usbcheck.py')

def checksystemwork():
    check=True
    txtdate="1992-05-07 12:00:00:00"
    nowdatetime=datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
    try:
        with open(os.getcwd()+"/mamaro/syscheck.text", "r+") as f:
            data = f.readlines()
            lines=data[0].split()
            txtdate=lines[0]+" "+lines[1]
    except:
        print("can not read syscheck.text")
        txtdate=nowdatetime
        pass
    if nowdatetime>txtdate:
        #print(txtdate)
        d0 = datetime.strptime(nowdatetime, '%Y-%m-%d %H:%M:%S:%f')
        d1 = datetime.strptime(txtdate, '%Y-%m-%d %H:%M:%S:%f')
        delta = d0 - d1
        #print (delta.seconds)
        if delta.seconds>120:
            check=False
        #print(str(check))
        print("now:"+nowdatetime+" , txt:"+txtdate+" , "+str(delta.seconds))

    return check

roomid=14
update_hour=1
update_minute=0
update_mode=1
updatecheck=False
updatecheckcou=0
if __name__ == '__main__':
    try:
        with open(os.getcwd()+"/mamaro/config.text", "r+") as f:
            data = f.readlines()
            lines=data[0].split(",")
            roomid=int(lines[0])
            update_hour=int(lines[1])
            update_minute=int(lines[2])
            update_mode=int(lines[3])
    except:
        print("read config fail")
        pass
    print(str(roomid))
    print(str(update_hour))
    print(str(update_minute))
    print(str(update_mode))
    updatecheck=False
    updatecheckcou=0
    if str(update_mode)=="0":
        print("update code")
        os.system("sudo kill -9 `pgrep -f usbcheck.py`")
        zipurl=""
        zippassword=""
        try:
            with connection.cursor() as cursor:
                with connection.cursor() as cursor:
                    sql = "SELECT * FROM `nursing_room_code` WHERE `nursing_room_id`=%s"
                    cursor.execute(sql, (str(roomid),))
                    result = cursor.fetchall()
                    for res in result:
                        zipurl=res['url']
                        zippassword=res['password']

            with connection.cursor() as cursor:
                with connection.cursor() as cursor:
                    sql = "UPDATE `nursing_room_code` SET `update_time`=NOW() WHERE `nursing_room_id`=%s"
                    cursor.execute(sql, (str(roomid),))
                    connection.commit()

        except:
            print ("DB connect fail")
            pass
        tmpfile=datetime.now().strftime('%Y%m%d%H%M%S%f')
        try:
            urllib.request.urlretrieve(zipurl, os.getcwd()+"/download/"+tmpfile+".zip")


            zip_file = os.getcwd()+"/download/"+tmpfile+".zip"
            unzip=os.getcwd()+"/mamaro"
            with zipfile.ZipFile(zip_file,"r") as zip_ref:
                zip_ref.extractall(unzip,pwd=bytes(zippassword,'utf-8'))
        except:
            print ("get zip file fail")
            pass

        try:
            os.remove(zip_file)
        except:
            print ("Error delete file")
            pass

        process_name= "usbcheck.py" # change this to the name of your process

        tmp = os.popen("ps -Af").read()
        if process_name not in tmp[:]:
            print ("start usbcheck.py")
            tpath=os.getcwd()+"/mamaro/"
            thread = threading.Thread(target=usbcheck, args=(tpath,1,))
            thread.daemon = True                            # Daemonize thread
            thread.start()
    nowdatetime=datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
    try:
        with open(os.getcwd()+"/mamaro/syscheck.text", "w+") as f:
            f.write(nowdatetime+"\n")
    except:
        pass

    global rt
    rt = RepeatedTimer(1, counter)
    tpath=os.getcwd()+"/mamaro/"
    #tpath=""
    thread = threading.Thread(target=usbcheck, args=(tpath,1,))
    thread.daemon = True                            # Daemonize thread
    thread.start()
