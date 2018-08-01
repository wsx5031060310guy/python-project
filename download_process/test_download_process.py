import requests
import os
import sys
from datetime import datetime, timedelta, date
import time
import pymysql.cursors


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

link = "mp4 url"
file_name = os.getcwd()+"/video/test.mp4"
room_id=38
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

update_log(room_id, "start update video", "0")

startTime = time.time()
with open(file_name, "wb") as f:
    update_log(room_id, "start download test.mp4", "0")

    update_log(room_id, "2,0", "2")
    print ("Downloading %s" % file_name)

    response = requests.get(link, stream=True)
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
            update_log(room_id, str("2")+","+str("test.mp4")+","+str(dl)+","+str(total_length)+","+str(percent), "1")
        endTime = time.time()
        nowdatetime=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(nowdatetime)
        update_log(room_id, "end download test.mp4", "0")
        update_log(room_id, "2,1", "2")


endTime = time.time()
print ("time :", str(int(endTime - startTime)),"sec")
update_log(room_id, "end update video", "0")
update_log(room_id, "use "+str(int(endTime - startTime))+" second", "0")

                # sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)) )
                # sys.stdout.flush()
