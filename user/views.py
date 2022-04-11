import json
from random import random, sample
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import AnonymousUser
from django.views import View
from django.views.generic import ListView
from .forms import LoginForm, SignupForm, MypageReviseForm, PasswordChangeSearchForm, PasswordChangeForm
from .models import *
from .constants import *
from .update import *
from .periodic_tasks import *
from qna.models import Question, Answer
from group.models import *
from group.iframe import *
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.hashers import check_password
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from .tokens import user_activation_token
from django.utils.encoding import force_bytes, force_str
from datetime import date, datetime, timedelta
from config.settings import MEDIA_ROOT
import re
import shutil
import os
import time
from threading import Timer
from datetime import datetime
from django.db.models import Count


# Main


def main(request):
    user = request.user
    ctx = {}
    if user != AnonymousUser():
        groups = user.group_set.all()
        posts = GroupPost.objects.filter(group__in=groups).exclude(
            user=user).order_by('-created_at')[:3]
        posts_img_dict = {}
        for post in posts:
            if get_img_src(post.attached_link):
                posts_img_dict[post] = get_img_src(post.attached_link)
            elif post.image:
                posts_img_dict[post] = post.image.url
            else:
                posts_img_dict[post] = ''

        ctx['posts_img_dict'] = posts_img_dict

        ### 이번주 우수 질문
        ## 특정 기간 동안 올라온 질문 중 답변이 완료된 질문들을 선정
        ## 좋아요 순서대로 10개를 택하고 그 중 3개를 랜덤으로 보여줌
        ### 답변은 좋아요가 제일 많은 답변 보여줌
        # main_questions = Question.objects.filter(created_at__gte = date.today() - timedelta(days=14))
        # questions_list = [question.id for question in main_questions if question.answer_set.filter(is_deleted = False, answer_depth = 0).exists()]
        # main_questions = Question.objects.filter(id__in = questions_list).annotate(total_likes=Count('like_user')).order_by('-total_likes')[:10]
        # ## 3개 랜덤으로 select
        # id_list = [question.id for question in main_questions]
        # main_questions = Question.objects.filter(id__in = sample(id_list, 3))
        # # 세 개의 질문에 대해 가장 좋아요 많이 받은 답변을 선택해 dictionary에 담기
        # question_answer_dict = {}
        # for question in main_questions:
        #     question_answer_dict[question] = question.answer_set.filter(is_deleted = False, answer_depth = 0).annotate(total_likes=Count('like_user')).order_by('-total_likes').first()
        # ctx['question_answer_dict'] = question_answer_dict
    return render(request, 'user/main.html', context=ctx)

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
        if request.user != AnonymousUser():
            return redirect('user:main')
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

        # signup / mypage_revise (password_change, image_change) / password_forgotten
        if 'signup' in command:
            # 예외1-1) 잘못된 이메일 형식
            if not re.compile('^[a-zA-Z0-9]+@[a-zA-Z0-9.]+$').match(email):
                self.email = '올바른 이메일 주소를 입력해주세요.'
            elif User.objects.filter(email=email):  # 예외1-2) 이미 가입된 유저
                self.email = '이미 가입된 유저예요. 다른 이메일 주소를 입력해주세요.'

        if 'signup' in command or 'mypage_revise' in command:
            if not nickname:  # 예외2-1) 닉네임 입력하지 않음
                self.nickname = '닉네임을 입력해주세요.'
            elif len(nickname) > 7:  # 예외2-2) 너무 긴 닉네임
                self.nickname = '닉네임은 7글자 이내로 지어주세요.'
            else:
                if 'signup' in command:  # 예외2-3) 이미 사용 중인 닉네임 (회원 가입 시)
                    if User.objects.filter(nickname=nickname):
                        self.nickname = '이미 사용 중인 닉네임이에요. 다른 닉네임을 입력해주세요.'
                else:  # 예외2-3) 이미 사용 중인 닉네임 (닉네임 수정 시)
                    if User.objects.filter(nickname=nickname) and User.objects.get(nickname=nickname).email != email:
                        self.nickname = '이미 사용 중인 닉네임이에요. 다른 닉네임을 입력해주세요.'

        if 'password_change' in command:
            # 예외3-1) 현재 비밀번호 오류
            if not check_password(current_password, User.objects.get(email=email).password):
                self.current_password = '현재 비밀번호가 일치하지 않아요.'

        if 'signup' in command or 'password_change' in command or 'password_forgotten' in command:
            # 예외4-1) 잘못된 비밀번호 형식
            if not re.compile('^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d$@$!%*#?&]{8,}$').match(new_password1):
                self.new_password1 = '비밀번호는 영문자와 숫자를 혼합하여 8자리 이상으로 만들어주세요. (사용 가능 특수 기호 : $@$!%*#?&)'
            elif new_password1 in email:  # 예외4-2) 이메일에 포함되는 비밀번호
                self.new_password1 = '비밀번호는 이메일 주소에 포함되지 않게 만들어주세요.'
            if new_password1 != new_password2:  # 예외4-3) 비밀번호 불일치
                self.new_password2 = '비밀번호가 일치하지 않아요.'

        # 예외5) 잘못된 생년월일 형식
        if 'signup' in command or 'mypage_revise' in command:
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
        elif 'password_forgotten' not in command:
            self.current_password = request.POST['current_password']
        self.new_password1 = request.POST['new_password1']
        self.new_password2 = request.POST['new_password2']
        if 'password_forgotten' not in command:
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
                MEDIA_ROOT + '/user/user_{}/thumbnail/'.format(request.POST['email']), exist_ok=True)
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
                                    './media/user/user_{}/thumbnail/{}'.format(user.email, request.POST['img_recent']))
                    user.img = '/user/user_{}/thumbnail/{}'.format(
                        user.email, request.POST['img_recent'])
            else:
                # USER가 DEFAULT IMG 고른 상황
                user.default_img = request.POST.get('img_setting')
                # shutil.copyfile('./static/img/user_thumbnail/{}'.format(request.POST.get('img_setting')),
                #                 './media/user/user_{}/thumbnail/{}'.format(user.email, request.POST.get('img_setting')))
                # user.img = '/user/user_{}/thumbnail/{}'.format(
                #     user.email, request.POST.get('img_setting'))
            user.is_active = False  # 이메일 인증 기능 구현 시에는 False로 바꿀 것
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
            ######## 업적 초기화를 위한 임시적인 부분 ########
            # if request.POST['email'] == 'reward@reward.com':
            #    initializeReward()
            ################################################
            ######## 타이머 실행을 위한 임시적인 부분 ########
            # if request.POST['email'] == 'timer@timer.com':
            #    PERIODIC_TASKS_TIMER.timer = Timer(initial_period(datetime.now()),
            #                                       periodic_tasks)
            #    PERIODIC_TASKS_TIMER.timer.start()
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
    user = get_object_or_404(User, pk=uid)
    if user is not None and user_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('user:main')
    else:
        return HttpResponse('비정상적인 접근입니다.')

