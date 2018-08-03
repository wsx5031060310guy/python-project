# # coding: UTF-8

import os, shutil
import urllib
import sys
from requests import get  # to make GET request
import operator
import pymysql.cursors
import serial
import threading
from threading import Timer
from datetime import datetime, timedelta, date
import re, uuid
import urllib.request, json
from firebase import firebase
import psutil
import time
import requests
import cv2
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
import base64

def check_internet():
    url='http://www.google.com/'
    try:
        urllib.request.urlopen(url, timeout=1)
        return True
    except urllib.request.URLError as err:
        return False
##mysql config
global connection
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
##firebase config
global firebase_sys,firebase_state,firebase_grid_eye
firebase_sys=None
firebase_state=None
firebase_grid_eye=None
try:
    firebase_sys = firebase.FirebaseApplication("firebase url", None)
    firebase_state = firebase.FirebaseApplication("firebase url", None)
    firebase_grid_eye=firebase.FirebaseApplication("firebase url", None)
except:
    firebase_sys=None
    firebase_state=None
    firebase_grid_eye=None
    pass

def update_log(id, log, type):
    try:
        with connection.cursor() as cursor:
            with connection.cursor() as cursor:
                sql = "INSERT INTO `nursing_room_log` (`nursing_room_id`,`log`,`update_time`,`type`) VALUES (%s,%s,NOW(),%s)"
                cursor.execute(sql, (str(id),str(log),str(type)))
                connection.commit()
    except:
        print("insert data for state fail")
        pass

def download(url, file_name,id,DBid,localname):

    try:
        update_log(id, "start download "+localname, "0")
        update_log(id, DBid+",0", "2")
        startTime = time.time()
        with open(file_name, "wb") as f:
            print ("Downloading %s" % file_name)

            response = requests.get(url, stream=True)
            total_length = response.headers.get('content-length')

            if total_length is None: # no content length header
                f.write(response.content)
            else:
                nowdatetime=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(nowdatetime)
                dl = 0
                total_length = int(total_length)
                cutsize=int(total_length/10)
                if cutsize<2097152:
                    cutsize=2097152
                for data in response.iter_content(chunk_size=cutsize):
                    dl += len(data)
                    f.write(data)
                    done = int(50 * dl / total_length)
                    percent=int(100 * (dl / total_length))
                    nowdatetime=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    print(str(nowdatetime))
                    print(str(dl)+","+str(total_length)+","+str(percent))

                    update_log(id, DBid+","+localname+","+str(dl)+","+str(total_length)+","+str(percent), "1")
                endTime = time.time()
                nowdatetime=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(nowdatetime)
                update_log(id, "end download "+localname, "0")
                update_log(id, DBid+",1", "2")
        # open in binary mode
        # with open(file_name, "wb") as file:
        #     # get request
        #     response = get(url)
        #     # write to file
        #     file.write(response.content)
    except:
        update_log(id, "fail download "+localname, "0")
        print("get video fail")
        pass
class video_DBinfo(object):
    """__init__() functions as the class constructor"""
    def __init__(self, play_index=None, video_local_name=None, video_size=None, video_url=None, DBid=None):
        self.play_index = play_index
        self.video_local_name = video_local_name
        self.video_size = video_size
        self.video_url = video_url
        self.DBid = DBid

def delete_blob( blob_name):
    """Deletes a blob from the bucket."""
    bucket = storage.bucket()
    blob = bucket.blob(blob_name)

    blob.delete()

    print('Blob {} deleted.'.format(blob_name))


