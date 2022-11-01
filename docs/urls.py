from django.urls import path
from . import views

#현재 폴더에 있는 views에서 가져옴

urlpatterns = [
    path('<str:BRID>/', views.upload_home),
    # path('', views.upload_home),
    path('<str:BRID>/upload/', views.file_upload_view),
]