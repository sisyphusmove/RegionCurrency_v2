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

app_name = 'payment'

urlpatterns = [
    path('withdraw/<int:account_id>/', views.withdraw, name='withdraw'),
    path('transfer/', views.transfer, name="transfer"),
    path('progress/', views.progress, name="progress"),
    path('payment', views.payment, name="payment"),
    path('get_history/',views.get_history, name="get_history"),
    path('get_receipt/',views.get_receipt, name="get_receipt")
]
