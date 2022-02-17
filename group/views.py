from calendar import c
from email import message
import re
from tkinter import E
from tokenize import blank_re
import uuid
import base64
import codecs
import json
import shutil
import os
import mimetypes
import time
from django.shortcuts import render, redirect, get_object_or_404
from django.templatetags.static import static
from django.db.models import Q, F
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import JsonResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from .models import *
from .forms import *
from django.core.paginator import Paginator
from hitcount.views import HitCountDetailView
from django.views.generic import ListView, View
from django.views.generic.detail import SingleObjectMixin
from django.core.files.storage import FileSystemStorage
from config.settings import MEDIA_ROOT
from user.update import *
from .iframe import *
from threading import Timer
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


######## 그룹 메인 페이지 ########

# 나의 그룹


def group_home(request):
    user = request.user  # 현재 접속한 사용자

    # 해당 유저의 그룹 리스트
    groups = user.group_set.all()
    group_star = Group.objects.filter(star_group__user=user)
    # group_star = GroupStar.objects.filter(group=groups)

    # 정렬하기
    sort_by = request.GET.get('sort', 'star')
    if sort_by == 'name':
        groups = groups.order_by('name', '-id')
    elif sort_by == 'star':  # filter -> 정렬
        dict = {}
        for group in groups:
            dict[group] = group.star_group.filter(user=user).count()
        groups = sorted(groups, key=lambda group: dict[group], reverse=True)

    # for group_star in groups:
    #     if is_star = 'True':
    #         groups_star_dict[group_star] = is_star

    # 페이징 처리
    page = request.GET.get('page', '1')

    # user의 닉네임이랑 같은 경우에 처리해야 하는 부분 이후 추가
    pagintor = Paginator(groups, 6)
    page_obj = pagintor.get_page(page)

    groups_star_dict = {}
    for group in page_obj:
        if group in group_star:
            groups_star_dict[group] = True
        else:
            groups_star_dict[group] = False

    ctx = {
        'user': user,  # 나중에는 쓸모 X
        'groups': page_obj,
        'groups_star_dict': groups_star_dict,
        'sort_by': sort_by,
        'ani_image': static('image/helphelp.png')
    }

    return render(request, template_name='group/group_home.html', context=ctx)


# 그룹 검색하기(공개 그룹 찾기)
def group_search_public(request):
    if 'search' in request.GET:
        query = request.GET.get('search')
        groups = Group.objects.all().filter(Q(name__icontains=query) & Q(mode='PUBLIC'))

    sort_by = request.GET.get('sort', 'interest')
    if sort_by == 'name':
        groups = groups.order_by('name')
    elif sort_by == 'interest':
        groups = groups.annotate(total_likes=Count(
            'interests')).order_by('-total_likes')
    elif sort_by == 'member':
        groups = groups.annotate(total_members=Count(
            'members')).order_by('-total_members')

    # 페이징 처리
    page = request.GET.get('page', '1')
    paginator = Paginator(groups, 6)    # 페이지당 6개씩 보여주기
    page_obj = paginator.get_page(page)

    ctx = {
        'groups': page_obj,
        'query': query,
        'ani_image': static('image/helphelp.png'),
        'sort_by': sort_by,
    }

    return render(request, 'group/group_search_public.html', context=ctx)


######## 그룹 CRUD ########

# 그룹 생성
def group_create(request):
    user = request.user

    if request.method == 'POST':
        form = GroupForm(request.POST, request.FILES)

        name = request.POST.get('name')
        image = request.FILES.get('image')
        mode = request.POST.get('group-mode__tag')

        # 에러 메세지
        error = GroupErrorMessage()
        error.validation_group(name, mode, '', 'group_create')

        if not error.has_error_group() and form.is_valid():
            group = form.save()
            os.makedirs(
                MEDIA_ROOT + '/group_{}/thumbnail/'.format(group.pk), exist_ok=True)
            group.mode = mode
            group.maker = user    # 방장 = 접속한 유저
            group.members.add(user)  # 방장도 그룹의 멤버로 추가

            if request.FILES.get('image'):  # form valid + 이미지 첨부 시
                group.image = request.FILES.get('image')
            elif request.POST['img_recent']:
                os.makedirs(MEDIA_ROOT + '/temp/', exist_ok=True)
                shutil.copyfile('./media/temp/{}'.format(request.POST['img_recent']),
                                './media/group_{}/thumbnail/{}'.format(group.pk, request.POST['img_recent']))
                group.image = './group_{}/thumbnail/{}'.format(
                    group.pk, request.POST['img_recent'])
            group.save()
            update_group_create(group, user)

            return redirect('group:group_home')

        original_info = OriginalGroupInfo()
        original_info.remember(request)
        # 다른 필드 에러 시(기존 파일 남아있도록)
        if request.FILES.get('image'):
            os.makedirs(MEDIA_ROOT + '/temp/', exist_ok=True)
            with open('./media/temp/{}'.format(request.FILES.get('image')), 'wb+') as destination:
                for chunk in request.FILES['image'].chunks():
                    destination.write(chunk)

        original_info.image = request.POST['img_recent']

        ctx = {
            'error': error,
            'origin': original_info,
            'temp_img_location': '/media/temp/'
        }

        return render(request, template_name='group/group_form.html', context=ctx)

    else:
        form = GroupForm()
        users = User.objects.all()
        # users = User.objects.exclude(user)
        # form.fields['maker'].queryset = users
        ctx = {'form': form, 'temp_img_location': '/media/temp/'}

        return render(request, 'group/group_form.html', context=ctx)

