import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import pymysql.cursors
import urllib.request, json
import requests
import os
import threading
import time
from datetime import datetime, timedelta, date

def db_execute(query,sqlpar):
    res=None
    try:
        connection = pymysql.connect(host='host',
        user='username',
        password='password',
        db='DBname',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor)

        with conn.cursor() as cursor:
            with conn.cursor() as cursor:
                sql = query
                if sqlpar is not None:
                    cursor.execute(sql, sqlpar)
                    res = cursor.fetchall()
                else:
                    cursor.execute(sql)
                    res = cursor.fetchall()
    except:
        pass

    return res


def db_execute_insert(query,sqlpar):
    res=None
    try:
        connection = pymysql.connect(host='host',
        user='username',
        password='password',
        db='DBname',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor)

        with conn.cursor() as cursor:
            with conn.cursor() as cursor:
                sql = query
                if sqlpar is not None:
                    cursor.execute(sql, sqlpar)
                    conn.commit()
                    res=True
                else:
                    cursor.execute(sql)
                    conn.commit()
                    res=True
    except:
        pass

    return res



def check_internet():
    url='http://www.google.com/'
    try:
        urllib.request.urlopen(url, timeout=1)
        return True
    except urllib.request.URLError as err:
        return False


def send_email(email, message, title):
    # me == my email address
    # you == recipient's email address
    me = "me.com"
    you = email
    gmail_user = 'who.com'
    gmail_password = 'password'

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = title
    msg['From'] = me
    msg['To'] = you

    # Create the body of the message (a plain-text and an HTML version).
    #text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttp://www.python.org"
    html=message
    # html = """\
    # <html>
    #   <head></head>
    #   <body>
    #     <p>Hi!<br>
    #        How are you?<br>
    #        Here is the <a href="http://www.python.org">link</a> you wanted.
    #     </p>
    #   </body>
    # </html>
    # """

    # Record the MIME types of both parts - text/plain and text/html.
    #part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    #msg.attach(part1)
    msg.attach(part2)

    # Send the message via local SMTP server.
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_password)
    server.sendmail(me, you, msg.as_string())
    server.close()
    print('Email sent!')

class mamaro_info(object):
    """__init__() functions as the class constructor"""
    def __init__(self, id=None, name=None):
        self.id = id
        self.name = name

class video_info(object):
    """__init__() functions as the class constructor"""
    def __init__(self, id=None, company_name=None, video_des=None, video_state=None):
        self.id = id
        self.company_name = company_name
        self.video_des = video_des
        self.video_state = video_state

class mamaro_wifi_maxtime(object):
    """__init__() functions as the class constructor"""
    def __init__(self, nursing_room_id=None, maxtime=None):
        self.nursing_room_id = nursing_room_id
        self.maxtime = maxtime

class mamaro_wifi_content(object):
    """__init__() functions as the class constructor"""
    def __init__(self, id=None, update_time=None, name=None, address=None, GPS_lat=None, GPS_lng=None, company=None, company_tel=None, nursing_room_id=None):
        self.id = id
        self.update_time = update_time
        self.name = name
        self.address = address
        self.GPS_lat = GPS_lat
        self.GPS_lng = GPS_lng
        self.company = company
        self.company_tel = company_tel
        self.nursing_room_id = nursing_room_id

