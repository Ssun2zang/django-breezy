import imp
import re
from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse, JsonResponse
from .models import Doc
import os
import random
import string
import pymysql
import datetime
import shutil
from influxdb import InfluxDBClient
from copy import deepcopy

# import sys
# sys.path.append("C:/Users/heise/Documents/janet_web/mysite/board")
# from views import success, fail

# Create your views here.


# def test(requset):
#     return render(main.html)

class MainView(TemplateView):
    template_name = 'docs/main.html'


def DeleteAllFiles(filePath):
        if os.path.exists(filePath):
            for file in os.scandir(filePath):
                os.remove(file.path)

def deleteFolder(directory):
    shutil.rmtree(directory)

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)


def upload_home(request, BRID):
    # success = 0
    # fail = 
    # BRID = "trst"
    key_value = ""
    for i in range(8):
        key_value += str(random.choice(string.ascii_uppercase + string.digits))

    rand = str(datetime.datetime.now())

    for i in range(8):
        rand += str(random.choice(string.ascii_uppercase + string.digits))

    cookie_dir = rand.replace(':','-',2)

    createFolder('media/'+cookie_dir)

    conn = pymysql.connect(
                    user='root',
                    passwd='0208',
                    host='localhost',
                    port=3306,
                    db='breezy'
                )
            
    curs = conn.cursor(pymysql.cursors.DictCursor)
    
    sql = """insert into `breezy`.`session` (`cookie`, `dir`) values (%s, %s)"""

    curs.execute(sql, (key_value,cookie_dir))
    conn.commit()


    response = render(request, 'main.html', {'dirrr' : key_value, 'BRID' : BRID})
    response.set_cookie('primary_key', key_value, max_age=90)
    
    DeleteAllFiles("media/datas") # 시간을 확인하며 새 폴더들을,..

    return response

def file_upload_view(request, BRID):
    # print(request.FILES)
    # DeleteAllFiles("media/datas")
    cookieee = request.COOKIES.get('primary_key')
    
    if request.method == 'POST':
        my_file = request.FILES.get('file')
        # Doc.upload_where = ('')
        Doc.objects.create(upload = my_file)

        conn = pymysql.connect(
                    user='root',
                    passwd='0208',
                    host='localhost',
                    port=3306,
                    db='breezy'
                )
        
        curs = conn.cursor()
        sql = "select dir from session where cookie = '"+ cookieee +"';"
        curs.execute(sql)

        row = curs.fetchall()

        source = 'media/datas/'
        destination = 'media/'+row[0][0]+'/'

        shutil.move(source+my_file.name,destination+my_file.name)
        # print(my_file)   # 파일명
        return HttpResponse('')
    return JsonResponse({'post':'false'})