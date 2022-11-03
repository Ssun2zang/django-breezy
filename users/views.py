import re
from django.shortcuts import render
from .models import user
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import redirect
from .forms import loginform
import pymysql

# Create your views here.

def test(request):
    return render(request, 'test.html')

def home(request):

    return render(request, 'home.html')


def logout(request):
    if request.session.get('user'):

        del(request.session['user'])
        # print(request.session.get('user'))

        # 세션을 삭제하여 로그아웃함
        # ()랑 [] 어케 구분함??
    return redirect('/users/login')


def login(request):
    if request.method == 'POST':
        form = loginform(request.POST)
        if form.is_valid():  # 값이 다 입력되면
            # 세션코드
            request.session['user'] = form.user_id
            return redirect('/bridges/list/')
    else:
        form = loginform()

    return render(request, 'login.html', {'form': form})


def register(request):
    # register 서버에 들어가는게 그냥 링크로 들어오는 거랑 등록해서 들어오는 2가지가 있는데 GET/POST로 나눔?
    if request.method == 'GET':
        return render(request, 'register.html')
    elif request.method == 'POST':
        # 회원 가입 코드 작성
        username = request.POST.get('username', None)
        useremail = request.POST.get('useremail', None)
        password = request.POST.get('password', None)
        re_password = request.POST.get('re-password', None)

        # if password != re_password:
        #     return HttpResponse('비밀번호가 다릅니다!')
        # # 엄청 불편한 상태

        res_data = {}

        if not (username and useremail and password and re_password):
            res_data['error'] = '모든 값을 입력해야합니다.'
            # 빈 문자열이 들어왔을 때 에러처리
        elif password != re_password:
            res_data['error'] = '비밀번호가 다릅니다'
            # html 위쪽에 뜨게 됨
        else:
            conn = pymysql.connect(
                    user='root',
                    passwd='0208',
                    host='localhost',
                    port=3306,
                    db='breezy'
                )
            
            curs = conn.cursor(pymysql.cursors.DictCursor)
            
            sql = """insert into `breezy`.`user` (`username`, `useremail`, `password`) values (%s, %s, %s)"""

            curs.execute(sql, (username,useremail, make_password(password)))
            conn.commit()
            
            res_data['sign'] = "등록되었습니다."
            
        return render(request, 'register.html', res_data)