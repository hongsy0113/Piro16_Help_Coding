from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.views import View
from .forms import LoginForm, SignupForm
from .models import *
from qna.models import Question, Answer
from django.contrib import auth
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from .tokens import user_activation_token
from django.utils.encoding import force_bytes, force_str
import re

def main(request):
    return render(request, 'user/main.html')

# Login
class LoginView(View):
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username = email, password = password)
            if user is not None:
                login(request, user)
                return redirect('user:main')
        ctx = {'form': form}
        return render(request, 'user/login.html', ctx)

    def get(self, request):
        form = LoginForm()
        return render(request, 'user/login.html', {'form': form})

# Logout
def log_out(request):
    logout(request)
    return redirect('user:main')

# Sign Up
def sign_up(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        sign_up_error = ''

        if not re.compile('^[a-zA-Z0-9]+@[a-zA-Z0-9.]+$').match(request.POST['email']):  # 예외1-1) 잘못된 이메일 형식
            sign_up_error += '올바른 이메일 주소를 입력해주세요.\n'
        elif User.objects.filter(email = request.POST['email']):  # 예외1-2) 이미 가입된 유저
            sign_up_error += '이미 가입된 유저입니다.\n'
            
        if not re.compile('^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d$@$!%*#?&]{8,}$').match(request.POST['password1']):  # 예외2-1) 잘못된 비밀번호 형식
            sign_up_error += '비밀번호는 영문자와 숫자를 혼합하여 8자리 이상으로 만들어주세요. (사용 가능 특수 기호 : $@$!%*#?&)\n'
        elif request.POST['password1'] != request.POST['password2']:  # 예외2-2) 비밀번호 불일치
            sign_up_error += '비밀번호가 일치하지 않습니다.\n'

        if not re.compile('[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]').match(request.POST['birth']):  # 예외3) 잘못된 생년월일 형식
            sign_up_error += '생년월일을 2022-02-22 형식으로 입력해주세요.\n'

        if not sign_up_error:  # 오류가 없는 경우 유저 생성
            user = User.objects.create_user(
                username = request.POST['email'],
                email = request.POST['email'],
                password = request.POST['password1'],
                nickname = request.POST['nickname'],
                birth = request.POST['birth'],
                img = request.FILES.get('img'),
                introduction = request.POST['introduction'],
                total_like = 0,
                job = request.POST['job'],
            )
            user.is_active = False
            user.save()
            # 인증 이메일 발송
            current_site = get_current_site(request)
            message = render_to_string('user/user_activate_email.html',
                {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)).encode().decode(),
                    'token': user_activation_token.make_token(user),
                }
            )
            mail_subject = '[도와줘, 코딩] 회원가입 인증 메일입니다.'
            email = EmailMessage(mail_subject, message, to=[user.email])
            email.send()
            return render(request, 'user/signup_success.html', {'email': user.email})
        return render(request, 'user/signup.html', {'form': form, 'sign_up_error': sign_up_error})
            
    else:
        form = SignupForm()
        return render(request, 'user/signup.html', {'form': form, 'sign_up_error': ''})

# Activate
def activate(request, uid64, token):
    uid = force_str(urlsafe_base64_decode(uid64))
    user = User.objects.get(pk = uid)
    if user is not None and user_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('user:main')
    else:
        return HttpResponse('비정상적인 접근입니다.')

# My Page
def my_page(request):
    user = request.user
    rewards = GetReward.objects.filter(user_id = user).order_by('-get_date')[:5]
    questions = Question.objects.filter(user = user).order_by('-updated_at')[:5]
    answers = Answer.objects.filter(user = user).order_by('-updated_at')[:5]
    ctx = {'user': user, 'rewards': rewards, 'questions': questions, 'answers': answers}
    return render(request, template_name='user/mypage.html', context = ctx)