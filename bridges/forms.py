from distutils.command.clean import clean
from django import forms
from .models import Bridges
from django.contrib.auth.hashers import check_password
# html에 쓰기위해 만든 forms.py 파일
# 1. html에 form은 쓴다한 2. form.py 파일을 만듦 3. view랑 url을 연결함

class Bridgeform(forms.Form):
    title = forms.CharField(
        error_messages= {
            'required' : '제목을 입력해주세요.'
        } ,
        max_length= 128, label ='제목')
    contents = forms.CharField(
        error_messages= {
          'required' : '내용을 입력해주세요.'  
        },
        widget=forms.Textarea, label = '내용')
    tags = forms.CharField(
        required=False, label = '태그')    
    # tag는 필수가 아니라서 required가 없음
    