# 그룹 정보 수정


def group_update(request, pk):
    group = get_object_or_404(Group, pk=pk)
    prev_name = group.name

    if request.method == 'POST':
        form = GroupForm(request.POST, instance=group)

        group.name = request.POST.get('name')
        name = group.name

        group.intro = request.POST.get('intro')
        intro = group.intro
        #os.makedirs(MEDIA_ROOT + '/group_{}/thumbnail/'.format(group.pk), exist_ok=True)
        # shutil.copyfile('./media/temp/{}'.format(request.POST['img_recent']),
        # './media/group_{}/thumbnail/{}'.format(group.pk, request.POST['img_recent']))

        # # 기존 이미지는 유지
        # if group.image:
        #     image = request.POST.get('image')

        # if request.FILES.get('image'):
        #     image = request.FILES.get('image')
        #     group.image = image
        #     group.save()

        mode = request.POST.get('group-mode__tag')
        group.mode = mode

        original_info = OriginalGroupInfo()
        original_info.remember(request)
        # 에러 메세지
        error = GroupErrorMessage()
        error.validation_group(name, mode, prev_name, 'group_update')

        if not error.has_error_group():
            group.intro = request.POST.get('intro')
            if request.FILES.get('image'):  # form valid 시
                group.image = request.FILES.get('image')

            else:   # 다른 필드 에러 시(기존 파일 남아있도록)
                group.image = './group_{}/thumbnail/{}'.format(
                    group.pk, request.POST['img_recent'])
                # original_info.image = request.POST['img_recent']

            group.save()

            return redirect('group:group_detail', pk)

        # 에러 메세지가 존재할 때
        if request.FILES.get('image'):
            #os.makedirs(MEDIA_ROOT + '/temp/', exist_ok=True)
            with open('/group_{}/thumbnail/{}'.format(group.pk, request.FILES.get('image')), 'wb+') as destination:
                for chunk in request.FILES['image'].chunks():
                    destination.write(chunk)

        original_info.image = request.POST['img_recent']

        if group.image:
            current_image = group.image.url.split('/')[-1]
        else:
            current_image = ''

        ctx = {
            'error': error,
            'origin': original_info,
            'current_image': current_image,
            'temp_img_location': '/media/group_{}/thumbnail/'.format(group.pk)
        }

        return render(request, template_name='group/group_form.html', context=ctx)

    else:
        form = GroupForm(instance=group)

        # try:
        #     current_image = '/media/group_{}/thumbnail/'.format(group.pk)
        # except:
        #     pass
        if group.image:
            current_image = group.image.url.split('/')[-1]
        else:
            current_image = ''

        ctx = {
            'group': group,
            'form': form,
            'current_image': current_image,
            'temp_img_location': '/media/group_{}/thumbnail/'.format(group.pk)
        }

        return render(request, template_name='group/group_form.html', context=ctx)

# 그룹 삭제


def group_delete(request, pk):
    user = request.user
    group = get_object_or_404(Group, pk=pk)

    if user == group.maker:
        update_delete_group(group)
        group.delete()

        return redirect('group:group_home')

    # else:
    #     ### 알림 창 하나 띄우기(alert) "방장만 그룹을 삭제할 수 있습니다."
    #     return redirect('group:group_detail', pk)

# 그룹 탈퇴


def group_drop(request, pk):
    user = request.user
    group = get_object_or_404(Group, pk=pk)
    members = group.members.all()

    if len(members) > 1:
        if user == group.maker:
            # group.members.remove(user)
            group.members.remove(user)
            # group.maker = members[0]   #랜덤하게 지정해야 하나..?
            # 그룹 대표를 넘겨줄 때
            update_change_group_maker(group, user, group.members.all()[0])
            # 이거 구현하면 윗줄 new_maker 부분에 새 대표 넣고 주석해제 해주세요! (-찬영)
            group.save()
            # group.maker = members[0]
            # group.save()

        else:
            update_drop_group(group, user)
            group.members.remove(user)

    else:
        update_delete_group(group)
        group.delete()

        # group_delete(request, pk)  # 그룹 삭제 함수 호출
    return redirect('group:group_home')

# 그룹 상세 페이지


