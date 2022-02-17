import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import AnonymousUser
from django.views import View
from django.views.generic import ListView
from .forms import LoginForm, SignupForm, MypageReviseForm
from .models import *
from .constants import *
from .update import *
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
from config.settings import MEDIA_ROOT
import re
import shutil
import os
import time
from threading import Timer

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
            user = authenticate(request, username=email, password=password)
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

# Error Messages


class ErrorMessages():

    email, nickname, current_password, new_password1, new_password2, birth, img, job = '', '', '', '', '', '', '', ''
    # Validation Check (Sign Up / My Page Revise)

    def validation_check(self, email, nickname, current_password, new_password1, new_password2, birth, img, img_setting, img_recent, job, command):

        if 'signup' in command:
            # 예외1-1) 잘못된 이메일 형식
            if not re.compile('^[a-zA-Z0-9]+@[a-zA-Z0-9.]+$').match(email):
                self.email = '올바른 이메일 주소를 입력해주세요.'
            elif User.objects.filter(email=email):  # 예외1-2) 이미 가입된 유저
                self.email = '이미 가입된 유저입니다.'

        if not nickname:  # 예외2-1) 닉네임 입력하지 않음
            self.nickname = '닉네임을 입력해주세요.'
        else:
            if 'signup' in command:  # 예외2-2) 이미 사용 중인 닉네임 (회원 가입 시)
                if User.objects.filter(nickname=nickname):
                    self.nickname = '이미 사용 중인 닉네임입니다.'
            else:  # 예외2-3) 이미 사용 중인 닉네임 (닉네임 수정 시)
                if User.objects.filter(nickname=nickname) and User.objects.get(nickname=nickname).email != email:
                    self.nickname = '이미 사용 중인 닉네임입니다.'

        if 'password_change' in command:
            # 예외3-1) 현재 비밀번호 오류
            if not check_password(current_password, User.objects.get(email=email).password):
                self.current_password = '현재 비밀번호가 일치하지 않습니다.'

        if 'signup' in command or 'password_change' in command:
            # 예외4-1) 잘못된 비밀번호 형식
            if not re.compile('^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d$@$!%*#?&]{8,}$').match(new_password1):
                self.new_password1 = '비밀번호는 영문자와 숫자를 혼합하여 8자리 이상으로 만들어주세요. (사용 가능 특수 기호 : $@$!%*#?&)'
            elif new_password1 in email:  # 예외4-2) 이메일에 포함되는 비밀번호
                self.new_password1 = '비밀번호는 이메일 주소에 포함되지 않게 만들어주세요.'
            if new_password1 != new_password2:  # 예외4-3) 비밀번호 불일치
                self.new_password2 = '비밀번호가 일치하지 않습니다.'

        # 예외5) 잘못된 생년월일 형식
        if not re.compile('^[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]$').match(birth):
            self.birth = '유효한 생년월일을 입력해주세요.'

        if 'signup' in command or 'image_change' in command:
            if img_setting == 'own_img' and not img and not img_recent:  # 예외6) 이미지 선택 안 함
                self.img = '이미지를 업로드하거나 기본 이미지를 선택해주세요.'

        if 'signup' in command:
            if not job:  # 예외7) 직업 미선택
                self.job = '직업을 선택해주세요.'

    def has_error(self):
        return self.email or self.nickname or self.current_password or self.new_password1 or self.new_password2 or self.birth or self.img or self.job

# Original Information (Forms)


