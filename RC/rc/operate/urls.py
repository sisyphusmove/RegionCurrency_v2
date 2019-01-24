"""rc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, include
from .views import *

from django.contrib.auth import views as auth_views

app_name = 'operate'

urlpatterns = [
#### main URL ##########################################################
    path('main/', main, name='main'),
#### 대시보드 URL #######################################################
    path('dashboard/', dashboard, name='dashboard'),
#### 공지사항 관리 URL ###################################################    
    path('notice/', manage_notice, name='notice'),
    path('notice/notice_add/', notice_edit, name='notice_add'),
    path('notice/notice_edit/<int:notice_id>', notice_edit, name='notice_edit'),
    path('notice/notice_activate/', notice_activate, name='notice_activate'),
#### 발행 관리 URL #######################################################    
    path('publish/', publish, name='publish'),
#### 거래 취소 관리 URL#######################################################
    path('cancel/', cancel, name='cancel'),
#### 네트워크 관리 URL ###################################################
    path('network/', network, name='network'),
#### 유저관리 URL ########################################################
    # path('users/', usersMyLV.as_view(), name='users'),
    path('users/', manageUser, name='users'),
    path('get_like/', get_like, name='get_like'),
#### 가맹점 URL ##########################################################
    path('approval/', manage_store_approval, name='approval'),
    path('get_approval/', get_approval, name='get_approval'),
##### 차트 URL ###########################################################
    path('stats/', manage_stats, name='stats'),
    path('stats/chartdata/', ChartData.as_view(), name='chartdata'),
    path('stats/west_stats/', west_stats, name='west_stats'),
    path('stats/north_stats/', north_stats, name='north_stats'),
    path('stats/wooleung_stats/', wooleung_stats, name='wooleung_stats'),
##### login_required ####################################################
    path('login_required/', login_required, name='login_required'),
    path('admin_logout/', admin_logout, name='admin_logout'),

    path('dd/', dd, name='dd'),
]