def upload_blob( source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    bucket = storage.bucket()
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print('File {} uploaded to {}.'.format(
        source_file_name,
        destination_blob_name))

def list_blobs():
    """Lists all the blobs in the bucket."""
    bucket = storage.bucket()

    blobs = bucket.list_blobs()

    for blob in blobs:
        print(blob.name)

def list_blobs_del(tmpname):
    """Lists all the blobs in the bucket."""
    bucket = storage.bucket()

    blobs = bucket.list_blobs()

    for blob in blobs:
        print(blob.name)
        findstr=tmpname
        #print(str(blob.name).find(findstr))
        if str(blob.name).find(findstr)>=0:
            delete_blob(blob.name)

def delete_folder():
    ##delete old files
    deldate = (datetime.now() - timedelta(days = 3)).strftime('%Y%m%d')
    if os.path.isdir(os.getcwd()+"/cvvideo/"+str(deldate)):
        list_blobs_del(str(deldate))
    shutil.rmtree(os.getcwd()+"/cvvideo/"+str(deldate), ignore_errors=True)
    print("delete "+os.getcwd()+"/cvvideo/"+str(deldate))


def realtime_cam(id,imgurl,firebase1):
    #upload data to firebase
    nowdatetime=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data = {'id': str(id), 'imgurl': str(imgurl), 'time': str(nowdatetime)}
    result = firebase1.post('/camera/'+str(id), data)


def push_system_info(id,firebase1):
    try:
        nowdatetime=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        #system info
        Boot_Start = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(psutil.boot_time()))
        time.sleep(0.5)
        Cpu_usage = psutil.cpu_percent()
        RAM_percent = psutil.virtual_memory().percent
        Net_sent = psutil.net_io_counters().bytes_sent
        Net_recv = psutil.net_io_counters().bytes_recv

        data = {'id': str(id), 'time': str(nowdatetime), 'total_cpu': str(Cpu_usage)+"%", 'total_mem': str(RAM_percent)+"%", 'Boot_Start_Time': str(Boot_Start)}
        result = firebase1.post('/mamaro/system_info/'+str(id), data)
        data = {'id': str(id), 'time': str(nowdatetime), 'download': str(Net_recv), 'upload': str(Net_sent)}
        result = firebase1.post('/mamaro/wifi_useage/'+str(id), data)
    except:
        print("push sys info fail")
        pass



def push_pir_state(id,state,firebase1):
    try:
        nowdatetime=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data = {'id': str(id), 'state': str(state), 'time': str(nowdatetime)}
        result = firebase1.post('/mamarostate/pir/'+str(id), data)
    except:
        print("push pir state fail")
        pass

def push_lock_state(id,state,firebase1):
    try:
        nowdatetime=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data = {'id': str(id), 'state': str(state), 'time': str(nowdatetime)}
        result = firebase1.post('/mamarostate/lock/'+str(id), data)
    except:
        print("push lock state fail")
        pass

def push_babymap_state(id,state):
    url1="api url"+str(id)+"&is_busy="+str(state)
    try:
        with urllib.request.urlopen(url1) as url:
            data = json.loads(url.read().decode())
            print(data["result"])
    except:
        print("push state fail")
        pass

