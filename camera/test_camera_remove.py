import multiprocessing as mp
import pymysql.cursors
import pyrebase
import json
from datetime import datetime, timedelta, date
import time
import os
import sys
import requests
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
import base64
from firebase import firebase

cred = credentials.Certificate(os.getcwd()+'/key/key.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'storageBucket url'
})
global connection
connection=None
try:
    connection = pymysql.connect(host='host',
    user='username',
    password='password',
    db='db name',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor)
except:
    print("connect fail")
    connection=None
    pass

config = {
  "apiKey": None,
  "authDomain": None,
  "databaseURL": "firebase url",
  "storageBucket": None
}
firebase = pyrebase.initialize_app(config)
db = firebase.database()


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

def checking_mamaro(id):
    ress=""
    try:
        all_users = db.child("camera").child(str(id)).child().order_by_child("time").limit_to_first(1).get()
        nowdatetime=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cou=0
        recou=0
        kecou=0
        check=False
        for user in all_users.each():
            #print(user.key())
            d = json.dumps(user.val())
            decoded = json.loads(d)
            #print(decoded["time"])
            d0 = datetime.strptime(nowdatetime, '%Y-%m-%d %H:%M:%S')
            d1 = datetime.strptime(decoded["time"], '%Y-%m-%d %H:%M:%S')
            delta = d0 - d1
            #print (delta.days)
            if delta.days>7:
                check=True
                break
            else:
                check=False
                break
        if check:
            all_users = db.child("camera").child(str(id)).child().order_by_child("time").limit_to_first(2).get()
            for user in all_users.each():
                cou+=1
                #print(user.key())
                d = json.dumps(user.val())
                decoded = json.loads(d)
                #print(decoded["time"])
                d0 = datetime.strptime(nowdatetime, '%Y-%m-%d %H:%M:%S')
                d1 = datetime.strptime(decoded["time"], '%Y-%m-%d %H:%M:%S')
                delta = d0 - d1
                #print (delta.days)
                if delta.days>7:
                    # print(decoded["imgurl"])
                    finstr=str(decoded["imgurl"])
                    startind=finstr.rfind('/')
                    endind=finstr.rfind('?')
                    # print(startind)
                    # print(endind)
                    # print(str(finstr[startind+1:endind]))
                    delete_blob( str(finstr[startind+1:endind]))
                    db.child("camera").child(str(id)).child(user.key()).remove()
                    #print("delete "+str(user.key()))
                    recou+=1
                else:
                    #print("keep "+str(user.key()))
                    break
            ress="id:"+str(id)+","+"total:"+str(cou)+","+"delete:"+str(recou)
        else:
            ress="id:"+str(id)+",not need to delete!"

    except:
        ress="id:"+str(id)+",fail checking."
    return ress

def multicore():
    startTime = time.time()
    pool = mp.Pool()
    idarr=[]
    with connection.cursor() as cursor:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `nursing_room`"
            cursor.execute(sql)
            result = cursor.fetchall()
            for res in result:
                idarr.append(res['id'])
    print(idarr)
    res = pool.map(checking_mamaro,idarr )
    for i in range(0,len(res)):
        print(res[i])
    #print(str(res))
    pool.close()
    pool.join()
    endTime = time.time()
    print ("time :", endTime - startTime)

    totaltime=endTime - startTime
    hour=0
    min=0
    sec=0
    if totaltime>0:
        sec=int(totaltime%60)
        min=int(totaltime/60)
        hour=int(min/60)
        min-=int(hour*60)
    print ("use time H:M:S => "+str(hour)+":"+str(min)+":"+str(sec))

if __name__ == "__main__":
    multicore()