# My page


def my_page(request):
    user = request.user
    if user == AnonymousUser():
        return redirect('user:login')
    rewards = GetReward.objects.filter(user=user).order_by('-get_date')[:5]
    questions = Question.objects.filter(user=user).order_by('-updated_at')[:5]
    answers = Answer.objects.filter(user=user).order_by('-updated_at')[:5]
    ctx = {'user': user, 'rewards': rewards,
           'questions': questions, 'answers': answers, 'periodic_tasks_timer': PERIODIC_TASKS_TIMER}
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
                updated += ' (비밀번호 변경 완료)'
            if 'image_change' in command:
                if request.POST.get('img_setting') == 'own_img':
                    if request.FILES.get('img'):
                        user.img = request.FILES.get('img')
                    else:
                        user.img = '/user/user_{}/thumbnail/{}'.format(
                            user.email, request.POST['img_recent'])
                    # 이미지 직접 설정한 경우 default_img field를 blank로 해야 함
                    user.default_img = ''
                else:
                    # default img 선택한 경우
                    # img field를 null로 해야 됨
                    user.img = None
                    user.default_img = request.POST.get('img_setting')
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
            with open('./media/user/user_{}/thumbnail/{}'.format(user.email, request.FILES.get('img')), 'wb+') as destination:
                for chunk in request.FILES['img'].chunks():
                    destination.write(chunk)
        original_information.img = request.POST['img_recent']
        ctx = {'user': user, 'form': form, 'revise_error': revise_error, 'base_images': BASE_IMAGES, 'job_choice': JOB_CHOICE,
               'original_information': original_information, 'temp_img_location': '/media/user/user_{}/thumbnail/'.format(user.email)}
        if user.img:
            ctx['current_image'] = user.img.url.split('/')[-1]
        else:
            ctx['current_image'] = user.default_img
        return render(request, template_name='user/mypage_revise.html', context=ctx)
    else:
        form = MypageReviseForm(instance=user)

        ctx = {'user': user, 'form': form, 'base_images': BASE_IMAGES, 'job_choice': JOB_CHOICE,
                'temp_img_location': '/media/user/user_{}/thumbnail/'.format(user.email)}
        # user_img 필드에 항상 값이 들어가 있지 않다. 만약 default이미지라면 null이 되어야 함
        if user.img:
            ctx['current_image'] = user.img.url.split('/')[-1]
        else:
            ctx['current_image'] = user.default_img
        return render(request, template_name='user/mypage_revise.html', context=ctx)

