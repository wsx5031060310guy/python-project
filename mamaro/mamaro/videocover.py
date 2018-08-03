import os
import sys
import tkinter
import threading
import time
import requests
import urllib.request

def check_internet():
    url='http://www.google.com/'
    try:
        urllib.request.urlopen(url, timeout=1)
        return True
    except urllib.request.URLError as err:
        return False

def callback(event):
    frame.focus_set()
    print("clicked at", event.x, event.y)
    thread = threading.Thread(target=webb, args=("Thread-99",))
    thread.daemon = True                            # Daemonize thread
    thread.start()
    time.sleep(4)
    os._exit(1)
def webb(threadName):
    if check_internet():
        print("open mainview")
        os.system('python3 '+os.getcwd()+'/mamaro/mainview.py')
    else:
        print("start no internet")
        os.system('python3 '+os.getcwd()+'/mamaro/nointernet.py')
    # time.sleep(1)
    print("kill videoplayerloop")
    os.system("sudo kill -9 `pgrep -f videoplayerloop.py`")
    # time.sleep(1)
    # print("kill vlc")
    # os.system("sudo kill -9 `pgrep -f vlc`")





root=tkinter.Tk()
root.wait_visibility(root)
root.wm_attributes('-alpha',0)
root.geometry("1920x1080+0+0")
frame = tkinter.Frame(root, width=1920, height=1080)
frame.bind("<Button-1>", callback)
frame.pack()
root.overrideredirect(True)
root.overrideredirect(False)
root.attributes("-fullscreen",True)
root.mainloop()
