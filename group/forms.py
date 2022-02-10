from django import forms
from .models import *

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('name', 'image', 'intro')

class PostForm(forms.ModelForm):
    class Meta:
        model = GroupPost
        exclude = ('hit', 'user', 'group')