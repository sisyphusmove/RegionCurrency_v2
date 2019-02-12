from django.contrib import admin
from .models import Board, Comment, BoardLiker

# Register your models here.

class CommentAdmin(admin.ModelAdmin):
    model = Comment
    verbose_name_plural = 'comments'

class BoardAdmin(admin.ModelAdmin):
    model = Board
    verbose_name_plural = 'boards'

class BoardLIkerAdmin(admin.ModelAdmin):
    model = BoardLiker
    verbose_name_plural = 'boardLikers'

admin.site.register(Board, BoardAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(BoardLiker, BoardLIkerAdmin)