class OriginalInformation():

    def remember(self, request, command):
        if 'signup' in command:
            self.email = request.POST['email']
        else:
            self.current_password = request.POST['current_password']
        self.new_password1 = request.POST['new_password1']
        self.new_password2 = request.POST['new_password2']
        self.nickname = request.POST['nickname']
        self.birth_y = request.POST['birth-y']
        self.birth_m = request.POST['birth-m']
        self.birth_d = request.POST['birth-d']
        self.img = request.FILES.get('img')
        self.img_setting = request.POST.get('img_setting')
        self.introduction = request.POST['introduction']
        self.job = request.POST.get('job')

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
        birth = birth_format(
            request.POST['birth-y'], request.POST['birth-m'], request.POST['birth-d'])
        sign_up_error = ErrorMessages()
        sign_up_error.validation_check(
            request.POST['email'],
            request.POST['nickname'],
            '',
            request.POST['new_password1'],
            request.POST['new_password2'],
            birth,
            request.FILES.get('img'),
            request.POST.get('img_setting'),
            request.POST['img_recent'],
            request.POST.get('job'),
            ['signup']
        )
        if not sign_up_error.has_error():  # 오류가 없는 경우 유저 생성
            os.makedirs(
                MEDIA_ROOT + '/user_{}/thumbnail/'.format(request.POST['email']), exist_ok=True)
            user = User.objects.create_user(
                username=request.POST['email'],
                email=request.POST['email'],
                password=request.POST['new_password1'],
                nickname=request.POST['nickname'],
                birth=birth,
                introduction=request.POST['introduction'],
                total_question_like=0,
                total_comment_like=0,
                total_question=0,
                total_answer=0,
                total_answer_reply=0,
                job=request.POST.get('job'),
            )
            if request.POST.get('img_setting') == 'own_img':
                if request.FILES.get('img'):
                    user.img = request.FILES.get('img')
                else:
                    shutil.copyfile('./media/temp/{}'.format(request.POST['img_recent']),
                                    './media/user_{}/thumbnail/{}'.format(user.email, request.POST['img_recent']))
                    user.img = '/user_{}/thumbnail/{}'.format(
                        user.email, request.POST['img_recent'])
            else:
                shutil.copyfile('./static/img/user_thumbnail/{}'.format(request.POST.get('img_setting')),
                                './media/user_{}/thumbnail/{}'.format(user.email, request.POST.get('img_setting')))
                user.img = '/user_{}/thumbnail/{}'.format(
                    user.email, request.POST.get('img_setting'))
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
            # email.send()
            Timer(24 * 60 * 60, unauthenticated_user_delete,
                  [request.POST['email']]).start()
            ######## 업적 초기화를 위한 임시적인 부분 ########
            if request.POST['email'] == 'reward@reward.com':
                initializeReward()
            ################################################
            return render(request, 'user/signup_success.html', {'email': user.email})

        original_information = OriginalInformation()
        original_information.remember(request, ['signup'])
        if request.FILES.get('img'):
            os.makedirs(MEDIA_ROOT + '/temp/', exist_ok=True)
            with open('./media/temp/{}'.format(request.FILES.get('img')), 'wb+') as destination:
                for chunk in request.FILES['img'].chunks():
                    destination.write(chunk)
        original_information.img = request.POST['img_recent']
        return render(request, 'user/signup.html', {'form': form, 'sign_up_error': sign_up_error,
                                                    'base_images': BASE_IMAGES, 'original_information': original_information, 'job_choice': JOB_CHOICE,
                                                    'temp_img_location': '/media/temp/'})

    else:
        form = SignupForm()
        return render(request, 'user/signup.html', {'form': form, 'sign_up_error': '',
                                                    'base_images': BASE_IMAGES, 'original_information': '', 'job_choice': JOB_CHOICE,
                                                    'temp_img_location': '/media/temp/'})

# Activate


def activate(request, uid64, token):
    uid = force_str(urlsafe_base64_decode(uid64))
    user = User.objects.get(pk=uid)
    if user is not None and user_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('user:main')
    else:
        return HttpResponse('비정상적인 접근입니다.')

# Remove Unauthenticated User


def unauthenticated_user_delete(email):
    try:
        user = User.objects.get(email=email)
        if not user.is_active:
            user.delete()
    except:
        pass

# My Page


def my_page(request):
    user = request.user
    if user == AnonymousUser():
        return redirect('user:login')
    rewards = GetReward.objects.filter(user=user).order_by('-get_date')[:5]
    questions = Question.objects.filter(user=user).order_by('-updated_at')[:5]
    answers = Answer.objects.filter(user=user).order_by('-updated_at')[:5]
    ctx = {'user': user, 'rewards': rewards,
           'questions': questions, 'answers': answers}
    return render(request, template_name='user/mypage.html', context=ctx)

