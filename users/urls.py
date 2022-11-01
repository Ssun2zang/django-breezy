#후에 만든 파일

from django.urls import path
from . import views

#현재 폴더에 있는 views에서 가져옴

urlpatterns = [
    path('register/', views.register),
    path('login/', views.login),
    path('logout/', views.logout),
    path('test/', views.test)
]