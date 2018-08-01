import time
import os
from threading import Timer
from datetime import datetime, timedelta, date
import logging
import traceback
import sys
import threading

def testblue(threadName):
    print("start testblue3.py")
    os.system('sudo python3 '+os.getcwd()+'/test_beacon.py')

class ExceptHookHandler(object):
    ## @detail 构造函数
    #  @param logFile: log的输入地址
    #  @param mainFrame: 是否需要在主窗口中弹出提醒
    def __init__(self, logFile, mainFrame = None):
        self.__LogFile = logFile
        self.__MainFrame = mainFrame

        self.__Logger = self.__BuildLogger()
        #重定向异常捕获
        sys.excepthook = self.__HandleException

    ## @detail 创建logger类
    def __BuildLogger(self):
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        logger.addHandler(logging.FileHandler(self.__LogFile))
        return logger

    ## @detail 捕获及输出异常类
    #  @param excType: 异常类型
    #  @param excValue: 异常对象
    #  @param tb: 异常的trace back
    def __HandleException(self, excType, excValue, tb):
        # first logger
        try:
            currentTime = datetime.datetime.now()
            self.__Logger.info('Timestamp: %s'%(currentTime.strftime("%Y-%m-%d %H:%M:%S")))
            self.__Logger.error("Uncaught exception：", exc_info=(excType, excValue, tb))
            self.__Logger.info('\n')
        except:
            pass

        # then call the default handler
        sys.__excepthook__(excType, excValue, tb)

        err_msg = ''.join(traceback.format_exception(excType, excValue, tb))
        err_msg += '\n Your App happen an exception, please contact administration.'
        print(err_msg)
        # Here collecting traceback and some log files to be sent for debugging.
        # But also possible to handle the error and continue working.
        # dlg = wx.MessageDialog(None, err_msg, 'Administration', wx.OK | wx.ICON_ERROR)
        # dlg.ShowModal()
        # dlg.Destroy()


class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False
global cou
cou=0
def counter():
    global cou
    nowdatetime=datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
    print(nowdatetime)

    process_name= "test_beacon.py" # change this to the name of your process

    tmp = os.popen("ps -Af").read()

    if process_name not in tmp[:]:
        thread = threading.Thread(target=testblue, args=("Thread-999",))
        thread.daemon = True                            # Daemonize thread
        thread.start()

    try:
        nowdatetime=datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
        with open(os.getcwd()+"/bluetooth_time.text", "r+") as f:
            data = f.readlines()
            lines=data[0].split("\n")
            checktime=datetime.strptime(lines[0], '%Y-%m-%d %H:%M:%S:%f')
            print(str(checktime))
            checktime=datetime.strptime(lines[0], '%Y-%m-%d %H:%M:%S:%f')
            delta = datetime.now() - checktime

            print(str(delta.seconds))
            if delta.seconds>30:
                print("timeout restart test_beacon.py")
                cou=0
                os.popen('sudo service bluetooth restart')
                os.popen('sudo kill -9 `pgrep -f test_beacon.py`')
                try:
                    with open(os.getcwd()+"/bluetooth_time.text", "w+") as f:
                        f.write(str(nowdatetime)+"\n")
                except:
                    print("write bluetooth time value text fail")
                    pass


        # try:
        #     with open(os.getcwd()+"/bluetooth_time.text", "r+") as f:
        #         data = f.readlines()
        #         lines=data[0].split("\n")
        #         checktime=datetime.strptime(lines[0], '%Y-%m-%d %H:%M:%S')
        #         print(str(checktime))
        #
        # except:
        #     pass

        # with open(os.getcwd()+"/bluetooth_time.text", "w+") as f:
        #     f.write(nowdatetime+"\n")
    except:
        print("check bluetooth time fail")
        cou+=1
        #os.popen('sudo hciconfig hci0 reset')
        #os.popen('sudo service bluetooth restart')
        pass
    if cou>9:
        print("timeout restart test_beacon.py")
        cou=0
        os.popen('sudo service bluetooth restart')
        os.popen('sudo kill -9 `pgrep -f test_beacon.py`')

    print("--------------------------------")

if __name__ == "__main__":
    sys.excepthook = ExceptHookHandler(os.getcwd()+"/errorlog2.text")
    global rt
    rt = RepeatedTimer(3, counter) # it auto-starts, no need of rt.start()
