from django.forms import ModelForm

from board.models import Board

class BoardForm(ModelForm):
    class Meta:
        model = Board
        fields = ('title', 'content')