def group_detail(request, pk):
    user = request.user
    group = get_object_or_404(Group, pk=pk)

    group_star = GroupStar.objects.filter(Q(group=group) & Q(user=user))
    if GroupStar.objects.filter(Q(group=group) & Q(user=user)):
        is_star = True
    else:
        is_star = False

    mygroup = user.group_set.all()
    members = group.members.all()
    waits = group.waits.all()
    if group.maker in members:
        maker = group.maker
    else:
        group.maker = members[0]
        maker = group.maker
    group.save()

    total_likes = len(group.interests.all())
    is_liked = user in group.interests.all()

    ctx = {
        'group': group,
        'mygroup': mygroup,
        'members': members,
        'waits': waits,
        'maker': maker,
        'total_likes': total_likes,
        'is_liked': is_liked,
        'user': user,
        'is_star': is_star,
        'ani_image': static('image/helphelp.png'),
        'profile_img': static('image/none_image_user.jpeg'),
    }

    return render(request, template_name='group/group_detail.html', context=ctx)


def group_member_state(request):
    user = request.user
    groups = Group.objects.all()
    mygroup = user.group_set.all()

    for group in groups:
        print(group.waits)
        for wait in group.waits:
            print(wait.nickname)
    print(groups_wait)
    group_wait = []
    wait_status = ''

    for group in groups:
        if user in groups_wait:
            group_wait.append(group)
            wait_status = '가입 대기중 ...'
        elif group == mygroup:
            wait_status = '가입 완료!'

    ctx = {
        'user': user,
        'groups': group_wait,
        'wait_status': wait_status
    }

    return render(request, template_name='group/group_member_state.html', context=ctx)

######## 그룹 생성 Form 오류 사항 체크 ########


class GroupErrorMessage():

    name, mode = '', ''

    def validation_group(self, name, mode, prev, command):

        # 미입력 시 에러 메세지
        if 'group_create' == command or 'group_update' == command:
            if not name:
                self.name = '그룹 이름을 입력하세요.'
            if not (mode in ['PUBLIC', 'PRIVATE']):
                self.mode = '그룹 공개모드를 선택하세요.'

        # 기존에 있던 입력과 비교
        if 'group_update' == command:
            if name != prev:
                if Group.objects.filter(name=name):
                    self.name = '이미 사용 중인 그룹 이름이에요.'
        elif 'group_create' == command:
            if Group.objects.filter(name=name):
                self.name = '이미 사용 중인 그룹 이름이에요.'

    def has_error_group(self):
        return self.name or self.mode

# Group Form에서 오류 발생 시 남아있는 정보


class OriginalGroupInfo():

    def remember(self, request):
        self.name = request.POST['name']
        self.intro = request.POST['intro']
        self.image = request.FILES.get('image')
        self.mode = request.POST.get('group-mode__tag')


######## 초대 코드 ########
# 7일의 코드 유효 기간
def group_code_save(pk):
    group = get_object_or_404(Group, pk=pk)
    group.code = get_invite_code()
    group.save()

    time = Timer(7 * 24 * 60 * 60, group_code_save, [group.pk])
    time.start()

    return group.code

# 초대 코드 발급


def get_invite_code(length=6):
    return base64.urlsafe_b64encode(
        codecs.encode(uuid.uuid4().bytes, 'base64').rstrip()
    ).decode()[:length]

# 초대 코드 생성 (from 상세 페이지)


@csrf_exempt
def create_code_ajax(request):
    req = json.loads(request.body)
    group_id = req['groupId']

    group = get_object_or_404(Group, pk=group_id)
    if group.code != None:
        code = group.code
    else:
        # time = Timer(7 * 24 * 60 * 60, group_code_save, [group_id])
        code = group_code_save(group_id)
        # code = group.code

        if time.finished:
            group.code = ''
    print(code)
    group.save()

    return JsonResponse({'name': group.name, 'code': code})


# 초대 코드 입력하기 (나의 그룹 홈페이지)
@csrf_exempt
def join_code_ajax(request):
    req = json.loads(request.body)

    user = request.user
    input_code = req['code']
    mygroup = list(user.group_set.all())
    message = ''

    try:
        if input_code != None:
            group = get_object_or_404(Group, code=input_code)
            if group in mygroup:
                message = '이미 가입된 그룹입니다.'
            else:
                group.members.add(user)
                # update -> 비공개 그룹 가입
                group.save()
                message = '가입에 성공했습니다.'
                update_private_group_join(group, user)

        else:
            message = '가입에 성공했습니다.'

    except:
        message = '존재하지 않는 코드입니다.'

    return JsonResponse({'message': message})


######## 공개 그룹 ########

# 그룹 모아보기 게시판(그룹 찾기)
def group_list(request):
    group = Group.objects.filter(mode='PUBLIC')
    # group = Group.objects.all()
    groups = group.order_by('name')
    # 페이징 처리
    page = request.GET.get('page', '1')

    sort_by = request.GET.get('sort', 'interest')
    if sort_by == 'name':
        groups = groups.order_by('name')
    elif sort_by == 'interest':
        groups = groups.annotate(total_likes=Count(
            'interests')).order_by('-total_likes')
    elif sort_by == 'member':
        groups = groups.annotate(total_members=Count(
            'members')).order_by('-total_members')

    pagintor = Paginator(groups, 6)
    page_obj = pagintor.get_page(page)

    ctx = {
        'groups': page_obj,
        'sort_by': sort_by,
        'ani_image': static('image/helphelp.png')
    }

    return render(request, template_name='group/group_list.html', context=ctx)