# Drop


def drop(request):
    user = request.user
    if user == AnonymousUser():
        return redirect('user:login')
    ctx = {'user': user, 'email': user.email}
    return render(request, template_name='user/drop.html', context=ctx)

# Drop Success


def drop_success(request):
    user = request.user
    if user == AnonymousUser():
        return redirect('user:login')
    user.is_active = False
    user.save()
    current_site = get_current_site(request)
    message = render_to_string('user/user_drop_email.html',
                               {
                                   'user': user,
                                   'domain': current_site.domain,
                                   'uid': urlsafe_base64_encode(force_bytes(user.pk)).encode().decode(),
                                   'token': user_activation_token.make_token(user),
                               }
                               )
    mail_subject = '[도와줘, 코딩] 회원탈퇴 확인 메일입니다.'
    email = EmailMessage(mail_subject, message, to=[user.email])
    email.send()
    ctx = {'user': user, 'email': user.email}
    return render(request, template_name='user/drop_success.html', context=ctx)


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
        if self.request.user == AnonymousUser():
            return HttpResponse('비정상적인 접근입니다.')
        try:
            user = get_object_or_404(User, pk=self.kwargs["pk"])
        except KeyError:
            user = self.request.user
        questions = Question.objects.filter(
            user=user).order_by('-updated_at')
        return questions


# My Page Answer List


class AnswerView(MypageView):
    model = Answer
    template_name = 'user/mypage_answer.html'
    context_object_name = 'answers'

    def get_queryset(self):
        if self.request.user == AnonymousUser():
            return HttpResponse('비정상적인 접근입니다.')
        try:
            user = get_object_or_404(User, pk=self.kwargs["pk"])
        except KeyError:
            user = self.request.user
        answers = Answer.objects.filter(
            user=user).order_by('-updated_at')
        return answers

# My Page Reward List


def my_page_reward(request, pk):
    public = False
    if request.user == AnonymousUser():
        return redirect('user:login')
    if request.user.pk != pk:
        view_user = get_object_or_404(User, pk=pk)
        public = True
    else:
        view_user = request.user
    user_reward = []
    rewards = Reward.objects.all()
    for get_reward in GetReward.objects.filter(user=view_user):
        user_reward.append(get_reward.reward.id)
    representative_reward = view_user.representative_reward
    ctx = {'view_user': view_user, 'rewards': rewards, 'user_reward': user_reward,
           'representative_reward': representative_reward, 'public': public}
    return render(request, template_name='user/mypage_reward.html', context=ctx)


# My Page Point List


class PointView(MypageView):
    model = GetPoint
    template_name = 'user/mypage_point.html'
    context_object_name = 'points'

    def get_queryset(self):
        if self.request.user == AnonymousUser():
            return HttpResponse('비정상적인 접근입니다.')
        points = GetPoint.objects.filter(
            user=self.request.user).order_by('-get_date')
        return points

# My Page Alert List


class AlertView(MypageView):
    model = Alert
    template_name = 'user/mypage_alert.html'
    context_object_name = 'alerts'

    def get_queryset(self):
        if self.request.user == AnonymousUser():
            return HttpResponse('비정상적인 접근입니다.')
        alerts = Alert.objects.filter(user=self.request.user).order_by('-time')
        return alerts

# (Superuser) Periodic Tasks


