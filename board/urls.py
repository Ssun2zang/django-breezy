from django.urls import path
from . import views

#현재 폴더에 있는 views에서 가져옴

urlpatterns = [
    path('put/', views.board_data),
    path('upload/<str:cookie>/<str:BRID>', views.board_upload),
]