def getvideodata(id):
    global checkupdatevideo
    #get data
    videolist=[]
    checkupdatevideo=False
    totalcount=0
    video_oneloop=1
    if check_internet():
        checkdb=True
        try:
            with connection.cursor() as cursor:
                with connection.cursor() as cursor:
                    sql = "SELECT `a`.`play_index`,`a`.`video_local_name`,`b`.`video_size`,`b`.`video_url`,`b`.`id` FROM `nursing_room_connect_video` as `a` inner join `nursing_room_video_info` as `b` on `a`.`nursing_room_video_info_id`=`b`.`id` WHERE `a`.`nursing_room_id`=%s"
                    cursor.execute(sql, (id,))
                    result = cursor.fetchall()
                    for res in result:
                        totalcount+=1
                        videolist.append(video_DBinfo(res['play_index'],res['video_local_name'],res['video_size'],res['video_url'],res['id']))
                        # print(res)
                        # print(res['company'])
            with connection.cursor() as cursor:
                with connection.cursor() as cursor:
                    sql = "SELECT * FROM `nursing_room` WHERE `id`=%s"
                    cursor.execute(sql, (id,))
                    result = cursor.fetchall()
                    for res in result:
                        video_oneloop=res['video_control']

        except:
            checkdb=False
            pass
        if checkdb:
            with open(os.getcwd()+'/mamaro/playconfig.text','w'): pass
            sorted_x = sorted(videolist, key=operator.attrgetter('play_index'))
            #sorted(videolist, key=lambda x: x[0])
            update_log(id, "start update playconfig", "0")
            with open(os.getcwd()+"/mamaro/playconfig.text", "a") as f:
                f.write(str(totalcount)+","+str(video_oneloop)+"\n")
                update_log(id, str(totalcount)+","+str(video_oneloop), "3")
                for i in range(len(sorted_x)):
                    f.write(str(sorted_x[i].video_local_name)+","+str(sorted_x[i].play_index)+","+str(sorted_x[i].DBid)+"\n")
                    update_log(id, str(sorted_x[i].video_local_name)+","+str(sorted_x[i].play_index)+","+str(sorted_x[i].DBid), "3")
            update_log(id, "end update playconfig", "0")

            search_folder = os.getcwd()+"/mamaro/video"
            # videoFile = url.split('/')[-1].split('#')[0].split('?')[0] #stripping the name of the file.
            # print(videoFile)
            update_log(id, "start update video", "0")
            for i in range(len(sorted_x)):
                boolcheck=True
                for root, dirs, files in os.walk(search_folder): # using the os.walk module to find the files.
                    for name in files:
                        print(name)
                        """Checking the videofile in the current directory and the sub-directories"""
                        if sorted_x[i].video_local_name == os.path.join(name):  #checking if the file is already present in the internal memory.(Traverse through subdirectories as well)
                            filesize=os.path.getsize(search_folder+"/"+name)
                            if int(sorted_x[i].video_size)!=filesize:
                                print(sorted_x[i].video_size+" , "+str(filesize))
                                boolcheck=True
                                print(sorted_x[i].video_local_name+" size not correct")
                                update_log(id, sorted_x[i].video_local_name+" need update", "0")
                            else:
                                boolcheck=False
                                print(sorted_x[i].video_local_name+" size correct")
                                update_log(id, sorted_x[i].video_local_name+" not need update", "0")
                                update_log(id, str(sorted_x[i].DBid)+",0", "2")
                                update_log(id, str(sorted_x[i].DBid)+",1", "2")
                            print(sorted_x[i].video_local_name+" is already present in the internal memory")
                            break  # Returning the confirmation that the file is present.
                if boolcheck:
                    print("download "+sorted_x[i].video_local_name)
                    curDir = os.getcwd()+"/mamaro/video"   # getting the current working directory.
                    fullVideoPath = os.path.join(curDir,sorted_x[i].video_local_name)  # Making the full path of the video file.
                    download(sorted_x[i].video_url, fullVideoPath,id,str(sorted_x[i].DBid),sorted_x[i].video_local_name)
            update_log(id, "end update video", "0")

    checkupdatevideo=True
    print(checkupdatevideo)
checkpir=False
checklock=False
checklockvideo=0
checkwrite=False
checkvideo=False
checktimeout=False
babymapid=0
countsleep=0
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