# 그룹 가입하기


def public_group_join(request, pk):
    user = request.user
    group = get_object_or_404(Group, pk=pk)
    members = group.members.all()

    if user not in members:
        # if user not in group.waits: (하고서 밑 부분 3개 들여쓰기)
        group.waits.add(user)
        group.save()
        update_public_group_register(group, user)
        # 혹시 이거 user이 group.waits에 있는지 확인하는 코드는 어떨까?

    return redirect('group:group_detail', pk)

# 가입 클릭 후 취소


def group_wait_cancel(request, pk):
    user = request.user
    group = get_object_or_404(Group, pk=pk)
    members = group.members.all()
    waits = group.waits.all()

    if user not in members and user in waits:
        group.waits.remove(user)
        group.save()

    return redirect('group:group_detail', pk)

# 수락 선택 시


@csrf_exempt
def group_join_accept(request):
    req = json.loads(request.body)
    group_id = req['groupId']
    wait_user_id = req['userId']

    wait_user = get_object_or_404(User, pk=wait_user_id)
    group = get_object_or_404(Group, pk=group_id)

    wait_id = wait_user.id
    group.waits.remove(wait_user)
    group.members.add(wait_user)
    group.save()
    update_public_group_join(group, wait_user)
    return JsonResponse({
        'userId': wait_id
    })

# 거절 선택 시


@csrf_exempt
def group_join_reject(request):
    req = json.loads(request.body)
    group_id = req['groupId']
    wait_user_id = req['userId']

    wait_user = get_object_or_404(User, pk=wait_user_id)
    group = get_object_or_404(Group, pk=group_id)

    wait_id = wait_user.id

    group.waits.remove(wait_user)
    group.save()
    update_public_group_reject(group, wait_user)
    # update -> 거절됨

    return JsonResponse({
        'userId': wait_id
    })


# 그룹 가입 대기자 명단
@csrf_exempt
def wait_list_ajax(request):
    req = json.loads(request.body)
    group_id = req['id']
    group = get_object_or_404(Group, pk=group_id)
    waits = group.waits.all()
    wait_member_name = []   # 대기자 명단 이름 배열
    wait_member_img = []   # 대기자 명단 이미지 배열
    wait_member_id = []

    for wait_member in waits:
        wait_member_name.append(wait_member.nickname)
        wait_img_url = wait_member.img.url if wait_member.img else ''
        wait_member_img.append(wait_img_url)
        wait_member_id.append(wait_member.id)

        if request.GET.get('accept'):
            group.waits.remove(wait_member)
            group.members.add(wait_member)
            group.save()
        elif request.GET.get('reject'):
            group.waits.remove(wait_member)
            group.save()

    return JsonResponse({
        'groupName': group.name,
        'waitsName': wait_member_name,
        'waitsImg': wait_member_img,
        'waitsId': wait_member_id,
    })


# 공개그룹 대기자 수락 여부
# @csrf_exempt
# def wait_member_accept(request):
#     req = json.loads(request.body)
#     user_id = req['userId']
#     waits = group.waits.

#     if request.GET.get('accept'):
#         group.waits.remove(wait)
#         group.members.add(wait)
#         group.save()
#     elif request.GET.get('reject'):
#         group.waits.remove(wait)
#         group.save()

#     return 1


######################### 그룹 내 커뮤니티 게시판 ##############################
# Error messages

# TODO : validation 체크할 때 request 객체와 form을 넘겨주는 건 어떨까요?
# TODO : 넘겨주는 인자가 너무 많고, 순서 헷갈릴 여지도 있어보입니다.

class GroupPostErrorMessages():
    title, content, image, attached_file, attached_link, category = '', '', '', '', '', ''

    def validation_check(self, request, command):
        title = request.POST.get('title')
        content = request.POST.get('content')
        attached_link = request.POST.get('attached_link')
        category = request.POST.get('category')
        if 'create' in command or 'update' in command:
            if not title:
                self.title = '제목을 입력해주세요'
            elif len(title) > 50:
                self.title = '제목은 50자 이내로 입력해주세요'
            if not content:
                self.content = '내용을 입력해주세요'
            if not category:
                self.category = '카테고리를 선택해주세요'
            if attached_link:
                val = URLValidator()
                try:
                    val(attached_link)
                except:
                    self.attached_link = '잘못된 링크입니다.'

    def has_error(self):
        return self.title or self.content or self.image or self.attached_file or self.attached_link or self.category


class OriginalInformation():
    def remember(self, request, command):
        self.title = request.POST.get('title')
        self.content = request.POST.get('content')
        self.image = request.FILES.get('image')
        self.attached_file = request.FILES.get('attached_file')
        self.category = request.POST.get('category')
        self.attached_link = request.POST.get('attached_link')
        self.command = command

# 게시글 목록


