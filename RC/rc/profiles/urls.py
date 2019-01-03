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
from django.urls import path
from . import views

app_name = 'profile'

urlpatterns = [
    path('agreement/', views.agreement, name='agreement'),
    path('signup/', views.account_edit, name='signup'),
    path('signup/check_username/', views.check_username, name='check_username'),
    path('myInfo/<int:account_id>/', views.my_info, name='account_myInfo'),
    path('myBalance', views.get_balance, name='get_balance'),
    path('myInfo/<int:account_id>/edit', views.account_edit, name='account_edit'),
    path('myInfo/<int:account_id>/check_password/', views.check_password, name='check_password'),
    path('check_username2/', views.check_username2, name='check_username2'),
    path('check_password2', views.check_password2, name='check_password2'),
    path('search_username/', views.search_username, name='search_username'),
    path('search_username/getUserList/', views.getUserList, name='getUserList'),
    path('search_password/', views.search_password, name='search_password'),
    path('search_password/initPassword/', views.initPassword, name='initPassword'),
    path('done/', views.done, name='done')
]
