from socket import fromshare
from django import forms
from .models import *

class GroupForm(form.ModelForm):
    class Meta:
        