def getlogdata(nowdate):
    global checkupdatelog
    #get data
    idlist=[]
    checkupdatelog=False
    if check_internet():
        body="<html><head></head><body><h1>video state list</h1>"
        body1="<html><head></head><body><h1>video log list</h1>"
        sql = "SELECT * FROM `nursing_room` WHERE `close`=%s"
        result =db_execute(sql, ("0",))
        if result is not None:
            for res in result:
                idlist.append(mamaro_info(res['id'],res['name']))

        for i in range(len(idlist)):
            checklist=[]
            #get video list from DB
            sql = "SELECT b.id,b.company_name,b.video_des FROM `nursing_room_connect_video` as a inner join `nursing_room_video_info` as b on a.nursing_room_video_info_id=b.id WHERE a.`nursing_room_id`=%s"
            result =db_execute(sql, (str(idlist[i].id),))
            if result is not None:
                for res in result:
                    checklist.append(video_info(res['id'],res['company_name'],res['video_des'],False))

            print(idlist[i].id)
            print("----------------")
            for ii in range(len(checklist)):
                print(checklist[ii].video_state)
            #print(checklist[0].company_name)
            #get play config log
            playconfiglist=[]
            sql = "SELECT * FROM `nursing_room_log` WHERE `nursing_room_id`=%s and `type`=%s and `update_time` BETWEEN %s AND %s"
            result =db_execute(sql,(str(idlist[i].id),str("3"),str(nowdate)+" 00:00:00",str(nowdate)+" 23:59:59",))
            if result is not None:
                for res in result:
                    playconfiglist.append(res['log'])
            ##get video state
            checkdata=False
            sql = "SELECT * FROM `nursing_room_log` WHERE `nursing_room_id`=%s and `type`=%s and `update_time` BETWEEN %s AND %s"
            result =db_execute(sql,(str(idlist[i].id),str("2"),str(nowdate)+" 00:00:00",str(nowdate)+" 23:59:59",))
            if result is not None:
                for res in result:
                    checkdata=True
                    liner=res['log'].split(",")
                    print(liner[1])
                    for ii in range(len(checklist)):
                        if str(checklist[ii].id)==str(liner[0]):
                            if str(liner[1])=="1":
                                checklist[ii].video_state=True

            body+="<hr><h1>"+str(idlist[i].name)+"</h1>"
            body1+="<hr><h1>"+str(idlist[i].name)+"</h1>"
            body+="<h2>Play List:</h2>"
            for ii in range(len(playconfiglist)):
                print(playconfiglist[ii])
                body+="<h3>"+str(playconfiglist[ii])+"</h3>"

            if checkdata:
                for ii in range(len(checklist)):
                    print(checklist[ii].video_state)
                    if checklist[ii].video_state:
                        body+="<div style='background-color:lightgreen;height:auto;width:100%;'>"
                        body+="<h2>ID:"+str(checklist[ii].id)+"</h2>"
                        body+="<h2>company name:"+str(checklist[ii].company_name)+"</h2>"
                        body+="<h2>video des:"+str(checklist[ii].video_des)+"</h2>"
                        body+="<h2>video state:"+str(checklist[ii].video_state)+"</h2>"
                        body+="</div>"
                    else:
                        body+="<div style='background-color:lightred;height:auto;width:100%;'>"
                        body+="<h2>ID:"+str(checklist[ii].id)+"</h2>"
                        body+="<h2>company name:"+str(checklist[ii].company_name)+"</h2>"
                        body+="<h2>video des:"+str(checklist[ii].video_des)+"</h2>"
                        body+="<h2>video state:"+str(checklist[ii].video_state)+"</h2>"
                        body+="</div>"
            else:
                body+="<h2>NO DATA</h2>"

            ##get video detail log
            checklog=False
            sql = "SELECT * FROM `nursing_room_log` WHERE `nursing_room_id`=%s and `type`<%s and `update_time` BETWEEN %s AND %s"
            result =db_execute(sql,(str(idlist[i].id),str("2"),str(nowdate)+" 00:00:00",str(nowdate)+" 23:59:59",))
            if result is not None:
                for res in result:
                    checklog=True
                    print(res['log'])
                    body1+="<h3>"+str(res['update_time'])+"</h3>"
                    body1+="<h3>"+str(res['log'])+"</h3>"

            if checklog==False:
                body1+="<h2>NO DATA</h2>"

        body+= "<hr></body></html>"
        body1+="<hr></body></html>"
        send_email("who.com",body , "update video state")
        send_email("who.com",body1 , "update video log")

def convert_timedelta(duration):
    days, seconds = duration.days, duration.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 60)
    return hours, minutes, seconds
#{" + '"' + "text" + '"' + ":" + '"' + "Please Check Customer" + '"' + "," + '"' + "response_type" + '"' + ":" + '"' + "in_channel" + '"' + "," + '"' + "title" + '"' + ":" + '"' + "Check Door View" + '"' + "," + '"' + "title_link" + '"' + ":" + '"' + urlp + '"' + " }
def send_to_slack(message,title):
    url = "https://slack.com/api/chat.postMessage"
    data = {
        "token" : "token",
        "channel" : "channel",
        "as_user" : "false",
        "username" : "test",
        "text" : str(title),
        "icon_url" : "img url",
        "attachments" : "["+str(message)+"]"
        }
    try:
        data = urllib.parse.urlencode(data).encode("utf-8")
        with urllib.request.urlopen(url, data=data) as res:
            html = json.loads(res.read().decode("utf-8"))
            print(html["result"])
            res=html["result"]

    except:
        pass


