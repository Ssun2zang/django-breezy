from distutils.command.clean import clean
from django import forms
from .models import user
from django.contrib.auth.hashers import check_password
import pymysql


class loginform(forms.Form):
    username = forms.CharField(
        error_messages={
            'required': '아이디를 입력해주세요.'
        },
        max_length=32, label='사용자 이름')
    password = forms.CharField(
        error_messages={
            'required': '비밀번호를 입력해주세요.'
        },
        widget=forms.PasswordInput, label='비밀번호')

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            try:
                conn = pymysql.connect(
                    user='root',
                    passwd='0208',
                    host='localhost',
                    port=3306,
                    db='breezy'
                )
                curs = conn.cursor()
                
                sql = "select * from user where username = '" + username + "';"
                
                curs.execute(sql)
                user = curs.fetchall()
                print(user)
                
            except user:
                self.add_error('username', '아이디가 없습니다.')
                return

            if not check_password(password, user[0][3]):
                self.add_error('password', '비밀번호를 틀렸습니다')
            else:
                self.user_id = user[0][1]