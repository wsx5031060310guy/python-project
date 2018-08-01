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

db.child("grid_eye").child(str(id)).remove()
print("finished delete id:"+str(id)+" grid-eye data!")