def post_list(request, pk):
    posts = GroupPost.objects.filter(group__pk=pk).order_by('-created_at')
    group = Group.objects.get(pk=pk)
    page = request.GET.get('page', '1')    # 페이지

    # 게시글 필터
    filter_by_list = request.GET.getlist('filter_by')
    if filter_by_list:
        num = len(filter_by_list)
        if num == 1:
            posts = posts.filter(category=filter_by_list[0])
        elif num == 2:
            posts = posts.filter(Q(category=filter_by_list[0]) | Q(
                category=filter_by_list[1]))
        elif num == 3:
            pass

    # 게시물 정렬
    sort_by = request.GET.get('sort', 'recent')
    if sort_by == 'recent':    # 최신순
        posts = posts.order_by('-created_at')
    elif sort_by == 'liked':   # 좋아요순
        posts = posts.annotate(total_likes=Count(
            'like_user')).order_by('-total_likes')
    elif sort_by == 'view':    # 조회수순
        posts = posts.order_by('-hit_count_generic__hits')

    # 페이징 처리
    paginator = Paginator(posts, 6)    # 페이지당 6개씩 보여주기
    page_obj = paginator.get_page(page)

    # 각 게시글과 iframe 관련 썸네일의 이미지 경로 딕셔너리 생성
    # key 는 각 게시글이고, value는 (댓글 수, 썸네일 이미지 경로) tuple인 딕셔너리
    posts_value_dict = {}
    for page in page_obj:
        answers_count = GroupAnswer.objects.filter(
            post_id=page, answer_depth=0, is_deleted=False).count()

        if page.attached_link:
            posts_value_dict[page] = (
                answers_count, get_img_src(page.attached_link))
        else:
            posts_value_dict[page] = (answers_count, None)

    ctx = {
        'posts': page_obj,
        'posts_value_dict': posts_value_dict,
        'group': group,
        'sort_by': sort_by,
        'filter_by': filter_by_list,
    }
    return render(request, 'group/group_post_list.html', context=ctx)

# 게시글 검색


def search_result(request, pk):
    if 'search' in request.GET:
        group = Group.objects.get(pk=pk)
        query = request.GET.get('search')
        posts = GroupPost.objects.filter(group__pk=pk).filter(
            Q(title__icontains=query) |  # 제목으로 검색
            Q(content__icontains=query)  # 내용으로 검색
        )

    # 게시물 정렬
    sort_by = request.GET.get('sort', 'recent')
    if sort_by == 'recent':    # 최신순
        posts = posts.order_by('-created_at')
    elif sort_by == 'liked':   # 좋아요순
        posts = posts.annotate(total_likes=Count(
            'like_user')).order_by('-total_likes')
    elif sort_by == 'view':    # 조회수순
        posts = posts.order_by('-hit_count_generic__hits')

    # 페이징 처리
    page = request.GET.get('page', '1')
    paginator = Paginator(posts, 6)    # 페이지당 6개씩 보여주기
    page_obj = paginator.get_page(page)

    # 각 게시글과 iframe 관련 썸네일의 이미지 경로 딕셔너리 생성
    # key 는 각 게시글이고, value는 (댓글 수, 썸네일 이미지 경로) tuple인 딕셔너리
    posts_value_dict = {}
    for page in page_obj:
        answers_count = GroupAnswer.objects.filter(
            post_id=page, answer_depth=0, is_deleted=False).count()

        if page.attached_link:
            posts_value_dict[page] = (
                answers_count, get_img_src(page.attached_link))
        else:
            posts_value_dict[page] = (answers_count, None)

    ctx = {
        'query': query,
        'posts': page_obj,
        'posts_value_dict': posts_value_dict,
        'group_pk': pk,
        'group': group,
        'sort_by': sort_by,
    }

    return render(request, 'group/search_result.html', context=ctx)

# 게시글 작성


