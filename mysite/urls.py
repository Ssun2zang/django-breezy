"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.conf.urls.static import static
from django.conf import settings
from docs.views import MainView, file_upload_view, upload_home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('board/', include('board.urls')),
    path('chart/', include('chart.urls')),
    path('users/', include('users.urls')),
    path('bridges/', include('bridges.urls')),
    path('', upload_home, name = 'main-view'),
    path('docs/', include('docs.urls')),
    path('upload/', file_upload_view, name = 'upload-view'),
]

urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_URL)
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)