def send_to_company(email, subbody):
    # me == my email address
    # you == recipient's email address
    me = "me.com"
    you = email
    gmail_user = 'who.com'
    gmail_password = 'password'

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "【】"
    msg['From'] = me
    msg['To'] = you

    body = ""
    body += "<table width='100%'>"
    body += "<tr>"
    body += "<td width='20%' height='10%'>"
    body += "</td>"
    body += "<td width='60%' height='10%'>"
    body += "</td>"
    body += "<td width='20%' height='10%'>"
    body += "</td>"
    body += "</tr>"
    body += "<tr>"
    body += "<td width='10%'>"
    body += "</td>"
    body += "<td width='70%'>"
    body += "<table width='100%'>"
    body += "<tr>"
    body += "<td height='50px' valign='bottom'>"
    body += "<a style='font-size: 15pt;text-decoration: none;color: #F88787;' href=''>"
    body += "<img alt='' title='' height='auto' src='' style='border:none;display:block;outline:none;text-decoration:none;width:400px;height:auto' width='180'></a><br/><br/>"
    body += "</td>"
    body += "</tr>"
    body += "<tr>"
    body += "<td>"
    body += "<span STYLE='font-size: 15pt;'>現在 "+subbody+" において</span><br/>"
    body += "<span STYLE='font-size: 15pt;'>利用されています。</span><br/>"

    body += "<span STYLE='font-size: 15pt;'></span><br/>"
    body += "<span STYLE='font-size: 15pt;'></span><br/><br/>"
    body += "<span STYLE='font-size: 15pt;'></span><br/>"

    body += "</td>"
    body += "</tr>"
    body += "<tr>"
    body += "<td align='center'>"
    body += "</td>"
    body += "</tr>"
    body += "<tr>"
    body += "<td>"
    body += "</td>"
    body += "</tr>"
    body += "</table>"
    body += "</td>"
    body += "<td width='20%'>"
    body += "</td>"
    body += "</tr>"
    body += "<tr>"
    body += "<td width='20%' height='10%'>"
    body += "</td>"
    body += "<td width='60%' height='10%'>"
    body += "</td>"
    body += "<td width='20%' height='10%'>"
    body += "</td>"
    body += "</tr>"
    body += "</table>"

    html=body

    part2 = MIMEText(html, 'html')


    msg.attach(part2)

    # Send the message via local SMTP server.
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_password)
    server.sendmail(me, you, msg.as_string())
    server.close()
    print('Email sent!')

def send_to_myself(email, subbody,title):
    # me == my email address
    # you == recipient's email address
    me = "me.com"
    you = email
    gmail_user = 'who.com'
    gmail_password = 'password'

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = title
    msg['From'] = me
    msg['To'] = you

    body = ""
    body += "<table width='100%'>"
    body += "<tr>"
    body += "<td width='20%' height='10%'>"
    body += "</td>"
    body += "<td width='60%' height='10%'>"
    body += "</td>"
    body += "<td width='20%' height='10%'>"
    body += "</td>"
    body += "</tr>"
    body += "<tr>"
    body += "<td width='20%'>"
    body += "</td>"
    body += "<td width='60%'>"
    body += "<table width='100%'>"
    body += "<tr>"
    body += "<td height='50px' valign='bottom' align='center'>"
    body += "<span STYLE='color: #F88787; font-size: 20pt;'></span><br/><br/>"
    body += "</td>"
    body += "</tr>"
    body += "<tr>"
    body += "<td>"

    body += subbody


    body += "</td>"
    body += "</tr>"
    body += "<tr>"
    body += "<td align='center'>"

    body += "</td>"
    body += "</tr>"
    body += "<tr>"
    body += "<td>"

    body += "<br/><br/><span STYLE='font-size: 15pt;'>どうぞよろしくお願いします。</span><br/>"
    body += "<span STYLE='font-size: 15pt;'> 運営局</span><br/><br/>"
    body += "</td>"
    body += "</tr>"
    body += "</table>"
    body += "</td>"
    body += "<td width='20%'>"
    body += "</td>"
    body += "</tr>"
    body += "<tr>"
    body += "<td width='20%' height='10%'>"
    body += "</td>"
    body += "<td width='60%' height='10%'>"
    body += "</td>"
    body += "<td width='20%' height='10%'>"
    body += "</td>"
    body += "</tr>"
    body += "</table>"

    html=body

    part2 = MIMEText(html, 'html')


    msg.attach(part2)

    # Send the message via local SMTP server.
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_password)
    server.sendmail(me, you, msg.as_string())
    server.close()
    print('Email sent!')