checkreadfile=True
checkupdatevideo=True
def counter():
    global checktimeout,babymapid,couupdate,grideye,countsleep,checkpir,checklock,checkreadfile,checkupdatevideo

    couupdate+=1
    if checkpir==True or checklock==True:
        realtime_grid_eye(str(roomid),grideye,firebase_grid_eye)
    ####update Information to cloud
    if couupdate==150:
        #push sys Information to firebase
        try:
            thread = threading.Thread(target=push_system_info, args=(str(roomid),firebase_sys,))
            thread.start()
        except:
            pass

        checkbabymapid=True
        GPSlat="0"
        GPSlng="0"
        mamaroname=""
        try:
            with connection.cursor() as cursor:
                with connection.cursor() as cursor:
                    sql = "SELECT * FROM `nursing_room` WHERE `id`=%s"
                    cursor.execute(sql, (roomid,))
                    result = cursor.fetchall()
                    for res in result:
                        babymapid=res['babymap_place_id']
                        mamaroname=res['name']
                        GPSlat=res['GPS_lat']
                        GPSlng=res['GPS_lng']
                        print(str(babymapid))
                        checkbabymapid=False
            if babymapid is None or babymapid=="":
                checkbabymapid=True
        except:
            checkbabymapid=False
            pass

        if checkbabymapid:
            url = "api url"
            data = {
                "Place[lat]" : str(GPSlat),
                "Place[lon]" : str(GPSlng),
                "Place[name]" : str(mamaroname),
                "Review[star]" : "5",
                "Review[message]" : "text",
                "Place[place_category_id]" : "9"
                }
            try:
                data = urllib.parse.urlencode(data).encode("utf-8")
                with urllib.request.urlopen(url, data=data) as res:
                    html = json.loads(res.read().decode("utf-8"))
                    print(html["result"])
                    babymapid=html["result"]
                try:
                    with connection.cursor() as cursor:
                        with connection.cursor() as cursor:
                            sql = "UPDATE `nursing_room` SET `babymap_place_id`=%s WHERE `id`=%s"
                            cursor.execute(sql, (str(babymapid),str(roomid)))
                            connection.commit()
                except:
                    babymapid="0"
                    pass
            except:
                babymapid="0"
                pass
        print(str(babymapid))
        couupdate=0
    ####update Information to cloud
    total=60*20
    #print(update_hour)

    nowhourr=datetime.now().strftime('%H')
    nowhour=int(nowhourr)
    nowminn=datetime.now().strftime('%M')
    nowmin=int(nowminn)
    nowsecc=datetime.now().strftime('%S')
    nowsec=int(nowsecc)
    # print(nowhour)
    # print(nowmin)
    if str(update_mode)=="1":
        if str(update_hour)==str(nowhour) and str(update_minute)==str(nowmin) and int(nowsec)<2:
            print("update video")
            if checkupdatevideo:
                getvideodata(roomid)

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
        if total<=0:
            print("timeout start")
            if checktimeout==False:
                print("kill all")

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

                os.system("sudo kill -9 `pgrep -f QA.py`")
                print("kill QA")
                os.system("sudo kill -9 `pgrep -f QA1.py`")
                print("kill QA1")

                os.system("sudo kill -9 `pgrep -f chrome`")
                print("kill chrome")
                os.system("sudo kill -9 `pgrep -f vlc`")
                print("kill vlc")

            checktimeout=True
            if checkpir==False and checklock==False:
                print("sleep & timeout")
                os.system("sudo kill -9 `pgrep -f timeout.py`")
                process_name= "sleep.py" # change this to the name of your process

                tmp = os.popen("ps -Af").read()
                if process_name not in tmp[:]:
                    print ("start sleep.py")
                    thread = threading.Thread(target=sleep, args=("Thread-11",))
                    thread.daemon = True                            # Daemonize thread
                    thread.start()
                print("reset time from timeout mode to sleep mode")
                total=60*20
                try:
                    with open(os.getcwd()+"/mamaro/counter.text", "w+") as f:
                        f.write(str(total)+"\n")
                except:
                    pass

                if countsleep>0:
                    try:
                        thread = threading.Thread(target=push_babymap_state, args=(str(babymapid),"0",))
                        thread.start()
                    except:
                        pass
                    try:
                        with connection.cursor() as cursor:
                            with connection.cursor() as cursor:
                                sql = "INSERT INTO `nursing_room_state_time` (`nursing_room_id`,`state`,`update_time`) VALUES (%s,%s,NOW())"
                                cursor.execute(sql, (str(roomid),str(0)))
                                connection.commit()
                    except:
                        print("insert data to DB fail")
                        pass
                    try:
                        thread = threading.Thread(target=push_lock_state, args=(str(roomid),"1",firebase_state,))
                        thread.start()
                    except:
                        pass
                    countsleep=0

            else:
                print("kill all")

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

                os.system("sudo kill -9 `pgrep -f QA.py`")
                print("kill QA")
                os.system("sudo kill -9 `pgrep -f QA1.py`")
                print("kill QA1")

                os.system("sudo kill -9 `pgrep -f chrome`")
                print("kill chrome")
                os.system("sudo kill -9 `pgrep -f vlc`")
                print("kill vlc")


                process_name= "timeout.py" # change this to the name of your process

                tmp = os.popen("ps -Af").read()

                if process_name not in tmp[:]:
                    print ("start timeout.py")
                    thread = threading.Thread(target=timeout, args=("Thread-8",))
                    thread.daemon = True                            # Daemonize thread
                    thread.start()
        else:
            #print ("kill timeout")
            os.system("sudo kill -9 `pgrep -f timeout.py`")
            checktimeout=False

        ####for video counter
        if checkwrite:
            total-=1
            print(str(total))
            try:
                #write date time
                with open(os.getcwd()+"/mamaro/counter.text", "w+") as f:
                    f.write(str(total)+"\n")
            except:
                print("write count fail")
                pass
        ####for video counter



