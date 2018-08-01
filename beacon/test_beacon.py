from bluetooth.ble import BeaconService
import time
import os
from threading import Timer
from datetime import datetime, timedelta, date
import logging
import traceback
import sys

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

class Beacon(object):

    def __init__(self, data, address):
        self._uuid = data[0]
        self._major = data[1]
        self._minor = data[2]
        self._power = data[3]
        self._rssi = data[4]
        self._address = address

    def __str__(self):
        # ret =""
        # if self._uuid=="UUID sensor":
        #     ret+="Sensor "
        # elif self._uuid=="UUID phone":
        #     ret+="User "
        #
        # firststep=int(self._major)
        # firststepvvv=format(firststep, '016b')
        # firststepvv=str(firststepvvv[8:16])+str(firststepvvv[0:8])
        # firststepv=firststepvv
        # cutstr=int(firststepv[0:6], 2)
        # cutstr1=int(firststepv[6:10], 2)
        # cutstr2=int(firststepv[10:16], 2)
        #
        # secondstep=int(self._minor)
        # secondstepvvv=format(secondstep, '016b')
        # secondstepvv=str(secondstepvvv[8:16])+str(secondstepvvv[0:8])
        # secondstepv=secondstepvv
        # cutstr3=int(secondstepv[0:4], 2)
        # cutstr4=int(secondstepv[4:12], 2)
        # cutstr5=int(secondstepv[12:16], 2)
        #
        # ret += "Beacon: address:{ADDR} uuid:{UUID} major:{MAJOR}"\
        #         " minor:{MINOR} txpower:{POWER} rssi:{RSSI} major data1:{DATA1} minor data2:{DATA2} weight:{d1} temperature:{d2} HB:{d3}"\
        #         .format(ADDR=self._address, UUID=self._uuid, MAJOR=self._major,
        #                 MINOR=self._minor, POWER=self._power, RSSI=self._rssi, DATA1=str(firststepv), DATA2=str(secondstepv),
        #                 d1=str(cutstr)+"."+str(cutstr1), d2=str(cutstr2)+"."+str(cutstr3), d3=str(cutstr4)+"."+str(cutstr5) )
        # self._weight =str(cutstr)+"."+str(cutstr1)
        # self._temperature =str(cutstr2)+"."+str(cutstr3)
        # self._HB =str(cutstr4)+"."+str(cutstr5)

        return self

def counter():
    nowdatetime=datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
    print(nowdatetime)
    try:
        with open(os.getcwd()+"/bluetooth_time.text", "w+") as f:
            f.write(str(nowdatetime)+"\n")
    except:
        print("write bluetooth time value text fail")
        pass

    try:
        devices = service.scan(2)
        height=""
        weight=""
        temperature=""
        heartrate=""


        for address, data in list(devices.items()):
            b = Beacon(data, address)
            #print(b.uuid)
            if b._uuid=="UUID sensor":
                #ret="babybed "
                firststep=int(b._major)
                firststepvvv=format(firststep, '016b')
                firststepvv=str(firststepvvv[8:16])+str(firststepvvv[0:8])
                firststepv=firststepvv
                cutstr=int(firststepv[0:6], 2)
                cutstr1=int(firststepv[6:10], 2)
                cutstr2=int(firststepv[10:16], 2)

                secondstep=int(b._minor)
                secondstepvvv=format(secondstep, '016b')
                secondstepvv=str(secondstepvvv[8:16])+str(secondstepvvv[0:8])
                secondstepv=secondstepvv
                cutstr3=int(secondstepv[0:4], 2)
                cutstr4=int(secondstepv[4:12], 2)
                cutstr5=int(secondstepv[12:16], 2)

                #weight=str(cutstr)+"."+str(cutstr1)

                #ret="weight:{d1} temperature:{d2} HB:{d3}".format(d1=str(cutstr)+"."+str(cutstr1), d2=str(cutstr2)+"."+str(cutstr3), d3=str(cutstr4)+"."+str(cutstr5) )
                #ret+="weight:{d1}".format(d1=str(cutstr)+"."+str(cutstr1) )
                #print(ret)
                ret1="Beacon: address:{ADDR} uuid:{UUID} major:{MAJOR}"\
                         " minor:{MINOR} txpower:{POWER} rssi:{RSSI} major data1:{DATA1} minor data2:{DATA2} weight:{d1} temperature:{d2} HB:{d3}"\
                         .format(ADDR=b._address, UUID=b._uuid, MAJOR=b._major,
                                 MINOR=b._minor, POWER=b._power, RSSI=b._rssi, DATA1=str(firststepv), DATA2=str(secondstepv),
                                 d1=str(cutstr)+"."+str(cutstr1), d2=str(cutstr2)+"."+str(cutstr3), d3=str(cutstr4)+"."+str(cutstr5) )
                print(ret1)
                weight=str(cutstr)+"."+str(cutstr1)
                temperature=str(cutstr2)+"."+str(cutstr3)
                heartrate=str(cutstr4)+"."+str(cutstr5)
                ret="weight:{d1} temperature:{d2} HB:{d3}".format(d1=str(weight), d2=str(temperature), d3=str(heartrate) )
                print(ret)

                #self.middleright.setText(ret)

            elif b._uuid=="UUID phone":
                #ret="User "
                firststep=int(b._major)
                firststepvvv=format(firststep, '016b')
                firststepvv=str(firststepvvv[8:16])+str(firststepvvv[0:8])
                firststepv=firststepvv
                cutstr=int(firststepv, 2)

                secondstep=int(b._minor)
                secondstepvvv=format(secondstep, '016b')
                secondstepvv=str(secondstepvvv[8:16])+str(secondstepvvv[0:8])
                secondstepv=secondstepvv
                cutstr3=int(secondstepv, 2)


                ret1="Beacon: address:{ADDR} uuid:{UUID} major:{MAJOR}"\
                         " minor:{MINOR} txpower:{POWER} rssi:{RSSI} major data1:{DATA1} minor data2:{DATA2} height int:{d1}"\
                         .format(ADDR=b._address, UUID=b._uuid, MAJOR=b._major,
                                 MINOR=b._minor, POWER=b._power, RSSI=b._rssi, DATA1=str(firststepv), DATA2=str(secondstepv),
                                 d1=str(cutstr)+"."+str(cutstr3) )
                print(ret1)
                height=str(cutstr)+"."+str(cutstr3)
                print(height)
        try:
            with open(os.getcwd()+"/beacon_value.text", "w+") as f:
                f.write(str(weight)+",")
                f.write(str(temperature)+",")
                f.write(str(heartrate)+",")
                f.write(str(height)+",")
        except:
            print("write value fail")
            pass

    except:
        print("restart bluetooth")
        #os.popen('sudo hciconfig hci0 reset')
        pass
    print("--------------------------------")

service = BeaconService()
if __name__ == "__main__":
    sys.excepthook = ExceptHookHandler(os.getcwd()+"/errorlog1.text")
    nowdatetime1=datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
    print(nowdatetime1)
    try:
        with open(os.getcwd()+"/bluetooth_timecheck.text", "a+") as f:
            f.write(str(nowdatetime1)+"\n")
    except:
        print("write bluetooth time value text fail")
        pass
    global rt
    rt = RepeatedTimer(3, counter) # it auto-starts, no need of rt.start()
