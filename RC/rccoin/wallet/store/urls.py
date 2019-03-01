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
from .views import *

app_name = 'store'

urlpatterns = [
    path('apply/', edit_store, name='apply'),
    path('info/', get_myStore, name='info'),
    path('edit/', edit_store, name='edit'),
    path('<int:s_id>/delete/', del_store, name='delete'),
    path('qrcode/', get_qrcode, name='qrcode'),
    path('list/', StorePV.as_view(), name='store_list'),
    path('list/filter/<int:loc>/', filteredStoresPV.as_view(), name='filteredStores'),
    path('list/detail/<int:store_id>/', detailView, name='filteredStoresDetail')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)