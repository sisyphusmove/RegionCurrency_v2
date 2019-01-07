from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from .models import Location, Category, Store, Photo

class LocationForm(ModelForm):
    class Meta:
        model = Location
        fields = ['loc']

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['domain']

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image']

class StoreForm(ModelForm):
    name = forms.CharField()
    corporate_number = forms.CharField()
    representative = forms.ModelChoiceField(queryset=User.objects.all().order_by('id'), required=False)
    category = forms.ModelChoiceField(queryset =Category.objects.all().order_by('id'))
    location = forms.ModelChoiceField(queryset=Location.objects.all().order_by('id'))
    address = forms.CharField(required=False)
    phone_number = forms.CharField(required=False)
    url = forms.CharField(required=False)
    opening_hour = forms.CharField()
    opening_minute = forms.CharField()
    closing_hour = forms.CharField()
    closing_minute = forms.CharField()
    description = forms.CharField(required=False)

    class Meta:
        model = Store
        fields = [
            'name', 'corporate_number', 'category', 'location', 'address', 'phone_number', 'url',
                  'opening_hour', 'opening_minute', 'closing_hour', 'closing_minute', 'description'
        ]
