from django.db import models
from store.models import Store
# from jdango
# Create your models here.

class Cancellation(models.Model):
    s_id = models.ForeignKey(Store, on_delete=models.CASCADE)
    txHash = models.CharField(max_length=70)

    def __str__(self):
        return self.txHash