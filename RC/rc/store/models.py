from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import User
from django.urls import reverse
import os

from .fields import ThumbnailImageField

# Create your models here.

class Location(models.Model):
    loc = models.CharField(max_length=20)

    def __str__(self):
        return self.loc

class Category(models.Model):
    domain = models.CharField(max_length=20)

    def __str__(self):
        return self.domain

def upload_path_handler(instance, filename):
    return "store/store_{id}/{file}".format(id=instance.store.id, file=filename)

@python_2_unicode_compatible
class Store(models.Model):
    name = models.CharField(max_length=100, null=True)
    corporate_number = models.CharField(max_length=12, null=True)
    representative = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, null=True, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, null=True, on_delete=models.CASCADE)
    address = models.CharField(max_length=100, null=True, default='-')
    phone_number = models.CharField(max_length=15, null=True, default='-')
    url = models.CharField(max_length=100, null=True, default='-')
    opening_hour = models.CharField(max_length=2, null=True)
    opening_minute = models.CharField(max_length=2, null=True)
    closing_hour = models.CharField(max_length=2, null=True)
    closing_minute = models.CharField(max_length=2, null=True)
    description = models.TextField(blank=True)
    registered_date = models.DateTimeField(auto_now_add=True, null=True)
    modified_date = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=1, null=True)

    def __str__(self):
        return self.name

class Photo(models.Model):
    store = models.ForeignKey('Store', on_delete=models.CASCADE)
    image = ThumbnailImageField(upload_to=upload_path_handler, null=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    location = models.ForeignKey(Location, null=True, on_delete=models.CASCADE)

    class Meta:
        ordering = ['store']

    def __str__(self):
        return self.store.name