def periodic_tasks(request):
    if request.user.is_superuser:
        if PERIODIC_TASKS_TIMER.timer != None:
            messages.success(request, "이미 DB 관리가 진행되고 있습니다.")
        else:
            PERIODIC_TASKS_TIMER.timer = Timer(
                initial_period(datetime.now()), periodic_tasks_execute)
            PERIODIC_TASKS_TIMER.timer.start()
            messages.success(request, "DB 관리가 성공적으로 진행되고 있습니다.")
        return redirect('user:mypage')
    return redirect('user:login')


# (Superuser) Periodic Tasks Immediate

def periodic_tasks_immediate(request):
    if request.user.is_superuser:
        periodic_tasks_execute_once()
        messages.success(request, "DB 관리가 이루어졌습니다.")
        return redirect('user:mypage')
    return redirect('user:login')

# (Superuser) Initialize Rewards


def initialize_rewards(request):
    if request.user.is_superuser:
        initializeReward()
        messages.success(request, "업적 업데이트가 성공적으로 이루어졌습니다.")
        return redirect('user:mypage')
    return redirect('user:login')

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
    all_alert_id.reverse()
    return JsonResponse({'all_alert_id': all_alert_id})


# Load New Alert (Ajax)
@csrf_exempt
def load_new_alert_ajax(request):
    try:
        new_alert = Alert.objects.filter(
            user=request.user, checked=False).order_by('-time')[2]
    except:
        return JsonResponse({'new_alert_id': 0, 'new_alert_content': "",
                             'new_alert_related_url': ""})
    return JsonResponse({'new_alert_id': new_alert.id, 'new_alert_content': new_alert.content,
                         'new_alert_related_url': new_alert.related_url()})


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
    if request.user == AnonymousUser():
        return redirect('user:login')
    view_user = get_object_or_404(User, pk=pk)

    rewards = GetReward.objects.filter(
        user=view_user).order_by('-get_date')[:5]
    questions = Question.objects.filter(
        user=view_user).order_by('-updated_at')[:5]
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


# Password Change (Email Search)
def password_change_search(request):
    if request.method == 'POST':
        if User.objects.filter(email=request.POST['email']):
            user = User.objects.get(email=request.POST['email'])
            # 이메일 발송
            current_site = get_current_site(request)
            message = render_to_string('user/user_password_change_email.html',
                                       {
                                           'user': user,
                                           'domain': current_site.domain,
                                           'uid': urlsafe_base64_encode(force_bytes(user.pk)).encode().decode(),
                                           'token': user_activation_token.make_token(user),
                                       }
                                       )
            mail_subject = '[도와줘, 코딩] 비밀번호 변경 메일입니다.'
            email = EmailMessage(mail_subject, message, to=[user.email])
            email.send()
            return render(request, 'user/password_change_email_sent.html', {'email': request.POST['email']})
        else:
            form = PasswordChangeForm(request.POST)
            return render(request, 'user/password_change_search.html', {'form': form, 'original_email': request.POST['email'], 'search_error': '해당 이메일의 유저가 없어요.'})
    form = PasswordChangeSearchForm()
    return render(request, 'user/password_change_search.html', {'form': form, 'original_email': '', 'search_error': ''})

# Password Change


def password_change(request, uid64, token):
    uid = force_str(urlsafe_base64_decode(uid64))
    user = get_object_or_404(User, pk=uid)
    if user is not None and request.method == 'POST':
        password_change_error = ErrorMessages()
        password_change_error.validation_check('', '', '',
                                               request.POST['new_password1'],
                                               request.POST['new_password2'],
                                               '', '', '', '', '',
                                               ['password_forgotten']
                                               )
        if not password_change_error.has_error():
            user.set_password(request.POST['new_password1'])
            user.save()
            return render(request, 'user/password_change_success.html', {'email': user.email})

        original_information = OriginalInformation()
        original_information.remember(request, ['password_forgotten'])
        form = PasswordChangeForm(request.POST)
        return render(request, 'user/password_change.html', {'form': form, 'original_information': original_information, 'password_change_error': password_change_error})

    elif user is not None and request.method == 'GET':
        form = PasswordChangeForm()
        return render(request, 'user/password_change.html', {'form': form, 'original_information': ''})

    else:
        return HttpResponse('비정상적인 접근입니다.')