def checkwifistate(nowdate):
    con_notice=[]
    slackmessage=""
    if check_internet():
        mamaromaxtime=[]
        #check Lock state
        sql = "select nursing_room_id,max(update_time) as maxtime from nursing_room_lock_state_time where TIMESTAMPDIFF(HOUR,update_time, CONVERT(NOW(),DATETIME))<24 group by nursing_room_id"
        result =db_execute(sql, None)
        if result is not None:
            for res in result:
                mamaromaxtime.append(mamaro_wifi_maxtime(str(res['nursing_room_id']),str(res['maxtime'])))
                print(res['nursing_room_id'])
                print(res['maxtime'])
        for i in range(len(mamaromaxtime)):
            Query1 = "select a.id,a.lock_state,b.name,b.address,b.GPS_lat,b.GPS_lng,b.company,b.company_tel,a.nursing_room_id";
            Query1 += " from nursing_room_lock_state_time as a inner join nursing_room as b on b.id=a.nursing_room_id";
            Query1 += " where a.nursing_room_id='" + mamaromaxtime[i].nursing_room_id + "' and a.update_time between'" + mamaromaxtime[i].maxtime + ".000" + "' and '" + mamaromaxtime[i].maxtime + ".999" + "' order by a.update_time;";
            result =db_execute(Query1, None)
            if result is not None:
                if len(result)>0:
                    if str(result[len(result)-1]['lock_state'])=="0":
                        con_notice.append(mamaro_wifi_content(str(result[len(result)-1]['id']),str(mamaromaxtime[i].maxtime),str(result[len(result)-1]['name']),str(result[len(result)-1]['address']),str(result[len(result)-1]['GPS_lat']),str(result[len(result)-1]['GPS_lng']),str(result[len(result)-1]['company']),str(result[len(result)-1]['company_tel']),str(result[len(result)-1]['nursing_room_id']) ))
        body_list = ""
        body_list_forcom = ""
        slackmessage=""
        for i in range(len(con_notice)):
            print(con_notice[i].id)
            nowdatetime=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            d0 = datetime.strptime(nowdatetime, '%Y-%m-%d %H:%M:%S')
            Query = "select id,notice_times from nursing_room_notice";
            Query += " where state_id='" + con_notice[i].id + "';";
            result =db_execute(Query, None)
            if result is not None:

                if len(result)>0:
                    print("have")
                    d1 = datetime.strptime(con_notice[i].update_time, '%Y-%m-%d %H:%M:%S')
                    delta = d0 - d1
                    hours, minutes, seconds = convert_timedelta(delta)
                    print ('{} seconds, {} minutes, {} hours'.format(seconds,minutes, hours))
                    minn=(hours*60)+minutes
                    for res in result:
                        if minn > 20 * (int(res['notice_times']) - 1) and minn < 20 * int(res['notice_times']):
                            #slack
                            slackmessage+= "{"+'"' + "title" + '"' + ":" + '"' + con_notice[i].name + '"' + " }"
                            slackmessage+=","
                            slackmessage+="{"+'"' + "text" + '"' + ":" + '"' + "Company name : " + con_notice[i].company + '"' + "," + '"' + "response_type" + '"' + ":" + '"' + "in_channel" + '"'+" }"
                            slackmessage+=","
                            slackmessage+="{"+'"' + "text" + '"' + ":" + '"' + "Company tel : " + con_notice[i].company_tel + '"' + "," + '"' + "response_type" + '"' + ":" + '"' + "in_channel" + '"' + " }"
                            slackmessage+=","
                            slackmessage+="{"+'"' + "text" + '"' + ":" + '"' + "Company address : " + con_notice[i].address + '"' + "," + '"' + "response_type" + '"' + ":" + '"' + "in_channel" + '"'+" }"
                            slackmessage+=","
                            slackmessage+="{"+'"' + "text" + '"' + ":" + '"' + " start time : " + con_notice[i].update_time + '"' + "," + '"' + "response_type" + '"' + ":" + '"' + "in_channel" + '"' + " }"
                            slackmessage+=","
                            slackmessage+="{"+'"' + "text" + '"' + ":" + '"' + " use time : " + str(hours) + " hours " + str(minutes) + " minutes " + str(seconds) + " seconds" + '"' + "," + '"' + "response_type" + '"' + ":" + '"' + "in_channel" + '"'+" }"
                            slackmessage+=","
                            #email
                            body_list += "<hr>"
                            body_list += "<span STYLE='font-size: 15pt;'>Company name : " + con_notice[i].company + "</span><br/>"
                            body_list += "<span STYLE='font-size: 15pt;'>Company tel : " + con_notice[i].company_tel + "</span><br/>"
                            body_list += "<span STYLE='font-size: 15pt;'>Company address : " + con_notice[i].address + "</span><br/>"
                            body_list += "<span STYLE='font-size: 15pt;'>mamaro name : " + con_notice[i].name + "</span><br/>"
                            body_list += "<span STYLE='font-size: 15pt;'> start time : " + con_notice[i].update_time + "</span><br/>"
                            body_list += "<span STYLE='font-size: 15pt;'> use time : " + str(hours) + " hours " + str(minutes) + " minutes " + str(seconds) + " seconds</span><br/>";

                            Query1 = "update nursing_room_notice set notice_times='" + str(int(res['notice_times']) + 1) + "',update_time=NOW() where id='" + res['id'] + "';"
                            checkin=db_execute_insert(Query1,None)
                            if checkin is not None:
                                if checkin:
                                    print("update notice time success")
                            else:
                                print("update notice time fail")

                            #send only once time
                            body_list = "";
                        if minn > 35 * (int(res['notice_times']) - 1) and minn < 35 * int(res['notice_times']):
                            body_list_forcom = con_notice[i].name

                else:
                    print("not have")
                    d1 = datetime.strptime(con_notice[i].update_time, '%Y-%m-%d %H:%M:%S')
                    delta = d0 - d1
                    hours, minutes, seconds = convert_timedelta(delta)
                    print ('{} seconds, {} minutes, {} hours'.format(seconds,minutes, hours))
                    minn=(hours*60)+minutes
                    if minn>20:
                        #slack
                        slackmessage+= "{"+'"' + "title" + '"' + ":" + '"' + con_notice[i].name + '"' + " }"
                        slackmessage+=","
                        slackmessage+="{"+'"' + "text" + '"' + ":" + '"' + "Company name : " + con_notice[i].company + '"' + "," + '"' + "response_type" + '"' + ":" + '"' + "in_channel" + '"'+" }"
                        slackmessage+=","
                        slackmessage+="{"+'"' + "text" + '"' + ":" + '"' + "Company tel : " + con_notice[i].company_tel + '"' + "," + '"' + "response_type" + '"' + ":" + '"' + "in_channel" + '"' + " }"
                        slackmessage+=","
                        slackmessage+="{"+'"' + "text" + '"' + ":" + '"' + "Company address : " + con_notice[i].address + '"' + "," + '"' + "response_type" + '"' + ":" + '"' + "in_channel" + '"'+" }"
                        slackmessage+=","
                        slackmessage+="{"+'"' + "text" + '"' + ":" + '"' + " start time : " + con_notice[i].update_time + '"' + "," + '"' + "response_type" + '"' + ":" + '"' + "in_channel" + '"' + " }"
                        slackmessage+=","
                        slackmessage+="{"+'"' + "text" + '"' + ":" + '"' + " use time : " + str(hours) + " hours " + str(minutes) + " minutes " + str(seconds) + " seconds" + '"' + "," + '"' + "response_type" + '"' + ":" + '"' + "in_channel" + '"'+" }"
                        slackmessage+=","
                        #email
                        body_list += "<hr>"
                        body_list += "<span STYLE='font-size: 15pt;'>Company name : " + con_notice[i].company + "</span><br/>";
                        body_list += "<span STYLE='font-size: 15pt;'>Company tel : " + con_notice[i].company_tel + "</span><br/>";
                        body_list += "<span STYLE='font-size: 15pt;'>Company address : " + con_notice[i].address + "</span><br/>";
                        body_list += "<span STYLE='font-size: 15pt;'> name : " + con_notice[i].name + "</span><br/>";
                        body_list += "<span STYLE='font-size: 15pt;'> start time : " + con_notice[i].update_time + "</span><br/>";
                        body_list += "<span STYLE='font-size: 15pt;'> use time : " + str(hours) + " hours " + str(minutes) + " minutes " + str(seconds) + " seconds</span><br/>";

                        Query1 = "insert into nursing_room_notice(state_id,notice_times,update_time) values('" + con_notice[i].id + "','1', NOW());";
                        checkin=db_execute_insert(Query1,None)
                        if checkin is not None:
                            if checkin:
                                print("insert notice time success")
                        else:
                            print("insert notice time fail")
            else:
                print("not have")


        if len(con_notice) > 0 and body_list != "":
            send_to_myself("who.com", body_list, "timeout check")
            send_to_slack(slackmessage,"timeout check")


        #check wifi state
        con_notice=[]
        body_list = ""
        body_list_forcom = ""
        slackmessage=""
        Query = "select nursing_room_id,max(update_time) as maxtime from nursing_room_wifi_state where TIMESTAMPDIFF(HOUR,update_time, CONVERT(NOW(),DATETIME))<24 group by nursing_room_id;"
        result =db_execute(Query, None)
        if len(result)>0:
            for res in result:
                maxtime=str(res['maxtime'])
                Query1 = "select a.id,b.name,b.address,b.GPS_lat,b.GPS_lng,b.company,b.company_tel"
                Query1 += " from nursing_room_wifi_state as a inner join nursing_room as b on b.id=a.nursing_room_id"
                Query1 += " where a.nursing_room_id='" + str(res['nursing_room_id']) + "' and a.update_time between'" + maxtime + ".000" + "' and '" + maxtime + ".999" + "' order by a.update_time;"
                result1 =db_execute(Query1, None)
                if len(result1)>0:
                    for res1 in result1:
                        #print(str(res1['id']))
                        con_notice.append(mamaro_wifi_content(str(res1['id']),str(maxtime),str(res1['name']),str(res1['address']),str(res1['GPS_lat']),str(res1['GPS_lng']),str(res1['company']),str(res1['company_tel']),str(res['nursing_room_id']) ))
        for i in range(len(con_notice)):
            print(con_notice[i].id)
            nowdatetime=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            d0 = datetime.strptime(nowdatetime, '%Y-%m-%d %H:%M:%S')
            Query = "select id,notice_times from nursing_room_notice_wifi"
            Query += " where state_id='" + con_notice[i].id + "';"
            result =db_execute(Query, None)
            if len(result)>0:
                for res in result:
                    d1 = datetime.strptime(con_notice[i].update_time, '%Y-%m-%d %H:%M:%S')
                    delta = d0 - d1
                    hours, minutes, seconds = convert_timedelta(delta)
                    print ('{} seconds, {} minutes, {} hours'.format(seconds,minutes, hours))
                    minn=(hours*60)+minutes
                    if minn > 20 * (int(res['notice_times']) - 1) and minn < 20 * int(res['notice_times']):
                        #slack
                        slackmessage+= "{"+'"' + "title" + '"' + ":" + '"' + con_notice[i].name + '"' + " }"
                        slackmessage+=","
                        slackmessage+="{"+'"' + "text" + '"' + ":" + '"' + "Company name : " + con_notice[i].company + '"' + "," + '"' + "response_type" + '"' + ":" + '"' + "in_channel" + '"'+" }"
                        slackmessage+=","
                        slackmessage+="{"+'"' + "text" + '"' + ":" + '"' + "Company tel : " + con_notice[i].company_tel + '"' + "," + '"' + "response_type" + '"' + ":" + '"' + "in_channel" + '"' + " }"
                        slackmessage+=","
                        slackmessage+="{"+'"' + "text" + '"' + ":" + '"' + "Company address : " + con_notice[i].address + '"' + "," + '"' + "response_type" + '"' + ":" + '"' + "in_channel" + '"'+" }"
                        slackmessage+=","
                        slackmessage+="{"+'"' + "text" + '"' + ":" + '"' + " start time : " + con_notice[i].update_time + '"' + "," + '"' + "response_type" + '"' + ":" + '"' + "in_channel" + '"' + " }"
                        slackmessage+=","
                        slackmessage+="{"+'"' + "text" + '"' + ":" + '"' + " use time : " + str(hours) + " hours " + str(minutes) + " minutes " + str(seconds) + " seconds" + '"' + "," + '"' + "response_type" + '"' + ":" + '"' + "in_channel" + '"'+" }"
                        slackmessage+=","
                        #email
                        body_list += "<hr>"
                        body_list += "<span STYLE='font-size: 15pt;'>Company name : " + con_notice[i].company + "</span><br/>";
                        body_list += "<span STYLE='font-size: 15pt;'>Company tel : " + con_notice[i].company_tel + "</span><br/>";
                        body_list += "<span STYLE='font-size: 15pt;'>Company address : " + con_notice[i].address + "</span><br/>";
                        body_list += "<span STYLE='font-size: 15pt;'> name : " + con_notice[i].name + "</span><br/>";
                        body_list += "<span STYLE='font-size: 15pt;'> start time : " + con_notice[i].update_time + "</span><br/>";
                        body_list += "<span STYLE='font-size: 15pt;'> use time : " + str(hours) + " hours " + str(minutes) + " minutes " + str(seconds) + " seconds</span><br/>";

                        #only once time
                        body_list = ""
                        Query1 = "update nursing_room_notice_wifi set notice_times='" + str(int(res['notice_times']) + 1) + "',update_time=NOW() where id='" + res['id'] + "';"
                        checkin=db_execute_insert(Query1,None)
                        if checkin is not None:
                            if checkin:
                                print("update wifi notice time success")
                            else:
                                print("update wifi notice time fail")
            else:
                d1 = datetime.strptime(con_notice[i].update_time, '%Y-%m-%d %H:%M:%S')
                delta = d0 - d1
                hours, minutes, seconds = convert_timedelta(delta)
                minn=(hours*60)+minutes
                print ('{} seconds, {} minutes, {} hours'.format(seconds,minutes, hours))
                if minn>20:
                    #slack
                    slackmessage+= "{"+'"' + "title" + '"' + ":" + '"' + con_notice[i].name + '"' + " }"
                    slackmessage+=","
                    slackmessage+="{"+'"' + "text" + '"' + ":" + '"' + "Company name : " + con_notice[i].company + '"' + "," + '"' + "response_type" + '"' + ":" + '"' + "in_channel" + '"'+" }"
                    slackmessage+=","
                    slackmessage+="{"+'"' + "text" + '"' + ":" + '"' + "Company tel : " + con_notice[i].company_tel + '"' + "," + '"' + "response_type" + '"' + ":" + '"' + "in_channel" + '"' + " }"
                    slackmessage+=","
                    slackmessage+="{"+'"' + "text" + '"' + ":" + '"' + "Company address : " + con_notice[i].address + '"' + "," + '"' + "response_type" + '"' + ":" + '"' + "in_channel" + '"'+" }"
                    slackmessage+=","
                    slackmessage+="{"+'"' + "text" + '"' + ":" + '"' + " start time : " + con_notice[i].update_time + '"' + "," + '"' + "response_type" + '"' + ":" + '"' + "in_channel" + '"' + " }"
                    slackmessage+=","
                    slackmessage+="{"+'"' + "text" + '"' + ":" + '"' + " use time : " + str(hours) + " hours " + str(minutes) + " minutes " + str(seconds) + " seconds" + '"' + "," + '"' + "response_type" + '"' + ":" + '"' + "in_channel" + '"'+" }"
                    slackmessage+=","
                    #email
                    body_list += "<hr>"
                    body_list += "<span STYLE='font-size: 15pt;'>Company name : " + con_notice[i].company + "</span><br/>";
                    body_list += "<span STYLE='font-size: 15pt;'>Company tel : " + con_notice[i].company_tel + "</span><br/>";
                    body_list += "<span STYLE='font-size: 15pt;'>Company address : " + con_notice[i].address + "</span><br/>";
                    body_list += "<span STYLE='font-size: 15pt;'> name : " + con_notice[i].name + "</span><br/>";
                    body_list += "<span STYLE='font-size: 15pt;'> start time : " + con_notice[i].update_time + "</span><br/>";
                    body_list += "<span STYLE='font-size: 15pt;'> use time : " + str(hours) + " hours " + str(minutes) + " minutes " + str(seconds) + " seconds</span><br/>";

                    Query1 = "insert into nursing_room_notice_wifi(state_id,notice_times,update_time) values('" + con_notice[i].id + "','1', NOW());";
                    checkin=db_execute_insert(Query1,None)
                    if checkin is not None:
                        if checkin:
                            print("insert wifi notice time success")
                    else:
                        print("insert wifi notice time fail")

        if body_list != "":
            send_to_myself("who.com", body_list, "【  】WIFI STATE check")
            send_to_slack(slackmessage,"【  】WIFI STATE check")

        #send recover email
        #send recover slack

        body_list=""
        slackmessage=""
        for i in range(len(con_notice)):
            print(con_notice[i].id)
            d0 = datetime.strptime(con_notice[i].update_time, '%Y-%m-%d %H:%M:%S')
            Query = "select * from nursing_room_notice_wifi_recover"
            Query += " where state_id='" + con_notice[i].id + "';"
            result =db_execute(Query, None)
            if len(result)==0:
                Query1 = "select nursing_room_id,max(update_time) as maxtime from nursing_room_wifi_state where "
                Query1 +="update_time<'"+con_notice[i].update_time+"' and nursing_room_id='"+con_notice[i].nursing_room_id+"' group by nursing_room_id;"
                result1 =db_execute(Query1, None)
                if len(result1)>0:
                    d1 = datetime.strptime(str(result1[0]['maxtime']), '%Y-%m-%d %H:%M:%S')
                    delta = d0 - d1
                    hours, minutes, seconds = convert_timedelta(delta)
                    minn=(hours*60)+minutes
                    print ('{} seconds, {} minutes, {} hours'.format(seconds,minutes, hours))
                    if minn>20:
                        #slack
                        slackmessage+= "{"+'"' + "title" + '"' + ":" + '"' + con_notice[i].name + '"' + " }"
                        slackmessage+=","
                        slackmessage+="{"+'"' + "text" + '"' + ":" + '"' + "Company name : " + con_notice[i].company + '"' + "," + '"' + "response_type" + '"' + ":" + '"' + "in_channel" + '"'+" }"
                        slackmessage+=","
                        slackmessage+="{"+'"' + "text" + '"' + ":" + '"' + "Company tel : " + con_notice[i].company_tel + '"' + "," + '"' + "response_type" + '"' + ":" + '"' + "in_channel" + '"' + " }"
                        slackmessage+=","
                        slackmessage+="{"+'"' + "text" + '"' + ":" + '"' + "Company address : " + con_notice[i].address + '"' + "," + '"' + "response_type" + '"' + ":" + '"' + "in_channel" + '"'+" }"
                        slackmessage+=","
                        slackmessage+="{"+'"' + "text" + '"' + ":" + '"' + " WIFI Disconnect time : " + str(result1[0]['maxtime']) + '"' + "," + '"' + "response_type" + '"' + ":" + '"' + "in_channel" + '"' + " }"
                        slackmessage+=","
                        slackmessage+="{"+'"' + "text" + '"' + ":" + '"' + " compare last disconnect time : " + str(hours) + " hours " + str(minutes) + " minutes " + str(seconds) + " seconds" + '"' + "," + '"' + "response_type" + '"' + ":" + '"' + "in_channel" + '"' + " }"
                        slackmessage+=","
                        slackmessage+="{"+'"' + "text" + '"' + ":" + '"' + " WIFI Recovery time : " + con_notice[i].update_time + '"' + "," + '"' + "response_type" + '"' + ":" + '"' + "in_channel" + '"' + " }"
                        slackmessage+=","
                        #email
                        body_list += "<hr>"
                        body_list += "<span STYLE='font-size: 15pt;'>Company name : " + con_notice[i].company + "</span><br/>";
                        body_list += "<span STYLE='font-size: 15pt;'>Company tel : " + con_notice[i].company_tel + "</span><br/>";
                        body_list += "<span STYLE='font-size: 15pt;'>Company address : " + con_notice[i].address + "</span><br/>";
                        body_list += "<span STYLE='font-size: 15pt;'> name : " + con_notice[i].name + "</span><br/>";
                        body_list += "<span STYLE='font-size: 15pt;'> WIFI Disconnect time : " + str(result1[0]['maxtime']) + "</span><br/>";
                        body_list += "<span STYLE='font-size: 15pt;'> compare last disconnect time : " + str(hours) + " hours " + str(minutes) + " minutes " + str(seconds) + " seconds</span><br/>";
                        body_list += "<span STYLE='font-size: 15pt;'> WIFI Recovery time : " + con_notice[i].update_time + " </span><br/>";

                        Query2 = "insert into nursing_room_notice_wifi_recover(state_id,update_time) values('" + con_notice[i].id + "', NOW());";
                        checkin=db_execute_insert(Query2,None)
                        if checkin is not None:
                            if checkin:
                                print("insert wifi recovery notice time success")
                        else:
                            print("insert wifi recovery notice time fail")


        if body_list != "":
            send_to_myself("who.com", body_list, "【  】WIFI Recovery Check")
            send_to_slack(slackmessage,"【  】WIFI Recovery Check")



