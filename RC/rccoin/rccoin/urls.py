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
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('accounts/', include('django.contrib.auth.urls')),

    path('', views.index, name='index'),
    path('<str:op>/done/', views.done, name='done'),
    
    path('intro/', views.intro, name='intro'),
    path('guide/', views.guide, name='guide'),
    path('map/', views.map, name='map'),

    path('operate/', include('operate.urls', namespace='operate')),
    path('account/', include('account.urls', namespace='account')),
    path('store/', include('store.urls', namespace='store')),
    path('wallet/', include('wallet.urls', namespace='wallet')),
    path('info/', include('info.urls', namespace='info')),
    path('board/', include('board.urls', namespace='board')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
