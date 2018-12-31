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
    corporate_number = forms.CharField(widget=forms.TextInput(attrs={'id':'corporate_number', 'class':'form-control'}))
    representative = forms.ModelChoiceField(queryset=User.objects.all().order_by('id'), required=False)
    category = forms.ModelChoiceField(queryset =Category.objects.all().order_by('id'),
                                      widget=forms.Select(attrs={'id':'category', 'class':'form-control'}))
    location = forms.ModelChoiceField(queryset=Location.objects.all().order_by('id'),
                                      widget=forms.Select(attrs={'id':'location', 'class':'form-control'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'id':'address', 'class':'form-control'}), required=False)
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'id':'phone_number', 'class':'form-control'}), required=False)
    url = forms.CharField(widget=forms.TextInput(attrs={'id':'url', 'class':'form-control'}), required=False)
    opening_hour = forms.CharField(widget=forms.Select(attrs={'id':'opening_hour', 'class':'form-control'}))
    opening_minute = forms.CharField(widget=forms.Select(attrs={'id':'opening_minute', 'class':'form-control'}))
    closing_hour = forms.CharField(widget=forms.Select(attrs={'id':'closing_hour', 'class':'form-control'}))
    closing_minute = forms.CharField(widget=forms.Select(attrs={'id':'closing_minute', 'class':'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'id':'description', 'class':'form-control text-area'}))

    class Meta:
        model = Store
        fields = [
            'name', 'corporate_number', 'category', 'location', 'address', 'phone_number', 'url',
                  'opening_hour', 'opening_minute', 'closing_hour', 'closing_minute', 'description'
        ]
