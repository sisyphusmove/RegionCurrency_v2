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
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'wallet'

urlpatterns = [
    path('info/', views.read_wallet, name="info"),
    path('publish/', views.publish, name="publish"),
    path('remittance/', views.remittance, name="remittance"),
    path('payment/', views.payment, name="payment"),
    path('history/', views.get_history),
    path('receipt/', views.get_receipt),
    path('cancel/', views.cancel, name="cancel"),
    path('cancel_payment/', views.cancel_payment, name="cancel_payment"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)