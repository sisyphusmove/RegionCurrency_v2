# /cms/templates/forms.py
from django.forms import ModelForm
from info.models import Notice

## info form
class NoticeForm(ModelForm):
    class Meta:
        model = Notice
        fields = ('title', 'content', ) 