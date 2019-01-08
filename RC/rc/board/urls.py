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

from .views import BoardLV
from .views import BoardDV
from .views import *

app_name = 'board'

urlpatterns = [
    path('list/', BoardLV.as_view(), name='list'),
    path('read/<int:pk>/', BoardDV.as_view(), name='read'),
    path('add/', board_edit, name='add'),
    path('edit/<int:board_id>/', board_edit, name='edit'),
    path('delete/<int:board_id>/', board_delete, name='delete'),
    path('comment/', get_comment, name='comment'),
    path('chg/', chg_board, name='chg'),
    path('write_comment/', write_comment, name='write_comment'),
    path('add_like/', add_like, name='add_like'),

    ## external
    path('board_each/', board_each, name='board_each'),
]