# My Page Revise


def my_page_revise(request):
    user = request.user
    if user == AnonymousUser():
        return redirect('user:login')
    if request.method == 'POST':
        form = MypageReviseForm(request.POST)
        birth = birth_format(
            request.POST['birth-y'], request.POST['birth-m'], request.POST['birth-d'])
        command = ['mypage_revise']
        print(request.POST['current_password'])
        print(request.POST['new_password1'])
        if request.POST['current_password'] or request.POST['new_password1'] or request.POST['new_password2']:
            command += ['password_change']
        if request.POST.get('img_setting') != 'no_change_img':
            command += ['image_change']
        revise_error = ErrorMessages()
        revise_error.validation_check(
            user.email,
            request.POST['nickname'],
            request.POST['current_password'],
            request.POST['new_password1'],
            request.POST['new_password2'],
            birth,
            request.FILES.get('img'),
            request.POST.get('img_setting'),
            request.POST['img_recent'],
            request.POST.get('job'),
            command
        )
        if not revise_error.has_error():
            updated = '프로필이 성공적으로 수정되었습니다.'
            if 'password_change' in command:
                user.set_password(request.POST['new_password1'])
                updated += ' (비밀번호가 성공적으로 변경되었습니다.)'
            if 'image_change' in command:
                if request.POST.get('img_setting') == 'own_img':
                    if request.FILES.get('img'):
                        user.img = request.FILES.get('img')
                    else:
                        user.img = '/user_{}/thumbnail/{}'.format(
                            user.email, request.POST['img_recent'])
                else:
                    shutil.copyfile('./static/img/user_thumbnail/{}'.format(request.POST.get('img_setting')),
                                    './media/user_{}/thumbnail/{}'.format(user.email, request.POST.get('img_setting')))
                    user.img = '/user_{}/thumbnail/{}'.format(
                        user.email, request.POST.get('img_setting'))
            user.nickname = request.POST['nickname']
            user.birth = birth
            user.introduction = request.POST['introduction']
            user.job = request.POST.get('job')
            user.save()
            login(request, user)
            messages.success(request, updated)
            return redirect('user:mypage')
        original_information = OriginalInformation()
        original_information.remember(request, command)
        if request.FILES.get('img'):
            with open('./media/user_{}/thumbnail/{}'.format(user.email, request.FILES.get('img')), 'wb+') as destination:
                for chunk in request.FILES['img'].chunks():
                    destination.write(chunk)
        original_information.img = request.POST['img_recent']
        ctx = {'user': user, 'form': form, 'revise_error': revise_error, 'base_images': BASE_IMAGES, 'job_choice': JOB_CHOICE,
               'current_image': user.img.url.split('/')[-1], 'original_information': original_information, 'temp_img_location': '/media/user_{}/thumbnail/'.format(user.email)}
        return render(request, template_name='user/mypage_revise.html', context=ctx)
    else:
        form = MypageReviseForm(instance=user)
        ctx = {'user': user, 'form': form, 'base_images': BASE_IMAGES, 'job_choice': JOB_CHOICE,
               'current_image': user.img.url.split('/')[-1], 'temp_img_location': '/media/user_{}/thumbnail/'.format(user.email)}
        return render(request, template_name='user/mypage_revise.html', context=ctx)

# List View (Question, Answer, Reward, Point)


