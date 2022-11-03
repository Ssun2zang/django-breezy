from django.shortcuts import render, redirect
from .models import *
from .models import Bridges
from bridges.forms import Bridgeform
# Create your views here.
from users.models import user

from django.http import Http404
from django.core.paginator import Paginator
import pymysql
import pandas as pd



def _board_list(request):
    userform = request.session.get('user')

    conn = pymysql.connect(
                    user='root',
                    passwd='0208',
                    host='localhost',
                    port=3306,
                    db='breezy'
                )
    
    curs = conn.cursor()
    sql = "select * from user where username = " + "'"+userform+"'"+";"
    # id 정보를 추가로 넘겨줘야 함

    curs.execute(sql)
    row = curs.fetchall()

    auth_bridge = row[0][4]
    if auth_bridge:
        auth_list = auth_bridge.split(',')
    print(auth_list)
        
    bridge_list = []     

#     boards = Board.objects.all().order_by('-id')

    if (auth_list[0] == 'admin'):
        curs1 = conn.cursor()
        sql1 = "select * from bridge_info;"
        # id 정보를 추가로 넘겨줘야 함

        curs1.execute(sql1)
        bridge_list = curs1.fetchall()
    else:
        for brid in auth_list:   
            curs1 = conn.cursor()
            sql1 = "select * from bridge_info where br_name = " + "'"+brid+"'"+";"
            # print(sql1)
            # id 정보를 추가로 넘겨줘야 함

            curs1.execute(sql1)
            row1 = curs1.fetchall()
            # print(row1)
            if row1:
                print(row1[0])
                bridge_list.append(row1[0])
    
    print(bridge_list)

    return render(request, 'brlist.html', {'bridge_list': bridge_list})

def board_list(request):
    userform = request.session.get('user')

    if not userform:
        return redirect('/users/login/')

    conn = pymysql.connect(
                    user='root',
                    passwd='0208',
                    host='localhost',
                    port=3306,
                    db='breezy'
                )
    
    curs = conn.cursor()
    sql = "select * from report where writer = " + "'"+userform+"'"+";"
    # id 정보를 추가로 넘겨줘야 함

    curs.execute(sql)
    row = curs.fetchall()
    print(row)


    return render(request, 'brlist.html', {'bridge_list': row, 'username': userform})

def board_add(request):
    if not request.session.get('user'):
        return redirect('/users/login/')
    

    return render(request, 'bradd.html')


def board_write(request):

    if not request.session.get('user'):
        return redirect('/users/login/')
    

    if request.method == 'GET':
        userform = request.session.get('user')

        conn = pymysql.connect(
                    user='root',
                    passwd='0208',
                    host='localhost',
                    port=3306,
                    db='breezy'
                )
        
        curs = conn.cursor()
        sql = "select * from user where username = " + "'"+userform+"'"+";"
        # id 정보를 추가로 넘겨줘야 함

        curs.execute(sql)
        row = curs.fetchall()

        auth_bridge = row[0][4]
        if auth_bridge:
            auth_list = auth_bridge.split(',')
        print(auth_list)

        return render(request, 'bradd.html',{'list':auth_list} )
    elif request.method == 'POST':
        # 회원 가입 코드 작성
        brname = request.POST.get('brname', None)
        brleng = request.POST.get('brleng', None)
        section = request.POST.get('section', None)
        writer = request.session.get('user')

        res_data = {}

        if not (brname and brleng and section):
            res_data['error'] = '모든 값을 입력해야합니다.'
            # 빈 문자열이 들어왔을 때 에러처리
        else:
            conn = pymysql.connect(
                    user='root',
                    passwd='0208',
                    host='localhost',
                    port=3306,
                    db='breezy'
                )
            
            curs = conn.cursor(pymysql.cursors.DictCursor)
            
            sql = """insert into `breezy`.`report` (`rp_name`, `rp_leng`, `rp_sID`, `writer`, `cur`) values (%s, %s, %s, %s, %s)"""

            curs.execute(sql, (brname,brleng, brname+section, writer, '2'))
            conn.commit()
            
            res_data['sign'] = "추가되었습니다."
            print("dd")
            
        return render(request, 'bradd.html', res_data)