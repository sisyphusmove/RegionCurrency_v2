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
from .views import NoticeLV

app_name = 'info'

urlpatterns = [
    path('list/', NoticeLV.as_view(), name='list'),
    # path('notice/add/', views.add, name='add'),
    # path('notice/read/<int:n_id>', views.read, name='read'),
    # path('notice/modify/<int:n_id>', views.add, name='modify'),
    # path('notice/delete/<int:n_id>', views.delete, name='delete'),
]