class MypageView(ListView):
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context['paginator']
        page_numbers_range = 5
        max_index = len(paginator.page_range)
        page = self.request.GET.get('page')
        current_page = int(page) if page else 1
        start_index = int((current_page - 1) /
                          page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index
        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range
        return context

# My Page Question List


class QuestionView(MypageView):
    model = Question
    template_name = 'user/mypage_question.html'
    context_object_name = 'questions'

    def get_queryset(self):
        questions = Question.objects.filter(
            user=self.request.user).order_by('-updated_at')
        return questions

# My Page Answer List


class AnswerView(MypageView):
    model = Answer
    template_name = 'user/mypage_answer.html'
    context_object_name = 'answers'

    def get_queryset(self):
        answers = Answer.objects.filter(
            user=self.request.user).order_by('-updated_at')
        return answers

# My Page Reward List


def my_page_reward(request):
    user = request.user
    user_reward = []
    if user == AnonymousUser():
        return redirect('user:login')
    rewards = Reward.objects.all()
    for get_reward in GetReward.objects.filter(user=user):
        user_reward.append(get_reward.reward.id)
    representative_reward = user.representative_reward
    ctx = {'user': user, 'rewards': rewards, 'user_reward': user_reward, 'representative_reward': representative_reward}
    return render(request, template_name='user/mypage_reward.html', context=ctx)


# My Page Point List


class PointView(MypageView):
    model = GetPoint
    template_name = 'user/mypage_point.html'
    context_object_name = 'points'

    def get_queryset(self):
        points = GetPoint.objects.filter(
            user=self.request.user).order_by('-get_date')
        return points

# My Page Alert List


class AlertView(MypageView):
    model = Alert
    template_name = 'user/mypage_alert.html'
    context_object_name = 'alerts'

    def get_queryset(self):
        alerts = Alert.objects.filter(user=self.request.user).order_by('-time')
        return alerts


# Check Alert (Ajax)
@csrf_exempt
def check_alert_ajax(request):
    req = json.loads(request.body)
    alert_id = req['id']
    alert = Alert.objects.get(id=alert_id)
    alert.checked = True
    alert.save()
    return JsonResponse({'alert_id': alert_id, 'new_alert_num': request.user.has_new_alert()})

# Check All Alert (Ajax)


@csrf_exempt
def check_all_alert_ajax(request):
    all_alert_id = []
    for alert in Alert.objects.filter(user=request.user):
        if not alert.checked:
            all_alert_id.append(alert.id)
            alert.checked = True
            alert.save()
    return JsonResponse({'all_alert_id': all_alert_id})


# Set Representative Reward (Ajax)
@csrf_exempt
def representative_reward_ajax(request):
    req = json.loads(request.body)
    user_id = req['user_id']
    reward_id = req['reward_id']
    reward = Reward.objects.get(pk=reward_id)
    user = User.objects.get(pk=user_id)
    try:
        previous_id = user.representative_reward.id
    except:  # 존재하지 않는 경우
        previous_id = 0
    user.representative_reward = reward
    user.save()
    return JsonResponse({'previous_id': previous_id, 'reward_id': reward_id})

# Get Reward Date (Ajax)


@csrf_exempt
def date_reward_ajax(request):
    req = json.loads(request.body)
    user_id = req['user_id']
    reward_ids = req['reward_id']
    date = []
    for reward_id in reward_ids:
        reward = Reward.objects.get(pk=reward_id)
        user = User.objects.get(pk=user_id)
        date.append(GetReward.objects.get(
            user=user, reward=reward).get_date.strftime("%Y.%m.%d")[2:])
    return JsonResponse({'reward_id': reward_ids, 'date': date})

# 공개 프로필 정보
def public_userpage(request, pk):
    view_user = get_object_or_404(User, pk=pk)

    rewards = GetReward.objects.filter(user=view_user).order_by('-get_date')[:5]
    questions = Question.objects.filter(user=view_user).order_by('-updated_at')[:5]
    answers = Answer.objects.filter(user=view_user).order_by('-updated_at')[:5]
    ctx = {
        'view_user': view_user, 
        'rewards': rewards,
        'questions': questions, 
        'answers': answers
    }
    
    return render(request, template_name='user/public_userpage.html', context=ctx)

# 그룹 가입 대기자 프로필 정보
@csrf_exempt
def group_wait_profile(request):
    req = json.loads(request.body)
    wait_user_id = req['userId']

    wait_user = get_object_or_404(User, pk=wait_user_id)

    wait_id = wait_user.id

    return JsonResponse({
        'userId': wait_id
    })