def post_create(request, pk):
    group = get_object_or_404(Group, pk=pk)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        error_messages = GroupPostErrorMessages()
        error_messages.validation_check(request, ['create'])
        if not error_messages.has_error():
            post = GroupPost.objects.create(
                title=request.POST.get('title'),
                content=request.POST.get('content'),
                # image=request.FILES.get('image'),
                # attached_file=request.FILES.get('attached_file'),
                attached_link=request.POST.get('attached_link'),
                category=request.POST.get('category'),
                user=request.user,
                group=group
            )
            os.makedirs(
                MEDIA_ROOT + '/group_{}/image/'.format(group.pk), exist_ok=True)
            os.makedirs(
                MEDIA_ROOT + '/group_{}/file/'.format(group.pk), exist_ok=True)

            if request.FILES.get('image'):
                post.image = request.FILES.get('image')
            elif request.POST['img_recent']:
                os.makedirs(MEDIA_ROOT + '/temp/', exist_ok=True)
                shutil.copyfile('./media/temp/{}'.format(request.POST['img_recent']),
                                './media/group_{}/image/{}'.format(group.pk, request.POST['img_recent']))
                post.image = './group_{}/image/{}'.format(
                    group.pk, request.POST['img_recent'])

            if request.FILES.get('attached_file'):
                post.attached_file = request.FILES.get('attached_file')
            elif request.POST['file_recent']:
                os.makedirs(MEDIA_ROOT + '/temp/', exist_ok=True)
                shutil.copyfile('./media/temp/{}'.format(request.POST['file_recent']),
                                './media/group_{}/file/{}'.format(group.pk, request.POST['file_recent']))
                post.attached_file = './group_{}/file/{}'.format(
                    group.pk, request.POST['file_recent'])

            post.save()
            update_group_post(post, request.user)

            return redirect('group:post_detail', pk, post.pk)
        else:
            original_information = OriginalInformation()
            original_information.remember(request, ['create'])

            if request.FILES.get('image'):
                os.makedirs(MEDIA_ROOT + '/temp/', exist_ok=True)
                with open('./media/temp/{}'.format(request.FILES['image'].name), 'wb+') as destination:
                    for chunk in request.FILES['image'].chunks():
                        destination.write(chunk)
            if request.FILES.get('attached_file'):
                os.makedirs(MEDIA_ROOT + '/temp/', exist_ok=True)
                with open('./media/temp/{}'.format(request.FILES['attached_file'].name), 'wb+') as destination:
                    for chunk in request.FILES['attached_file'].chunks():
                        destination.write(chunk)

            original_information.image = request.POST['img_recent']
            original_information.attached_file = request.POST['file_recent']

            ctx = {
                'form': form,
                'error_messages': error_messages,
                'original_information': original_information,
                'group': group,
                'temp_img_location': '/media/temp/',
                'temp_file_location': '/media/temp/',
            }
            return render(request, 'group/group_post_form.html', context=ctx)

    else:
        form = PostForm()
        ctx = {
            'form': form,
            'group': group,
            'temp_img_location': '/media/temp/',
            'temp_file_location': '/media/temp/',
        }

        return render(request, 'group/group_post_form.html', context=ctx)


def post_update(request, pk, post_pk):
    post = get_object_or_404(GroupPost, pk=post_pk)
    group = get_object_or_404(Group, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)

        error_messages = GroupPostErrorMessages()
        error_messages.validation_check(request, ['create'])
        if not error_messages.has_error():
            if request.FILES.get('image'):  # form valid 시
                post.image = request.FILES.get('image')

            else:   # 다른 필드 에러 시(기존 파일 남아있도록)
                post.image = './group_{}/image/{}'.format(
                    group.pk, request.POST['img_recent'])
            if request.FILES.get('attached_file'):  # form valid 시
                post.attached_file = request.FILES.get('attached_file')

            else:   # 다른 필드 에러 시(기존 파일 남아있도록)
                post.attached_file = './group_{}/file/{}'.format(
                    group.pk, request.POST['file_recent'])

            post = form.save()

            return redirect('group:post_detail', pk, post.pk)
        else:
            if request.FILES.get('image'):
                with open('/group_{}/image/{}'.format(group.pk, request.FILES.get('image')), 'wb+') as destination:
                    for chunk in request.FILES['image'].chunks():
                        destination.write(chunk)
            if request.FILES.get('attached_file'):
                with open('/group_{}/file/{}'.format(group.pk, request.FILES.get('attached_file')), 'wb+') as destination:
                    for chunk in request.FILES['attached_file'].chunks():
                        destination.write(chunk)

            original_information = OriginalInformation()
            original_information.remember(request, ['update'])

            original_information.image = request.POST['img_recent']
            original_information.attached_file = request.POST['file_recent']

            if post.image:
                current_image = post.image.url.split('/')[-1]
            else:
                current_image = ''
            if post.attached_file:
                current_file = post.attached_file.url.split('/')[-1]
            else:
                current_file = ''

            ctx = {
                'form': form,
                'error_messages': error_messages,
                'original_information': original_information,
                'group': group,
                'current_image': current_image,
                'temp_img_location': '/media/group_{}/image/'.format(group.pk),
                'current_file': current_file,
                'temp_file_location': '/media/group_{}/file/'.format(group.pk),
            }
            return render(request, 'group/group_post_form.html', context=ctx)
    else:
        form = PostForm(instance=post)

        if post.image:
            current_image = post.image.url.split('/')[-1]
        else:
            current_image = ''
        if post.attached_file:
            current_file = post.attached_file.url.split('/')[-1]
        else:
            current_file = ''

        ctx = {
            'form': form,
            'post': post,
            'group': group,
            'current_image': current_image,
            'temp_img_location': '/media/group_{}/image/'.format(group.pk),
            'current_file': current_file,
            'temp_file_location': '/media/group_{}/file/'.format(group.pk),
        }

        return render(request, template_name="group/group_post_form.html", context=ctx)


