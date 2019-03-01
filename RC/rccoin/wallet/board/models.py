from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

# Create your models here.
# author = models.ForeignKey(settings.AUTH_USER_MODEL)

User = get_user_model()

class Board(models.Model):
    title = models.CharField('TITLE', max_length=100)
    content = models.TextField('CONTENT')
    writer = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    create_date = models.DateTimeField('CREATE_DATE', auto_now_add=True)
    modify_date = models.DateTimeField('MODIFY_DATE', auto_now=True)
    category = models.CharField('CATEGORY', max_length=10)
    count = models.IntegerField('COUNT', default=0)
    recommend = models.IntegerField('RECOMMEND', default=0)
    status = models.CharField('STATUS', max_length=1, default='Y')

    class Meta:
        ordering = ('-create_date',)
    def get_absolute_url(self):
        return reverse("board:read", args=(self.pk,))

class Comment(models.Model):
    board_id = models.ForeignKey(Board, on_delete=models.CASCADE)
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField('CONTENT')
    create_date = models.DateTimeField('CREATE_DATE', auto_now_add=True)
    modify_date = models.DateTimeField('MODIFY_DATE', auto_now=True)
    status = models.CharField('STATUS', max_length=1, default='Y')

class BoardLiker(models.Model):
    liker = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    board = models.ForeignKey(Board, null=True, on_delete=models.CASCADE)
