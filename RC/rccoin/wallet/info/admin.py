from django.contrib import admin
from .models import Notice, FAQ, QnA

# Register your models here.

class NoticeAdmin(admin.ModelAdmin):
    model = Notice
    verbose_name_plural = 'notice'

class FAQAdmin(admin.ModelAdmin):
    model = FAQ
    verbose_name_plural = 'faq'

class QnAAdmin(admin.ModelAdmin):
    model = QnA
    verbose_name_plural = 'qna'

admin.site.register(Notice, NoticeAdmin)
admin.site.register(FAQ, FAQAdmin)
admin.site.register(QnA, QnAAdmin)