class GroupPostDetailView(HitCountDetailView):
    model = GroupPost
    template_name = 'group/group_post_detail.html'
    count_hit = True
    context_object_name = 'post'

    def get_context_data(self, **kargs):
        context = super().get_context_data(**kargs)
        # self.object로 GroupPost 객체에 접근할 수 있음
        try:
            previous_pk = GroupPost.get_previous_by_created_at(
                self.object, group=self.object.group).pk
        except:
            # 이전글 없을 때
            previous_pk = -1
        try:
            next_pk = GroupPost.get_next_by_created_at(
                self.object, group=self.object.group).pk
        except:
            # 이전글 없을 때
            next_pk = -1
        context['next_pk'] = next_pk
        context['previous_pk'] = previous_pk

        post = self.object

        if post.user:
            username = self.object.user.nickname
        else:
            username = '(알 수 없음)'

        ## 그룹 탈퇴한 유저인지 여부

        if post.user in post.group.members.all():
            is_member = True
        else: is_member = False

        total_likes = len(post.like_user.all())
        is_liked = self.request.user in post.like_user.all()

        # 해당 게시글에 대한 답변 가져오기
        answers = GroupAnswer.objects.filter(post_id=post.id, parent_answer__isnull=True).order_by(
            'answer_order')  # 나중에 답변 정렬도 고려. 최신순 또는 좋아요 순
        answers_count = len(answers)

        answers_reply_dict = {}
        for answer in answers:
            replies = GroupAnswer.objects.filter(
                parent_answer=answer).order_by('answer_order')
            answers_reply_dict[answer] = replies

        # iframe
        iframe_url = post.attached_link
        iframe = get_iframe(iframe_url, 800, 600)
        context['iframe'] = iframe

        ####

        context['group'] = post.group
        context['username'] = username
        context['total_likes'] = total_likes
        context['is_liked'] = is_liked
        # context['answers']= answers
        context['answers_count'] = answers_count
        context['answers_reply_dict'] = answers_reply_dict
        context['is_member'] = is_member
        return context


class FileDownloadView(SingleObjectMixin, View):
    queryset = GroupPost.objects.all()

    def get(self, request, pk):
        object = get_object_or_404(GroupPost, pk=pk)

        file_path = object.attached_file.path
        file_type, _ = mimetypes.guess_type(file_path)
        # file_type = object.attached_file.name.split('.')[-1]  # django file object에 content type 속성이 없어서 따로 저장한 필드
        fs = FileSystemStorage(file_path)
        response = FileResponse(
            fs.open(file_path, 'rb'), content_type=file_type)
        response['Content-Disposition'] = f'attachment; filename={object.get_filename()}'

        return response


def post_delete(request, pk, post_pk):
    post = get_object_or_404(GroupPost, pk=post_pk)
    post.delete()
    return redirect('group:post_list', pk)


@csrf_exempt
def answer_ajax(request):
    req = json.loads(request.body)
    post_id = req['postId']
    content = req['content']
    user_id = req['user']
    user = get_object_or_404(User, pk=user_id)
    username = user.nickname
    user_image_url = user.img.url if user.img else ''

    this_post = get_object_or_404(GroupPost, pk=post_id)
    # 작성자 여부
    if this_post.user == None:
        is_author = False
    elif user_id == this_post.user.pk:
        is_author = True
    else:
        is_author = False

    # 새 답변의 order 필드를 정해주기 위한 부분.
    current_answers = GroupAnswer.objects.filter(
        post_id=post_id).order_by('answer_order')
    if len(current_answers) == 0:
        new_order = 1
    else:
        new_order = current_answers.last().answer_order + 1

    # 새로운 답변
    new_answer = GroupAnswer.objects.create(
        post_id=this_post,
        content=content,
        answer_order=new_order,
        answer_depth=0,
        user=user)
    # 템플릿에서 쉽게 띄울 수 있도록 답변 게시일자 포맷팅해서 json에 전달
    created_at = new_answer.created_at.strftime('%y.%m.%d %H:%M')
    update_group_comment(this_post, new_answer, this_post.user, user)

    return JsonResponse({
        'id': new_answer.id,
        'content': content,
        'user': username,
        'created_at': created_at,
        'user_image_url': user_image_url,
        'is_author': is_author,
    })

# 대댓글 작성


@csrf_exempt
def reply_ajax(request):
    req = json.loads(request.body)

    answer_id = req['answerId']
    content = req['content']
    user_id = req['user']
    user = get_object_or_404(User, pk=user_id)
    username = user.nickname

    # 작성하려는 대댓글이 속한 질문 구하기
    this_answer = get_object_or_404(GroupAnswer, pk=answer_id)
    this_post = this_answer.post_id

    user_image_url = user.img.url if user.img else ''
    # 작성자 여부
    if this_post.user == None:
        is_author = False
    elif user_id == this_post.user.pk:
        is_author = True
    else:
        is_author = False

    # 새 답변의 order 필드를 정해주기 위한 부분.
    current_answers = GroupAnswer.objects.filter(
        post_id=this_post.id).order_by('answer_order')
    if len(current_answers) == 0:
        new_order = 1
    else:
        new_order = current_answers.last().answer_order + 1

    # 새로운 대댓글
    new_answer = GroupAnswer.objects.create(
        post_id=this_post,
        content=content,
        answer_order=new_order,
        answer_depth=1,
        user=user,
        parent_answer=this_answer
    )

    # 템플릿에서 쉽게 띄울 수 있도록 답변 게시일자 포맷팅해서 json에 전달
    created_at = new_answer.created_at.strftime('%y.%m.%d %H:%M')

    update_group_comment_reply(this_post, new_answer, user)

    response = JsonResponse({
        'reply_id': new_answer.id,
        'answer_id': this_answer.id,
        'content': content,
        'user': username,
        'created_at': created_at,
        'user_image_url': user_image_url,
        'is_author': is_author,
    })

    return response


