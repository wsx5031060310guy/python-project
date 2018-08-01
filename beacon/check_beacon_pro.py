import os
import threading
import time

def mamaroupdate(threadName):
    print("start check_beacon.py")
    os.system('sudo python3 '+os.getcwd()+'/check_beacon.py')

process_name= "check_beacon.py" # change this to the name of your process

tmp = os.popen("ps -Af").read()

if process_name not in tmp[:]:
    thread = threading.Thread(target=mamaroupdate, args=("Thread-711",))
    thread.daemon = True                            # Daemonize thread
    thread.start()

time.sleep(4)
os._exit(1)
