import cv2
from datetime import datetime, timedelta, date
import os, shutil
import sys
import requests
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
import base64
from firebase import firebase
import serial
import time
import re, uuid

firebase_cam=firebase.FirebaseApplication("firebase url", None)

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

def capture_camera(mirror=True, size=None):
    """Capture video from camera"""
    # カメラをキャプチャする
    roomid=14
    try:
        with open(os.getcwd()+"/config.text", "r+") as f:
            data = f.readlines()
            lines=data[0].split(",")
            roomid=int(lines[0])
    except:
        pass
    print(str(roomid))
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
    except:
        print("get data for mac addr fix id fail")
        pass
    print(str(roomid))

    cap = cv2.VideoCapture(0) # 0はカメラのデバイス番号
    startTime = time.time()


    #print (delta.seconds)
    while True:
        # timeoutを秒で設定．ボーレートはデフォルトで9600．
        micorwave_state="0"
        try:
            with open(os.getcwd()+"/micorwave_value.text", "r+") as f:
                data = f.readlines()
                lines=data[0].split("\n")
                micorwave_state=lines[0]
        except:
            pass
        if micorwave_state=="1":
            # retは画像を取得成功フラグ
            ret, frame = cap.read()
            endTime = time.time()
            print ("time :", endTime - startTime)

            # 鏡のように映るか否か
            if mirror is True:
                frame = frame[:,::-1]

            # フレームをリサイズ
            # sizeは例えば(800, 600)
            if size is not None and len(size) == 2:
                frame = cv2.resize(frame, size)

            # フレームを表示する
            #cv2.imshow('camera capture', frame)
            #if endTime - startTime>=0.5:

            #date = now + datetime.timedelta(days = 1)
            tmpfolder=datetime.now().strftime('%Y%m%d')

            os.makedirs(os.getcwd()+"/cvvideo/"+str(tmpfolder), exist_ok=True)
            tmpfilename=datetime.now().strftime('%Y%m%d%H%M%S%f')
            cv2.imwrite(os.getcwd()+"/cvvideo/"+str(tmpfolder)+"/"+str(tmpfilename)+".jpg", frame)
            #upload file to firebase
            upload_blob( os.getcwd()+"/cvvideo/"+str(tmpfolder)+"/"+str(tmpfilename)+".jpg", str(tmpfilename)+".jpg")
            #upload value to firebase
            #https://firebasestorage.googleapis.com/v0/b/mamarocam.appspot.com/o/new_cool_image11111.jpg?alt=media&token=78f871b5-8188-434c-a0da-e737214c166d
            realtime_cam(str(roomid),"https://firebasestorage.googleapis.com/v0/b/storageBucket url/o/"+str(tmpfilename)+".jpg?alt=media&token=token key",firebase_cam)


            delete_folder()
            os.remove(os.getcwd()+"/cvvideo/"+str(tmpfolder)+"/"+str(tmpfilename)+".jpg")
            #cv2.SaveImage(os.getcwd()+"/cvvideo/"+str(tmpfilename)+".jpg",frame)
            startTime = time.time()
        else:
            ret, frame = cap.read()


    # while True:
    #     # retは画像を取得成功フラグ
    #     ret, frame = cap.read()
    #     camdatetime=datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
    #     d1 = datetime.strptime(camdatetime, '%Y-%m-%d %H:%M:%S:%f')
    #     d0 = datetime.strptime(nowdatetime, '%Y-%m-%d %H:%M:%S:%f')
    #     delta = d1 - d0
    #     # 鏡のように映るか否か
    #     if mirror is True:
    #         frame = frame[:,::-1]
    #
    #     # フレームをリサイズ
    #     # sizeは例えば(800, 600)
    #     if size is not None and len(size) == 2:
    #         frame = cv2.resize(frame, size)
    #
    #     # フレームを表示する
    #     cv2.imshow('camera capture', frame)
    #     if delta.seconds>=1:
    #
    #         #date = now + datetime.timedelta(days = 1)
    #         print(str(delta.seconds))
    #         tmpfolder=datetime.now().strftime('%Y%m%d')
    #
    #         os.makedirs(os.getcwd()+"/cvvideo/"+str(tmpfolder), exist_ok=True)
    #         tmpfilename=datetime.now().strftime('%Y%m%d%H%M%S%f')
    #         cv2.imwrite(os.getcwd()+"/cvvideo/"+str(tmpfolder)+"/"+str(tmpfilename)+".jpg", frame)
    #         #upload file to firebase
    #         upload_blob( os.getcwd()+"/cvvideo/"+str(tmpfolder)+"/"+str(tmpfilename)+".jpg", str(tmpfilename)+".jpg")
    #         #upload value to firebase
    #         #https://firebasestorage.googleapis.com/v0/b/mamarocam.appspot.com/o/new_cool_image11111.jpg?alt=media&token=78f871b5-8188-434c-a0da-e737214c166d
    #         realtime_cam(str(roomid),"https://firebasestorage.googleapis.com/v0/b/mamarocam.appspot.com/o/"+str(tmpfilename)+".jpg?alt=media&token=78f871b5-8188-434c-a0da-e737214c166d",firebase_cam)
    #
    #
    #         delete_folder()
    #         os.remove(os.getcwd()+"/cvvideo/"+str(tmpfolder)+"/"+str(tmpfilename)+".jpg")
    #         #cv2.SaveImage(os.getcwd()+"/cvvideo/"+str(tmpfilename)+".jpg",frame)
    #         nowdatetime=datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
    #
    #     k = cv2.waitKey(1) # 1msec待つ
    #     if k == 27: # ESCキーで終了
    #         break

    # キャプチャを解放する
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    cred = credentials.Certificate(os.getcwd()+'/key/key.json')
    firebase_admin.initialize_app(cred, {
        'storageBucket': 'storageBucket url'
    })
    capture_camera()
