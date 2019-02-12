"""rccoin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('forget_id/', views.forget_id, name='forget_id'),
    path('forget_pwd/', views.forget_pwd, name='forget_pwd'),
    path('agreement/', views.agreement, name='agreement'),
    path('chk_username/', views.chk_username),
    path('chk_password/', views.chk_password),
    path('signup/', views.signup, name='signup'),
    path('info/', views.get_myinfo, name='info'),
    path('<str:op>/identity/', views.identity, name='identity'),
    path('<str:op>/identity/<int:s_id>/', views.identity, name='identity2'),
    path('edit/', views.account_edit, name='edit'),
    path('chg_pwd/', views.change_pwd, name='chg_pwd'),
]