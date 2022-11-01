from django.urls import path
from . import views

urlpatterns = [
    path('data/<str:cookie>/', views.chart_data),
    path('datedata/<str:BRID>/', views.datedata),
    path('loading/<str:BRID>/<int:year>/<int:month>/<int:day>/<int:year2>/<int:month2>/<int:day2>/', views.loading),
    path('report/<str:BRID>/', views.report)
]