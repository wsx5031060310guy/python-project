import os
import urllib
import sys
from requests import get  # to make GET request
import vlc
import operator
import tkinter
import pymysql.cursors
import requests
import urllib.request

def download(url, file_name):
    # open in binary mode
    with open(file_name, "wb") as file:
        # get request
        response = get(url)
        # write to file
        file.write(response.content)

def myVideo(url):
    flag = 0  #flag for checking if the file in present in the memory.
    search_folder = "./video"
    videoFile = url.split('/')[-1].split('#')[0].split('?')[0] #stripping the name of the file.
    print(videoFile)
    for root, dirs, files in os.walk(search_folder): # using the os.walk module to find the files.
        for name in files:
            print(name)
            """Checking the videofile in the current directory and the sub-directories"""
            if videoFile == os.path.join(name):  #checking if the file is already present in the internal memory.(Traverse through subdirectories as well)
                flag += 1
                print("The file is already present in the internal memory")
                return -1  # Returning the confirmation that the file is present.

            if flag == 0: # dowiloding only when the flag is zero(i.e the file is not in the internal memory.)
                print("Downloading the file")
                curDir = os.getcwd()   # getting the current working directory.
                fullVideoPath = os.path.join(curDir,videoFile)  # Making the full path of the video file.
                download(url, fullVideoPath)
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
        print("videoplayerloop insert video play time fail")
        pass


class video_info(object):
    """__init__() functions as the class constructor"""
    def __init__(self, playindex=None, filename=None, DBindex=None, check=None):
        self.playindex = playindex
        self.filename = filename
        self.DBindex = DBindex
        self.check=check

def check_internet():
    url='http://www.google.com/'
    try:
        urllib.request.urlopen(url, timeout=1)
        return True
    except urllib.request.URLError as err:
        return False

def closeEvent():
    #Your desired functionality here
    print('Close button pressed')
    os._exit(1)

roomid=14
readcheck=True
playlist=[]
sorted_x=[]
totalfile=0
oneloopindex=1
totalindexx=1
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
                    #print(lin)
            # print(lines)
            # for line in lines:
            #     print(line)

            #playlist.append(video_info(res['company_icon'],res['company_name'],res['company_des'],res['company_url']))
            #total=int(lines[0])

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

    # for i in range(len(playlist)):
    #     print(playlist[i].playindex)
    #     print(playlist[i].filename)
    #     print(playlist[i].DBindex)

    sorted_y = sorted(playlist, key=operator.attrgetter('playindex'))
    search_folder = os.getcwd()+"/mamaro/video"
    localcou=0
    localvideo=[]
    sorted_x=[]
    for i in range(len(sorted_y)):
        sorted_y[i].check=False
        if int(sorted_y[i].playindex)>int(oneloopindex):
            sorted_x.append(sorted_y[i])
    for root, dirs, files in os.walk(search_folder): # using the os.walk module to find the files.
        for name in files:
            localcou+=1
            localvideo.append(os.path.join(name))
            for i in range(len(sorted_x)):
                if sorted_x[i].filename == os.path.join(name):
                    sorted_x[i].check=True
            """Checking the videofile in the current directory and the sub-directories"""

    instance = vlc.Instance()
    media_ply = instance.media_player_new()
    media_ply.set_fullscreen(True)
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
        with open(os.getcwd()+"/mamaro/playindex.text", "r+") as f:
            data = f.readlines()
            lines=data[0].split()
            totalindexx=int(lines[0])

    except:
        with open(os.getcwd()+"/mamaro/playindex.text","w"): pass
        pass

    try:
        with open(os.getcwd()+"/mamaro/playindex.text", "w+") as f:
            f.write(str(totalindexx)+"\n")
    except:
        pass

    insertdata(sorted_x[cou].DBindex,sorted_x[cou].playindex,totalindexx)
    media_ply.set_mrl(strings2[cou])
    cou+=1
    totalindexx+=1
    media_ply.play()
    print(media_ply.get_state())


    while True:
        try:
            media_ply.set_fullscreen(True)
            if media_ply.get_state() == vlc.State.Playing:
                pass
            if media_ply.get_state() == vlc.State.Ended:
                if cou != len(strings2):
                    print(cou)
                    try:
                        with open(os.getcwd()+"/mamaro/playindex.text", "w+") as f:
                            f.write(str(totalindexx)+"\n")
                    except:
                        pass
                    insertdata(sorted_x[cou].DBindex,sorted_x[cou].playindex,totalindexx)
                    media_ply.set_mrl(strings2[cou])
                    cou+=1
                    totalindexx+=1
                    media_ply.play()
                else:
                    #print("end")
                    cou=0
                    print(cou)
                    try:
                        with open(os.getcwd()+"/mamaro/playindex.text", "w+") as f:
                            f.write(str(totalindexx)+"\n")
                    except:
                        pass
                    insertdata(sorted_x[cou].DBindex,sorted_x[cou].playindex,totalindexx)
                    media_ply.set_mrl(strings2[cou])
                    cou+=1
                    totalindexx+=1
                    media_ply.play()
        except KeyboardInterrupt:
            # clean up
            raise
