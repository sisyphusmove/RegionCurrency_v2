
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import *

app_name = 'store'

urlpatterns = [
    path('apply/', store_edit, name='add'),
    path('read/<int:pk>/',StoreDV.as_view(), name='read'),
    path('edit/', store_edit, name='edit'),
    path('cancel_payment/', cancel_payment, name='cancel_payment'),
    path('add_canceled_payment/', add_canceled_payment, name='add_canceled_payment'),
    path('delete/', store_remove, name='delete'),
    path('getMyStore', get_myStore),
    path('QRcode', get_QRcode, name='get_QRcode'),
    path('store_list/', StorePV.as_view(), name='store_list'),
    path('store_list/filter/<int:loc>/',filteredStoresPV.as_view(), name='filteredStores'),
    path('store_list/detail/<int:store_id>/', detailView, name='filteredStoresDetail')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
