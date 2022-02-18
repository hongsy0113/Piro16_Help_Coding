from django import forms
from .models import *

class QuestionForm(forms.ModelForm):
    img_recent = forms.CharField(required=False)
    file_recent = forms.CharField(required=False)
    class Meta:
        model = Question
        exclude = ('hit', 'like_user', 'user')

class FileForm(forms.ModelForm):
    attached_file = forms.FileField(label='attached_file')    
    class Meta:
        model = QuestionFiles
        fields = ()

class FileFieldForm(forms.Form):
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))