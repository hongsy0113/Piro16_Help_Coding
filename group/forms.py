from django import forms
from .models import *

class GroupForm(forms.ModelForm):
    img_recent = forms.CharField(required=False)
    class Meta:
        model = Group
        fields = ('name', 'image', 'intro')

class PostForm(forms.ModelForm):
    img_recent = forms.CharField(required=False)
    file_recent = forms.CharField(required=False)
    class Meta:
        model = GroupPost
        exclude = ('hit', 'user', 'group')