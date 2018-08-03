import os
from tkinter import*
import time
import threading

root = Tk()

def topcontent(threadName,delay):
    time.sleep(delay)
    print("start videocover")
    os.system('python3 '+os.getcwd()+'/mamaro/videocover.py')
def webb(threadName):
    print("start videoplayerloop")
    os.system('python3 '+os.getcwd()+'/mamaro/videoplayerloop.py')

def current_position():
    return [root.winfo_pointerx(), root.winfo_pointery()]

pos1 = current_position()
coubabybed=0
couQA1=0
coumain=0
couweb=0
while True:
    try:
        time.sleep(0.5)
        pos2 = current_position()
        if not pos1 == pos2:
            # run a command:
            print("action!")
            coubabybed=0
            couQA1=0
            coumain=0
            couweb=0
        else:
            process_name= "QA1.py" # change this to the name of your process

            tmp = os.popen("ps -Af").read()

            if process_name in tmp[:]:
                couQA1+=1
                coubabybed=0
                coumain=0
                couweb=0
                if couQA1==20:
                    print("kill QA1!")
                    os.system("sudo kill -9 `pgrep -f QA1.py`")
                    couQA1=16
            else:
                process_name2= "testblueview1.py" # change this to the name of your process

                tmp2 = os.popen("ps -Af").read()

                if process_name2 in tmp2[:]:
                    couQA1=0
                    coubabybed+=1
                    coumain=0
                    couweb=0
                    if coubabybed==125:
                        print("kill testblueview1!")
                        os.system("sudo kill -9 `pgrep -f testblueview1.py`")
                        coubabybed=110
                else:

                    process_name1= "mainview.py" # change this to the name of your process

                    tmp1 = os.popen("ps -Af").read()

                    if process_name1 in tmp1[:]:
                        couQA1=0
                        coubabybed=0
                        process_name3= "chrome" # change this to the name of your process

                        tmp3 = os.popen("ps -Af").read()

                        if process_name3 not in tmp3[:]:

                            coumain+=1
                            if coumain==200:
                                print("kill mainview!")
                                os.system("sudo kill -9 `pgrep -f mainview.py`")
                                coumain=196

                                process_name2= "videoplayerloop.py" # change this to the name of your process

                                tmp2 = os.popen("ps -Af").read()

                                if process_name2 not in tmp2[:]:
                                    print("start videoplayerloop")
                                    thread = threading.Thread(target=webb, args=("Thread-2",))
                                    thread.daemon = True                            # Daemonize thread
                                    thread.start()

                                process_name2= "videocover.py" # change this to the name of your process

                                tmp2 = os.popen("ps -Af").read()

                                if process_name2 not in tmp2[:]:
                                    print("start videocover")
                                    thread1 = threading.Thread(target=topcontent, args=("Thread-1",2,))
                                    thread1.daemon = True                            # Daemonize thread
                                    thread1.start()
                        else:
                            couweb+=1
                            if couweb==200:
                                print("kill chrome!")
                                os.system("sudo kill -9 `pgrep -f chrome`")
                                print("kill window!")
                                os.system("sudo kill -9 `pgrep -f window.py`")
                                couweb=196





                # print ("start timeout.py")
                # thread = threading.Thread(target=timeout, args=("Thread-8",))
                # thread.daemon = True                            # Daemonize thread
                # thread.start()

        pos1 = pos2
    except:
        print('Close button pressed')
        os._exit(1)

root.mainloop()
