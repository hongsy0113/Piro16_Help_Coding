from django import forms
from .models import *

class QuestionForm(forms.ModelForm):
    img_recent = forms.CharField(required=False)
    file_recent = forms.CharField(required=False)
    class Meta:
        model = Question
        exclude = ('hit', 'like_user', 'user')
