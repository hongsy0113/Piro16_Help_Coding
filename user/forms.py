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
            user = User.objects.get(username=email)
            if not user.check_password(password):  # 예외1) 잘못된 비밀번호 입력
                raise forms.ValidationError('올바른 비밀번호를 입력해주세요.')
            if not user.is_active:  # 예외2) 이메일 인증 미완료
                raise forms.ValidationError('이메일 인증 후 로그인해주세요.')
            else:
                return self.cleaned_data
        except User.DoesNotExist:  # 예외3) 회원가입하지 않은 이메일
            raise forms.ValidationError('유저가 존재하지 않습니다.')


class SignupForm(forms.Form):
    email = forms.CharField()
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    nickname = forms.CharField()
    birth = forms.CharField()
    img = forms.ImageField(required=False)
    img_recent = forms.CharField(required=False)
    introduction = forms.CharField(required=False)
    JOB_CHOICE = (('elementary_school', '초등학생'), ('middle_school', '중학생'), ('high_school', '고등학생'),
                  ('university', '대학생'), ('programmer', '개발자'), ('parents', '학부모'), ('etc', '기타'))
    job = forms.ChoiceField(choices=JOB_CHOICE)

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2',
                  'nickname', 'birth', 'img', 'introduction', 'job']


class MypageReviseForm(forms.ModelForm):
    current_password = forms.CharField(
        widget=forms.PasswordInput, required=False)
    new_password1 = forms.CharField(widget=forms.PasswordInput, required=False)
    new_password2 = forms.CharField(widget=forms.PasswordInput, required=False)
    nickname = forms.CharField()
    birth = forms.CharField()
    img = forms.ImageField(required=False)
    introduction = forms.CharField(required=False)
    JOB_CHOICE = (('elementary_school', '초등학생'), ('middle_school', '중학생'), ('high_school', '고등학생'),
                  ('university', '대학생'), ('programmer', '개발자'), ('parents', '학부모'), ('etc', '기타'))
    job = forms.ChoiceField(choices=JOB_CHOICE)

    class Meta:
        model = User
        fields = ['nickname', 'birth', 'img', 'introduction', 'job']


class PasswordChangeSearchForm(forms.Form):
    email = forms.CharField()


class PasswordChangeForm(forms.Form):
    new_password1 = forms.CharField(widget=forms.PasswordInput, required=False)
    new_password2 = forms.CharField(widget=forms.PasswordInput, required=False)