# 게시글(질문) 좋아요 기능
@csrf_exempt
def post_like_ajax(request):
    req = json.loads(request.body)
    # user id 는 요청 안 보내도 됐을 수도
    post_id = req['postId']

    post = get_object_or_404(GroupPost, pk=post_id)
    liked_users = post.like_user

    is_liked = request.user in liked_users.all()

    if is_liked:
        liked_users.remove(request.user)
    else:
        liked_users.add(request.user)

    total_likes = len(liked_users.all())
    return JsonResponse({'post_id': post_id, 'total_likes': total_likes, 'is_liking': not(is_liked)})

# 답변 (대댓글 포함) 좋아요 기능


@csrf_exempt
def answer_like_ajax(request):
    req = json.loads(request.body)
    answer_id = req['id']

    answer = get_object_or_404(GroupAnswer, pk=answer_id)
    liked_users = answer.like_user

    is_liked = request.user in liked_users.all()

    if is_liked:
        liked_users.remove(request.user)
    else:
        liked_users.add(request.user)

    total_likes = len(liked_users.all())

    return JsonResponse({'answer_id': answer_id, 'total_likes': total_likes,  'is_liking': not(is_liked)})


# 답변(대댓글 포함) 삭제
@csrf_exempt
def answer_delete_ajax(request):
    req = json.loads(request.body)
    answer_id = req['id']

    answer = get_object_or_404(GroupAnswer, pk=answer_id)

    # 대댓글이거나 대댓글이 없는 답변의 경우 아예 삭제
    if answer.groupanswer_set.count() == 0:
        # 마지막 대댓글이었다면 부모 답변도 삭제
        if answer.answer_depth == 1 and answer.parent_answer.groupanswer_set.count() == 1 and answer.parent_answer.is_deleted == True:
            answer.parent_answer.delete()

        answer.delete()
        delete_yes = True
    # 답변인 경우 내용만 삭제된 것처럼
    else:
        answer.is_deleted = True
        answer.content = '삭제된 답변입니다.'
        answer.user = None
        answer.save()
        delete_yes = False

    answer_count = GroupAnswer.objects.filter(
        post_id=answer.post_id, is_deleted=False, answer_depth=0).count()

    return JsonResponse({'id': answer_id, 'delete_yes': delete_yes, 'answer_count': answer_count})

# 답변(대댓글 포함) 수정
# 수정버튼 눌렀을 때 해당하는 폼 띄우는 기능


@csrf_exempt
def answer_edit_ajax(request):
    req = json.loads(request.body)
    answer_id = req['id']

    answer = get_object_or_404(GroupAnswer, pk=answer_id)
    # TODO : 고려해볼 사항. 원래 작성되어 있던 내용을 지금은 db에서 찾아서 넘겨주고 있는데
    # 그렇게 말고 data전송을 최소화화면서 프론트 단에서 그냥 현재 입력된 내용 받앙오기

    return JsonResponse({'id': answer_id})

# 답변(대댓글 포함) 수정
# 수정할 내용 입력 후 버튼 눌렀을 때 수정 내용 적용하는 기능


@csrf_exempt
def answer_edit_submit_ajax(request):
    req = json.loads(request.body)
    answer_id = req['id']
    new_content = req['content']
    answer = get_object_or_404(GroupAnswer, pk=answer_id)
    answer.content = new_content
    answer.save()

    return JsonResponse({'id': answer_id, 'content': new_content})


############################################################################

# Ajax
# 내 그룹 - 찜 기능 ajax
# star 클릭 시
@csrf_exempt
def group_star_ajax(request):
    req = json.loads(request.body)
    group_id = req['id']

    user = request.user
    group = get_object_or_404(Group, id=group_id)
    # 1. 그룹 -> 2. 사용자
    group_star = GroupStar.objects.filter(Q(group=group) & Q(user=user))

    if group_star:
        group_star.delete()
        is_star = False
    else:
        GroupStar.objects.create(group=group, user=user)
        is_star = True

    is_stared = is_star

    return JsonResponse({'id': group_id, 'is_star': is_stared})


# 공개 그룹 좋아요 수
@csrf_exempt
def interest_ajax(request):
    req = json.loads(request.body)
    group_id = req['groupId']
    group = get_object_or_404(Group, pk=group_id)
    interests = group.interests

    is_liked = request.user in interests.all()

    if is_liked:
        interests.remove(request.user)
    else:
        interests.add(request.user)

    total_likes = len(interests.all())
    # group.save()

    return JsonResponse({'groupId': group_id, 'total_likes': total_likes, 'is_liked': not(is_liked)})
