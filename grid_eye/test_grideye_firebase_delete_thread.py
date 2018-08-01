import multiprocessing as mp
import pymysql.cursors
import pyrebase
import json
from datetime import datetime, timedelta, date
import time

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


def checking_mamaro(id):
    ress=""
    try:
        all_users = db.child("grid_eye").child(str(id)).child().order_by_child("time").limit_to_first(1).get()
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
            all_users = db.child("grid_eye").child(str(id)).child().order_by_child("time").limit_to_first(2).get()
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
                    db.child("grid_eye").child(str(id)).child(user.key()).remove()
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
    #print(res)

    # for i in range(0,len(idarr)):
    #     print(idarr[i])
    #     res = pool.map(checking_mamaro,str(idarr[i]) )
    #     print(res)


if __name__ == '__main__':
    multicore()