checkupdatelog=True
if __name__ == '__main__':
    global checkupdatelog

    update_hour=9
    update_minute=0
    cousec=0
    while True:
        nowdatetimepr=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(str(nowdatetimepr))
        cousec+=1
        if cousec==150:
            nowdate=datetime.now().strftime('%Y-%m-%d')
            thread = threading.Thread(target=checkwifistate, args=(nowdate,))
            thread.daemon = True                            # Daemonize thread
            thread.start()

            #checkwifistate(nowdate)

            cousec=0
        nowhourr=datetime.now().strftime('%H')
        nowhour=int(nowhourr)
        nowminn=datetime.now().strftime('%M')
        nowmin=int(nowminn)
        nowsecc=datetime.now().strftime('%S')
        nowsec=int(nowsecc)
        # print(nowhour)
        # print(nowmin)
        if str(update_hour)==str(nowhour) and str(update_minute)==str(nowmin) and int(nowsec)<2:
            nowdatetime=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(nowdatetime)
            print("check log")
            nowdate=datetime.now().strftime('%Y-%m-%d')
            if checkupdatelog:
                thread = threading.Thread(target=getlogdata, args=(nowdate,))
                thread.daemon = True                            # Daemonize thread
                thread.start()
                #getlogdata(nowdate)
        if str(update_hour)==str(nowhour) and str(update_minute)==str(nowmin) and int(nowsec)>2:
            checkupdatelog=True
        time.sleep(1)
