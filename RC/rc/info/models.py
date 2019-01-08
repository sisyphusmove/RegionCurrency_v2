from django.db import models
from django.contrib.auth.models import User

# from django.contrib.auth import get_user_model

# Create your models here.

# User = get_user_model()

class Notice(models.Model):
    title = models.CharField('TITLE', max_length=100)
    content = models.TextField('CONTENT')
    writer = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    create_date = models.DateTimeField('CREATE_DATE', auto_now_add=True)
    modify_date = models.DateTimeField('MODIFY_DATE', auto_now=True)
    status = models.CharField('STATUS', max_length=1, default='Y')

class FAQ(models.Model):
    title = models.CharField('TITLE', max_length=100)
    content = models.TextField('CONTENT')
    writer = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

class QnA(models.Model):
    title = models.CharField('TITLE', max_length=100)
    content = models.TextField('CONTENT')
    writer = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    create_date = models.DateTimeField('CREATE_DATE', auto_now_add=True)
    modify_date = models.DateTimeField('MODIFY_DATE', auto_now=True)
    status = models.CharField('STATUS', max_length=1, default='Y')
    answer = models.TextField('ANSWER')
