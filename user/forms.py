from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class LoginForm(forms.Form):
  email = forms.CharField()
  password = forms.CharField(widget=forms.PasswordInput)

  def clean(self):
    email = self.cleaned_data.get('email')
    password = self.cleaned_data.get('password')

    try:
      user = User.objects.get(username = email)
      if user.check_password(password):
        return self.cleaned_data
      else:
        raise forms.ValidationError('올바른 비밀번호를 입력해주세요.')
    except User.DoesNotExist:
      raise forms.ValidationError('올바른 이메일 주소를 입력해주세요.')

class SignupForm(UserCreationForm):
  class Meta:
    model = User
    fields = ['email', 'password1', 'password2', 'nickname', 'birth', 'img', 'introduction', 'job']
