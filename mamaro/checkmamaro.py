import os
import threading
import time

def mamaroupdate(threadName):
    print("kill checkmouse")
    os.system("sudo kill -9 `pgrep -f checkmouse.py`")
    time.sleep(1)
    print("kill chrome")
    os.system("sudo kill -9 `pgrep -f chrome`")
    time.sleep(1)
    print("start mamaro_update")
    os.system('python3 '+os.getcwd()+'/mamaro_update.py')

process_name= "mamaro_update.py" # change this to the name of your process

tmp = os.popen("ps -Af").read()

if process_name not in tmp[:]:
    thread = threading.Thread(target=mamaroupdate, args=("Thread-789",))
    thread.daemon = True                            # Daemonize thread
    thread.start()

time.sleep(4)
os._exit(1)
