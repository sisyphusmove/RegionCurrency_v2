from django.contrib import admin
from .models import Store, Location, Category, Photo

# Register your models here.

class LocationAdmin(admin.ModelAdmin):
    model = Location
    list_display = ['loc',]
    verbose_name_plural = 'location'

class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ['domain',]
    verbose_name_plural = 'category'



class StoreAdmin(admin.ModelAdmin):
    model = Store
    list_display = ['name', 'corporate_number', 'representative', 'category', 'location', 'address',
                    'phone_number', 'url', 'opening_hour', 'opening_minute', 'closing_hour', 'closing_minute',
                    'description', 'registered_date', 'modified_date', 'status']
    verbose_name_plural = 'store'

class PhotoAdmin(admin.ModelAdmin):
    list_display = ['store', 'image', 'upload_date', ]
    verbose_name_plural = 'photo'

admin.site.register(Location, LocationAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Store, StoreAdmin)