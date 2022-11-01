from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.board_list),
    path('add/', views.board_write),
]