def checkmouse(threadName):
    print("start checkmouse")
    os.system('python3 '+os.getcwd()+'/mamaro/checkmouse.py')
def sleep(threadName):
    print("kill chrome")
    os.system("sudo kill -9 `pgrep -f chrome`")
    print("start sleep")
    os.system('python3 '+os.getcwd()+'/mamaro/sleep.py')
def timeout(threadName):
    print("start timeout")
    os.system('python3 '+os.getcwd()+'/mamaro/timeout.py')
def lock(threadName):
    print("kill chrome")
    os.system("sudo kill -9 `pgrep -f chrome`")
    print("start lock")
    os.system('python3 '+os.getcwd()+'/mamaro/lock.py')
def video(threadName):
    print("kill chrome")
    os.system("sudo kill -9 `pgrep -f chrome`")
    print("start videoplayer")
    os.system('python3 '+os.getcwd()+'/mamaro/videoplayer.py')
couwifistate=0
def main(args):
    # while True:
    global rt,checkpir,checklock,checkwrite,checkvideo,checklockvideo,checktimeout,babymapid,countsleep,couwifistate,couupdate,grideye,firebase_sys,firebase_state,firebase_grid_eye,connection
    rt = RepeatedTimer(1, counter)
    print ("start checkmouse.py")
    thread = threading.Thread(target=checkmouse, args=("Thread-12",))
    thread.daemon = True                            # Daemonize thread
    thread.start()

    countlock=0
    countpir=0
    countsleep=0

    cclock=0
    ccpir=0

    while True:
        # timeoutを秒で設定．ボーレートはデフォルトで9600．
        ser = serial.Serial('/dev/ttyACM0', 115200, timeout=5.0)
        line1 = ser.readline()
        linestr=line1.decode("utf-8")
        lines=linestr.split(",")
        #print(linestr)
        if len(lines)>3:
            ##camera
            micorwave_state="0"
            try:
                micorwave_state=str(lines[4].replace('\r\n',""))
            except:
                pass
            try:
                with open(os.getcwd()+"/mamaro/micorwave_value.text", "w+") as f:
                    f.write(str(micorwave_state)+"\n")
            except:
                print("write value fail")
                pass
            ##camera
            writesystime()
            couwifistate+=1
            if couwifistate==600:

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
                print(firebase_state)
                try:
                    firebase_sys = firebase.FirebaseApplication("firebase url", None)
                    firebase_state = firebase.FirebaseApplication("firebase url", None)
                    firebase_grid_eye=firebase.FirebaseApplication("firebase url", None)
                    firebase_cam=firebase.FirebaseApplication("firebase url", None)
                except:
                    firebase_sys = None
                    firebase_state = None
                    firebase_grid_eye= None
                    firebase_cam=None
                    pass

                try:
                    with connection.cursor() as cursor:
                        with connection.cursor() as cursor:
                            sql = "INSERT INTO `nursing_room_wifi_state` (`nursing_room_id`,`update_time`) VALUES (%s,NOW())"
                            cursor.execute(sql, (str(roomid)))
                            connection.commit()
                except:
                    print("insert data for wifi state fail")
                    pass
                couwifistate=0


            if lines[1]=="0":
                try:
                    linegrdre=lines[5].replace('\r\n',"")
                    linegrid=linegrdre.split(" ")
                    grideye=linegrdre
                except:
                    pass


            if lines[0]=="1":
                if checkpir==False:
                    ccpir+=1
                else:
                    ccpir=0
                if ccpir>2:
                    checkpir=True
            elif lines[0]=="0":
                if checkpir==True:
                    ccpir+=1
                else:
                    ccpir=0
                if ccpir>2:
                    checkpir=False
            if lines[2]=="1":
                if checklock==False:
                    cclock+=1
                else:
                    cclock=0
                if cclock>2:
                    checklock=True
            elif lines[2]=="0":
                if checklock==True:
                    cclock+=1
                else:
                    cclock=0
                if cclock>2:
                    checklock=False

            ####insert into DB state
            if checkpir:
                countpir+=1
                if countpir==1:
                    try:
                        with connection.cursor() as cursor:
                            with connection.cursor() as cursor:
                                sql = "INSERT INTO `nursing_room_pir_state_time` (`nursing_room_id`,`pir_state`,`update_time`) VALUES (%s,%s,NOW())"
                                cursor.execute(sql, (str(roomid),str(1)))
                                connection.commit()
                    except:
                        print("insert data for pir state fail")
                        pass
                    try:
                        thread = threading.Thread(target=push_pir_state, args=(str(roomid),"1",firebase_state,))
                        thread.start()
                    except:
                        pass
            else:
                if countpir>0:
                    try:
                        with connection.cursor() as cursor:
                            with connection.cursor() as cursor:
                                sql = "INSERT INTO `nursing_room_pir_state_time` (`nursing_room_id`,`pir_state`,`update_time`) VALUES (%s,%s,NOW())"
                                cursor.execute(sql, (str(roomid),str(0)))
                                connection.commit()
                    except:
                        print("insert data for pir state fail")
                        pass
                    try:
                        thread = threading.Thread(target=push_pir_state, args=(str(roomid),"0",firebase_state,))
                        thread.start()
                    except:
                        pass
                countpir=0

            if checklock:
                countlock+=1
                if countlock==1:
                    try:
                        with connection.cursor() as cursor:
                            with connection.cursor() as cursor:
                                sql = "INSERT INTO `nursing_room_lock_state_time` (`nursing_room_id`,`lock_state`,`update_time`) VALUES (%s,%s,NOW())"
                                cursor.execute(sql, (str(roomid),str(0)))
                                connection.commit()
                    except:
                        print("insert data for lock state fail")
                        pass
                    try:
                        thread = threading.Thread(target=push_lock_state, args=(str(roomid),"0",firebase_state,))
                        thread.start()
                    except:
                        pass
            else:
                if countlock>0:
                    try:
                        with connection.cursor() as cursor:
                            with connection.cursor() as cursor:
                                sql = "INSERT INTO `nursing_room_lock_state_time` (`nursing_room_id`,`lock_state`,`update_time`) VALUES (%s,%s,NOW())"
                                cursor.execute(sql, (str(roomid),str(1)))
                                connection.commit()
                    except:
                        print("insert data for lock state fail")
                        pass
                    try:
                        thread = threading.Thread(target=push_lock_state, args=(str(roomid),"1",firebase_state,))
                        thread.start()
                    except:
                        pass
                countlock=0
            ####insert into DB state

            if checktimeout==False:
                #sleep
                if checkpir==False and checklock==False:
                    os.system("sudo kill -9 `pgrep -f videoplayer.py`")
                    print("kill videoplayer")
                    os.system("sudo kill -9 `pgrep -f videocover.py`")
                    print("kill videocover")
                    os.system("sudo kill -9 `pgrep -f videoplayerloop.py`")
                    print("kill videoplayerloop")
                    os.system("sudo kill -9 `pgrep -f lock.py`")
                    print("kill lock")
                    os.system("sudo kill -9 `pgrep -f window.py`")
                    print("kill window")
                    os.system("sudo kill -9 `pgrep -f mainview.py`")
                    print("kill mainview")

                    os.system("sudo kill -9 `pgrep -f QA.py`")
                    print("kill QA")
                    os.system("sudo kill -9 `pgrep -f QA1.py`")
                    print("kill QA1")

                    os.system("sudo kill -9 `pgrep -f chrome`")
                    print("kill chrome")
                    os.system("sudo kill -9 `pgrep -f vlc`")
                    print("kill vlc")
                    process_name= "sleep.py" # change this to the name of your process

                    tmp = os.popen("ps -Af").read()
                    if process_name not in tmp[:]:
                        print("pir:"+lines[0]+",lock:"+lines[1])
                        print("pir:"+str(checkpir)+",lock:"+str(checklock))
                        print(lines)
                        print ("start sleep.py")
                        thread = threading.Thread(target=sleep, args=("Thread-11",))
                        thread.daemon = True                            # Daemonize thread
                        thread.start()

                    if countsleep>0:
                        try:
                            thread = threading.Thread(target=push_babymap_state, args=(str(babymapid),"0",))
                            thread.start()
                        except:
                            pass

                        try:
                            with connection.cursor() as cursor:
                                with connection.cursor() as cursor:
                                    sql = "INSERT INTO `nursing_room_state_time` (`nursing_room_id`,`state`,`update_time`) VALUES (%s,%s,NOW())"
                                    cursor.execute(sql, (str(roomid),str(0)))
                                    connection.commit()
                        except:
                            print("insert data for state fail")
                            pass
                        countsleep=0
                else:
                    process_name= "sleep.py" # change this to the name of your process
                    tmp = os.popen("ps -Af").read()
                    if process_name in tmp[:]:
                        os.system("sudo kill -9 `pgrep -f sleep.py`")

                    countsleep+=1
                    if countsleep==1:
                        try:
                            thread = threading.Thread(target=push_babymap_state, args=(str(babymapid),"1",))
                            thread.start()
                        except:
                            pass

                        try:
                            with connection.cursor() as cursor:
                                with connection.cursor() as cursor:
                                    sql = "INSERT INTO `nursing_room_state_time` (`nursing_room_id`,`state`,`update_time`) VALUES (%s,%s,NOW())"
                                    cursor.execute(sql, (str(roomid),str(1)))
                                    connection.commit()
                        except:
                            print("insert data for state fail")
                            pass

                if checkpir:
                    checkwrite=False
                    process_name= "lock.py" # change this to the name of your process
                    #print("pir sensor lock start")
                    tmp = os.popen("ps -Af").read()

                    if process_name not in tmp[:]:
                        print("reset time from checkpir sensor")
                        total=60*20
                        try:
                            with open(os.getcwd()+"/mamaro/counter.text", "w+") as f:
                                f.write(str(total)+"\n")
                        except:
                            pass
                        print ("start lock.py")
                        thread = threading.Thread(target=lock, args=("Thread-1",))
                        thread.daemon = True                            # Daemonize thread
                        thread.start()
                else:
                    os.system("sudo kill -9 `pgrep -f lock.py`")

                if checklock:
                    checklockvideo+=1
                    if checklockvideo==1:
                        print("lock sensor video start")
                        process_name= "videoplayer.py" # change this to the name of your process

                        tmp = os.popen("ps -Af").read()

                        if process_name not in tmp[:]:
                            print ("start videoplayer.py")
                            thread = threading.Thread(target=video, args=("Thread-2",))
                            thread.daemon = True                            # Daemonize thread
                            thread.start()

                    checkvideo=False
                    process_name= "videoplayer.py" # change this to the name of your process
                    tmp = os.popen("ps -Af").read()
                    if process_name in tmp[:]:
                        checkvideo=True
                    process_name= "videoplayerloop.py" # change this to the name of your process
                    tmp = os.popen("ps -Af").read()
                    if process_name in tmp[:]:
                        checkvideo=True
                    if checkvideo:
                        checkwrite=True
                    else:
                        checkwrite=False


                else:
                    checkwrite=False
                    checklockvideo=0
                    #print("pir sensor lock end")
                    os.system("sudo kill -9 `pgrep -f videoplayer.py`")
                    #print("kill videoplayer")
                    os.system("sudo kill -9 `pgrep -f vlc`")
                    #print("kill vlc")




