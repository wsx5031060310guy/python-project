import os
import threading
import time

def mamaroupdate(threadName):
    print("start checkcamera.py")
    os.system('python3 '+os.getcwd()+'/mamaro/mamaro_camera.py')

process_name= "mamaro_camera.py" # change this to the name of your process

tmp = os.popen("ps -Af").read()

if process_name not in tmp[:]:
    thread = threading.Thread(target=mamaroupdate, args=("Thread-7171",))
    thread.daemon = True                            # Daemonize thread
    thread.start()

time.sleep(4)
os._exit(1)
