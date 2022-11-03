from stat import S_IFDIR
from unittest.result import failfast
from django.shortcuts import render
import os
import numpy as np
import json
import pymysql
import shutil
from users.models import user
from datetime import datetime, timedelta
import pprint
import time
from influxdb import InfluxDBClient
from copy import deepcopy
import math
from datetime import datetime, timedelta
import pprint
import time
from influxdb import InfluxDBClient
from copy import deepcopy
import math
from django.http import Http404




# Create your views here.

def board_data(request):
    return render(request, 'board_data.html')


def _board_upload(request, cookie):  # 안 씀
    conn = pymysql.connect(
                user='root',
                passwd='pass',
                host='localhost',
                port=3306,
                db='breezy'
            )
        
    curs = conn.cursor()
    sql = "select dir from session where cookie = '"+ cookie +"';"
    curs.execute(sql)

    row = curs.fetchall()
    path = 'C:/Users/heise/Documents/janet_web/mysite/media/'+row[0][0]+'/'

    acc1 = []
    acc2 = []
    acc3 = []
    str1 = []
    str2 = []
    str3 = []
    S_id = "1"
    S_time="1"
    cal1 = "1"
    cal2 = "1"
    datalist = [S_id, S_time, acc1, acc2, acc3, str1, str2, str3, cal1, cal2]

    def FetchAllFiles(datalist, file, _fail):
        f = open(file.path, 'r')
        # data = f.read()
        filelist = f.readlines()
        if (filelist[0][:19] ):
            _fail +=1
            f.close() 
            os.remove(file)
            return (_fail)
        for line in filelist[6:-1]:

            dat  = line.split('\t')       # txt 한줄
            datalist[2].append(np.float64(dat[1])) # 가속도 x축
            datalist[3].append(np.float64(dat[2])) # 가속도 y축
            datalist[4].append(np.float64(dat[3])) # 가속도 z축
            datalist[5].append(np.float64(dat[4])) # 변형률 1채널
            datalist[6].append(np.float64(dat[5])) # 변형률 2채널
            datalist[7].append(np.float64(dat[6])) # 변형률 3채널
            # print(filelist[0][:18])
        if (filelist[0][:19] == "- * MCU: TEENSY 4.1"):
            datalist[0]= filelist[1][-2:]
            datalist[1]= filelist[2][-19:]
        f.close()
        return 0 
    
    

    
    if os.path.exists(path):
            success = 0
            _fail = 0
            for file in os.scandir(path):
                _fail += FetchAllFiles(datalist, file, _fail)

                if os.path.exists(file):

                    _curs = conn.cursor(pymysql.cursors.DictCursor)

                            
                    _sql = """insert into `janetweb`.`Sbridge_data` (`S_id`, `S_time`, `acc1`, `acc2`, `acc3`,`str1`, `str2`, `str3`, `cal1`, `cal2`, `cookie` ) values (%s, %s,%s, %s,%s, %s,%s, %s,%s, %s, %s)"""

                    _curs.execute(_sql, (datalist[0],datalist[1],str(datalist[2]),str(datalist[3]),str(datalist[4]),str(datalist[5]),str(datalist[6]),str(datalist[7]), str(datalist[8]), str(datalist[9]), cookie))
                    conn.commit()

                    acc1.clear()
                    acc2.clear()
                    acc3.clear()
                    str1.clear()
                    str2.clear()
                    str3.clear()
                    S_id = "1"   
                    S_time="1"
                    cal1 = "1"
                    cal2 = "1"
                    success += 1
    if os.path.exists(path):
        shutil.rmtree(path)

    return render(request, 'board_upload.html', {'datalist': datalist, 'cookie': cookie, 'success': success, 'fail': _fail})


def get_ifdb(db, host='localhost', port=8086):
    
    client = InfluxDBClient(host, port, database = db)
    try:
            client.create_database(db)
            print('Connection Successful')
            # print(f'host :{host}\nport :{port}\n\ndatabase :{db}')
    except:
        print('Connection Failed')
        pass
    return client


