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
from django.conf.urls import url
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('accounts/', include('django.contrib.auth.urls')),

    path('intro/', views.intro, name='intro'),
    path('map/', views.map, name='map'),
    path('info/', include('info.urls', namespace='info')),
    path('accounts/', include('profiles.urls', namespace='profile')),
    path('board/', include('board.urls', namespace='board')),
    path('store/', include('store.urls', namespace='store')),
    path('payment/', include('payment.urls', namespace='payment')),
    path('publish/', include('publish.urls', namespace='publish')),

    path('operate/', include('operate.urls', namespace='operate')),
  ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