def ps(output):
    sys.stdout.write(str(output))
    sys.stdout.flush()

def create_grid_eye():
    tempgrideyefile=datetime.now().strftime('%Y%m%d%H%M%S%f')
    gpath=os.getcwd()+"/grid_eye/"+tempgrideyefile+".text"
    with open(gpath,'w+'): pass


def write_grid_eye(grid_eye_str):
    #write data to text file
    gpath=os.getcwd()+"/grid_eye/"+tempgrideyefile+".text"
    with open(gpath, "a") as f:
        f.write(str(grid_eye_str)+"\n")

def upload_grid_eye():
    #upload data to cloud
    gpath=os.getcwd()+"/grid_eye/"+tempgrideyefile+".text"

def realtime_grid_eye(id,grid_eye_str,firebase1):
    try:
        #upload data to firebase
        nowdatetime=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data = {'id': str(id), 'eye': str(grid_eye_str), 'time': str(nowdatetime)}
        result = firebase1.post('/grid_eye/'+str(id), data)
    except:
        print("grid eye data upload fail")
        pass

def writesystime():
    nowdatetime=datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
    try:
        with open(os.getcwd()+"/mamaro/syscheck.text", "w+") as f:
            f.write(nowdatetime+"\n")
    except:
        pass


roomid=38
update_hour=1
update_minute=0
update_mode=1
couupdate=0
tempgrideyefile=""
grideye=""
if __name__ == '__main__':
    cred = credentials.Certificate(os.getcwd()+'/key/key.json')
    firebase_admin.initialize_app(cred, {
        'storageBucket': 'storage url'
    })
    #QWidget.setGeometry (int x, int y, int w, int h)
    try:
        with open(os.getcwd()+"/mamaro/config.text", "r+") as f:
            data = f.readlines()
            lines=data[0].split(",")
            roomid=int(lines[0])
            update_hour=int(lines[1])
            update_minute=int(lines[2])
            update_mode=int(lines[3])
    except:
        pass
    print(str(roomid))
    print(str(update_hour))
    print(str(update_minute))
    print(str(update_mode))
    couupdate=0
    tempgrideyefile=datetime.now().strftime('%Y%m%d%H%M%S%f')


    ##mac address fix id
    babymapid="0"
    checkbabymapid=True
    GPSlat="0"
    GPSlng="0"
    mamaroname=""

    macaddr=':'.join(re.findall('..', '%012x' % uuid.getnode()))
    print(macaddr)
    print(macaddr.replace(":",""))
    macaddr1=macaddr.replace(":","")
    try:
        with connection.cursor() as cursor:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM `nursing_room` WHERE `mac_addr`=%s"
                cursor.execute(sql, (macaddr1,))
                result = cursor.fetchall()
                for res in result:
                    roomid=res['id']
                    babymapid=res['babymap_place_id']
                    mamaroname=res['name']
                    GPSlat=res['GPS_lat']
                    GPSlng=res['GPS_lng']
                    print(str(babymapid))
                    checkbabymapid=False
        if babymapid is None or babymapid=="":
            checkbabymapid=True
    except:
        print("get data for mac addr fix id fail")
        checkbabymapid=False
        pass


    if checkbabymapid:
        url = "api url"
        data = {
            "Place[lat]" : str(GPSlat),
            "Place[lon]" : str(GPSlng),
            "Place[name]" : str(mamaroname),
            "Review[star]" : "5",
            "Review[message]" : "text",
            "Place[place_category_id]" : "9"
            }
        try:
            data = urllib.parse.urlencode(data).encode("utf-8")
            with urllib.request.urlopen(url, data=data) as res:
                html = json.loads(res.read().decode("utf-8"))
                print(html["result"])
                babymapid=html["result"]
            try:
                with connection.cursor() as cursor:
                    with connection.cursor() as cursor:
                        sql = "UPDATE `nursing_room` SET `babymap_place_id`=%s WHERE `id`=%s"
                        cursor.execute(sql, (str(babymapid),str(roomid)))
                        connection.commit()
            except:
                babymapid="0"
                pass
        except:
            babymapid="0"
            pass

    ##mac address fix id
    print(str(babymapid))

    if str(update_mode)=="0":
        print("update video")
        getvideodata(roomid)


    try:
        thread = threading.Thread(target=push_babymap_state, args=(str(babymapid),"0",))
        thread.start()
    except:
        pass

    try:
        with connection.cursor() as cursor:
            with connection.cursor() as cursor:
                sql = "INSERT INTO `nursing_room_state_time` (`nursing_room_id`,`state`,`update_time`) VALUES (%s,%s,NOW())"
                cursor.execute(sql, (str(roomid),str(0)))
                connection.commit()
    except:
        pass
    try:
        thread = threading.Thread(target=push_lock_state, args=(str(roomid),"1",firebase_state,))
        thread.start()
    except:
        pass

    main(sys.argv)
    #update video & video info
    #getvideodata(roomid)
