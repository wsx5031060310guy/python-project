import pyrebase
import json
from datetime import datetime, timedelta, date

config = {
  "apiKey": None,
  "authDomain": None,
  "databaseURL": "firebase url",
  "storageBucket": None
}
id=39
firebase = pyrebase.initialize_app(config)
db = firebase.database()
#all_users = db.child("grid_eye/14").order_by_key().limit_to_first(3).get()
#all_users = db.child("grid_eye").child("39").child().order_by_child("time").limit_to_last(20).get()
#all_users = db.child("grid_eye").child("39").child().order_by_child("time").equal_to("2018-06-25").limit_to_first(20).get()
all_users = db.child("grid_eye").child(str(id)).child().order_by_child("time").get()
nowdatetime=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
cou=0
recou=0
kecou=0
for user in all_users.each():
    cou+=1
    #print(user.key())
    d = json.dumps(user.val())
    decoded = json.loads(d)
    print(decoded["time"])
    d0 = datetime.strptime(nowdatetime, '%Y-%m-%d %H:%M:%S')
    d1 = datetime.strptime(decoded["time"], '%Y-%m-%d %H:%M:%S')
    delta = d0 - d1
    print (delta.days)
    if delta.days>2:
        db.child("grid_eye").child(str(id)).child(user.key()).remove()
        print("delete "+str(user.key()))
        recou+=1
    else:
        print("keep "+str(user.key()))
        kecou+=1


nowdatetime1=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
d0 = datetime.strptime(nowdatetime1, '%Y-%m-%d %H:%M:%S')
d1 = datetime.strptime(nowdatetime, '%Y-%m-%d %H:%M:%S')
delta = d0 - d1
totaltime=float(delta.seconds)
hour=0
min=0
sec=0
if totaltime>0:
    sec=totaltime%60
    min=int(totaltime/60)
    hour=int(min/60)
    min-=(hour*60)




print ("use time (second) : "+str(delta.seconds))
print ("use time H:M:S => "+str(hour)+":"+str(min)+":"+str(sec))

print("total data : "+str(cou))
print("remove data : "+str(recou))
print("keep data : "+str(kecou))
print("finished checking id:"+str(id)+"!")
    # for user1 in user.val():
    #     print(user1)
        # if str(user1)=='time':
        #     print(user1.key())
        #     print(user1.val())
    # print(user.key())
    # print(user.val())
    #db.child("grid_eye").child(str(id)).child(user.key()).remove()
