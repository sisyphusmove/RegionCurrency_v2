from django.db import models
from store.models import Store

# Create your models here.
# class Discount_rate(modes.Model):
#     pass

class ChartStat(models.Model):
    age = models.IntegerField(null=True)
    gender = models.CharField(max_length=3, null=True)
    store = models.ForeignKey(Store, null=True, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now=True, null=True)
    amount = models.IntegerField(null=True)
