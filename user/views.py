from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import AnonymousUser
from django.views import View
from django.views.generic import ListView
from .forms import LoginForm, SignupForm, MypageReviseForm
from .models import *
from qna.models import Question, Answer
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.hashers import check_password
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from .tokens import user_activation_token
from django.utils.encoding import force_bytes, force_str
from datetime import date, datetime
import re, shutil

# Main
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

# Validation Check (Sign Up / My Page Revise)
def validation_check(email, nickname, current_password, new_password1, new_password2, birth, command):
    error = ''

    if 'signup' in command:
        if not re.compile('^[a-zA-Z0-9]+@[a-zA-Z0-9.]+$').match(email):  # 예외1-1) 잘못된 이메일 형식
            error += '올바른 이메일 주소를 입력해주세요.\n'
        elif User.objects.filter(email = email):  # 예외1-2) 이미 가입된 유저
            error += '이미 가입된 유저입니다.\n'

    if User.objects.filter(nickname = nickname) or not nickname:
        error += '이미 사용 중인 닉네임입니다.\n'

    if 'password_change' in command:
        if not check_password(current_password, User.objects.get(email = email).password):  # 예외2-1) 현재 비밀번호 오류
            error += '현재 비밀번호가 일치하지 않습니다.\n'

    if 'signup' in command or 'password_change' in command:
        if not re.compile('^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d$@$!%*#?&]{8,}$').match(new_password1):  # 예외3-1) 잘못된 비밀번호 형식
            error += '비밀번호는 영문자와 숫자를 혼합하여 8자리 이상으로 만들어주세요. (사용 가능 특수 기호 : $@$!%*#?&)\n'
        elif new_password1 != new_password2:  # 예외3-2) 비밀번호 불일치
            error += '비밀번호가 일치하지 않습니다.\n'

    if not re.compile('^[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]$').match(birth):  # 예외4) 잘못된 생년월일 형식
        error += '생년월일을 2022-02-22 형식으로 입력해주세요.\n'
    
    return error

# Birth Format (YYYY-MM-DD)
def birth_format(year, month, day):
    today = date.today()
    try:
        if int(year) > today.year:
            return ''
        birth = datetime(int(year), int(month), int(day)).strftime("%Y-%m-%d")
        return birth
    except:  # 잘못된 날짜
        return ''

# Sign Up
def sign_up(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        sign_up_error = validation_check(
            request.POST['email'],
            request.POST['nickname']
            '',
            request.POST['password1'],
            request.POST['password2'],
            request.POST['birth'],
            ['signup']
        )
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
            user.is_active = True  # 이메일 인증 기능 구현 시에는 False로 바꿀 것
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
    if user == AnonymousUser():
        return redirect('user:login')
    rewards = GetReward.objects.filter(user_id = user).order_by('-get_date')[:5]
    questions = Question.objects.filter(user = user).order_by('-updated_at')[:5]
    answers = Answer.objects.filter(user = user).order_by('-updated_at')[:5]
    ctx = {'user': user, 'rewards': rewards, 'questions': questions, 'answers': answers}
    return render(request, template_name = 'user/mypage.html', context = ctx)

# My Page Revise
def my_page_revise(request):
    user = request.user
    if user == AnonymousUser():
        return redirect('user:login')
    if request.method == 'POST':
        form = MypageReviseForm(request.POST)
        command = ['mypage_revise']
        if request.POST['current_password'] or request.POST['new_password1'] or request.POST['new_password2']:
            command += ['password_change']
        if request.FILES.get('img') or request.POST.get('img_setting') != 'own_img':
            command += ['image_change']
        birth = birth_format(request.POST['birth-y'], request.POST['birth-m'], request.POST['birth-d'])
        revise_error = validation_check(
            user.email,
            request.POST['nickname'],
            request.POST['current_password'],
            request.POST['new_password1'],
            request.POST['new_password2'],
            birth,
            command
        )
        if not revise_error:
            updated = '프로필이 성공적으로 수정되었습니다.'
            if 'password_change' in command:
                user.set_password(request.POST['new_password1'])
                updated += ' (비밀번호가 성공적으로 변경되었습니다.)'
            if 'image_change' in command:
                if request.POST.get('img_setting') == 'own_img':
                    user.img = request.FILES.get('img')
                else:
                    shutil.copyfile('./static/img/{}'.format(request.POST.get('img_setting')),
                    './media/user_{}/thumbnail/{}'.format(user.email, request.POST.get('img_setting')))
                    user.img = '/user_{}/thumbnail/{}'.format(user.email, request.POST.get('img_setting'))
            user.nickname = request.POST['nickname']
            user.birth = birth
            user.introduction = request.POST['introduction']
            user.job = request.POST['job']
            user.save()
            login(request, user)
            messages.success(request, updated)
            return redirect('user:mypage')
        ctx = {'user': user, 'form': form, 'revise_error': revise_error}
        return render(request, template_name = 'user/mypage_revise.html', context = ctx)
    else:
        form = MypageReviseForm(instance = user)
        ctx = {'user': user, 'form': form}
        return render(request, template_name = 'user/mypage_revise.html', context = ctx)

# My Page Question List
class QuestionView(ListView):
    model = Question
    paginate_by = 10
    template_name = 'user/mypage_question.html'
    context_object_name = 'questions'
    
    def get_queryset(self):
        questions = Question.objects.filter(user = self.request.user).order_by('-updated_at') 
        return questions

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context['paginator']
        page_numbers_range = 5
        max_index = len(paginator.page_range)
        page = self.request.GET.get('page')
        current_page = int(page) if page else 1
        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index
        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range
        return context

class AnswerView(ListView):
    model = Answer
    paginate_by = 10
    template_name = 'user/mypage_answer.html'
    context_object_name = 'answers'
    
    def get_queryset(self):
        answers = Answer.objects.filter(user = self.request.user).order_by('-updated_at') 
        return answers

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context['paginator']
        page_numbers_range = 5
        max_index = len(paginator.page_range)
        page = self.request.GET.get('page')
        current_page = int(page) if page else 1
        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index
        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range
        return context

#def my_page_question(request):
#    user = request.user
#    if user == AnonymousUser():
#        return redirect('user:login')
#    questions = Question.objects.filter(user = user).order_by('-updated_at')
#    ctx = {'user': user, 'questions': questions}
#    return render(request, template_name = 'user/mypage_question.html', context = ctx)

# My Page Answer List
#def my_page_answer(request):
#    user = request.user
#    if user == AnonymousUser():
#        return redirect('user:login')
#    answers = Answer.objects.filter(user = user).order_by('-updated_at')
#    ctx = {'user': user, 'answers': answers}
#    return render(request, template_name = 'user/mypage_answer.html', context = ctx)