def board_upload(request, cookie, BRID):
    userform = request.session.get('user')
    Success = 0
    conn = pymysql.connect(
                    user='root',
                    passwd='0208',
                    host='localhost',
                    port=3306,
                    db='breezy'
                )

    curs = conn.cursor()
    sql = "select * from user where username = " + "'"+str(userform)+"'"+";"
    # id 정보를 추가로 넘겨줘야 함
    print(sql)

    curs.execute(sql)
    row = curs.fetchall()
    print(row)
    auth_bridge = row[0][4]
    if auth_bridge:
        auth_list = auth_bridge.split(',')

    if (auth_list[0] == 'admin'):
        Success = 1
        pass
    else:
        for brid in auth_list:   
            if brid in BRID:
                Success = 1
                continue

    if Success == 0:
        raise Http404('교량 권한이 없습니다')
    
    conn = pymysql.connect(
                    user='root',
                    passwd='0208',
                    host='localhost',
                    port=3306,
                    db='breezy'
            )
        
    curs = conn.cursor()
    sql = "select dir from session where cookie = '"+ cookie +"';"
    curs.execute(sql)

    row = curs.fetchall()
    path = 'C:/Users/heise/Documents/janet_web/mysite/media/'+row[0][0]+'/'


    def upload_rtcdata(ifdb, txtfile, BRID):
    
        table_name = 'JANET_1'    # 수정
        fieldlist = ["acc_1", "acc_2", "acc_3", "str_1", "str_2", "str_3", "dt"]     # 수정
        
        point = {
            "measurement":table_name,
            "tags":{
                "tag1" : 'acceleration1',
                "S_id":BRID,
                "cookie":"cookie",
            },
            "time" : None,
            "fields":{
                fieldlist[0]: 0,
                fieldlist[1]: 0,
                fieldlist[2]: 0,
                fieldlist[3]: 0,
                fieldlist[4]: 0,
                fieldlist[5]: 0,
                fieldlist[6]: "",
            },
        }
        
        json_body = []
        # print(str(20)+str(txtfile)[2:-4])
        print(str(txtfile))
        
        dt = datetime.strptime(str(20)+str(txtfile)[-18:-6],'%Y%m%d%H%M%S')

            
        f = open(txtfile, 'r')
        _file = f.readlines()


        if (_file[0][:19] != "- * MCU: TEENSY 4.1"):
            f.close()  
            os.remove(txtfile)
            return 0

        # aa = int(len(lines))
        for line in _file[6:]:

            np = deepcopy(point)
            dat  = line.split('\t')    
            try:
                # np["tags"]["S_id"]=str(_file[1][-2:-1])
                np["tags"]["cookie"]=cookie
                np["tags"]["tag1"]="acceleration1"
                np["fields"][fieldlist[0]]=float(dat[1])
                np["fields"][fieldlist[1]]=float(dat[2])
                np["fields"][fieldlist[2]]=float(dat[3])
                np["fields"][fieldlist[3]]=float(dat[4])
                np["fields"][fieldlist[4]]=float(dat[5])
                np["fields"][fieldlist[5]]=float(dat[6])
                np["fields"][fieldlist[6]]=str(dt)
                np["time"] = dt
                dt += timedelta(milliseconds=10)
                json_body.append(np)
                # print(dt)
            except IndexError:
                break
                
        ifdb.write_points(json_body)
        # result = ifdb.query('select * from %s' % table_name)
        # pprint.pprint(result.raw)
        # print(np)
        
        return 1
    
    
    success = 0
    fail = 0
    
    if os.path.exists(path):
            
            for file in os.scandir(path):
                ifdb = get_ifdb(db='sensor')
                isSuccess = upload_rtcdata(ifdb, file, BRID)
                if (isSuccess):
                    success += isSuccess
                else:
                    fail += 1

    if os.path.exists(path):
        shutil.rmtree(path)

    return render(request, 'board_upload.html', { 'cookie': cookie, 'success': success, 'fail': fail, 'BRID':BRID})

