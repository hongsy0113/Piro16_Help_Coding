import re
from tokenize import blank_re
import uuid
import base64
import codecs
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.templatetags.static import static
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .forms import *

######## 그룹 메인 페이지 ########

# 나의 그룹
def group_home(request):
    user = request.user  # 현재 접속한 사용자

    # 해당 유저의 그룹 리스트
    groups = Group.objects.filter(members__nickname__contains=user.nickname)
    
    # 정렬하기
    sort = request.GET.get('sort', '')
    if sort == 'name':
        groups = groups.order_by('name')
    elif sort == 'star':
        groups = groups.order_by('-is_star')
    # elif sort == 'member':
    #     groups = groups.order_by('-members')
    # elif sort == 'date':  # django에서 기본 제공하는 create날짜 있는지 체크
    #     groups = groups.order_by('date')
    ### user의 닉네임이랑 같은 경우에 처리해야 하는 부분 이후 추가

    ctx = { 
        'user': user,  #나중에는 쓸모 X 
        'groups': groups,
        'ani_image': static('image/helphelp.png')    
    }

    return render(request, template_name='group/group_home.html', context=ctx)


######## 그룹 CRUD ########

# 그룹 생성
def group_create(request):
    user = request.user
    groups = Group.objects.values('name')
    print(groups)

    if request.method == 'POST':
        form = GroupForm(request.POST, request.FILES)
        if form.is_valid():
            group = form.save()
            group.mode = request.POST.get('group-mode__tag')
        # image = request.FILES.get('image')
        # group.image = image
            print(group.mode)
            group.maker = user    # 방장 = 접속한 유저
            group.members.add(user)  # 방장도 그룹의 멤버로 추가
            group.save()

            print(group.members)

            return redirect('group:group_home')
    else:
        form = GroupForm()
        users = User.objects.all()
        # users = User.objects.exclude(user)
        # form.fields['maker'].queryset = users
        ctx = { 'form': form }
        
        return render(request, 'group/group_form.html', context=ctx)

# 그룹 정보 수정
def group_update(request, pk):
    group = get_object_or_404(Group, pk=pk)

    if request.method == 'POST':
        form = GroupForm(request.POST, instance=group)
        group.name = request.POST.get('name')
        # 이미지 수정 -> 파일 탐색기
        group.mode = request.POST.get('group-mode__tag')
        image = request.FILES.get('image')
        group.image = image
        group.intro = request.POST.get('intro')
        
        group.save()

        # if form.is_valid():
        #     group = form.save()
        #     group.user = request.user
        #     group.save()

        return redirect('group:group_detail', pk)
    else:
        form = GroupForm(instance=group)
        ctx = {'group': group, 'form': form}

        return render(request, template_name='group/group_form.html', context=ctx)

# 그룹 삭제
def group_delete(request, pk):
    user = request.user
    group = get_object_or_404(Group, pk=pk)

    if user == group.maker:
        group.delete()

        return redirect('group:group_home')
    else:
        ### 알림 창 하나 띄우기(alert) "방장만 그룹을 삭제할 수 있습니다."
        return redirect('group:group_detail', pk)

# 그룹 탈퇴
def group_drop(request, pk):
    user = request.user
    group = get_object_or_404(Group, pk=pk)
    members = group.members.all()

    if len(members) > 1:
        if user == group.maker:
            # group.members.remove(user)
            print(members)
            group.members.remove(user)
            # group.maker = members[0]   #랜덤하게 지정해야 하나..?
            group.save()

            print(group.maker)
            # group.maker = members[0]
            # group.save()

        else:
            group.members.remove(user)
        
    else: 
        group.delete()

        # group_delete(request, pk)  # 그룹 삭제 함수 호출

    return redirect('group:group_home')

# 그룹 상세 페이지
def group_detail(request, pk):
    groups = get_object_or_404(Group, pk=pk)
    members = groups.members.all()
    groups.maker = members[0]
    maker = groups.maker
    groups.save()

    # if groups.mode == 'PUBLIC':
    #     modes = groups.mode

    print(members)
    print(maker)
    print(groups.mode)
    print(members.filter(nickname__contains=maker.nickname))

    ctx = { 
        'group': groups, 
        'members': members,
        'maker': maker,
        'ani_image': static('image/helphelp.png'),    
        'profile_img': static('image/none_image_user.jpeg'),
    }

    return render(request, template_name='group/group_detail.html', context=ctx)


######## 초대 코드 ########

# def group_status(group, login_user):
#     if group.status == 'false':
#         if group.maker == login_user:
#             return 2  # 초대 수락 여부 결정
#         else:
#             return 1  # 수락을 기다리는 중
#     else:
#         return 3  # 가입 완료

# 초대 코드 발급
def get_invite_code(length=6):
    return base64.urlsafe_b64encode(
        codecs.encode(uuid.uuid4().bytes, 'base64').rstrip()
    ).decode()[:length]

# 초대 코드 공개(from 그룹 상세 페이지)
def create_code(request, pk):
    group = get_object_or_404(Group, pk=pk)
    group.code = get_invite_code()
    group.save()
    # 여기서 3분 제한 둘 것
    ctx = { 'group': group }

    return render(request, template_name='group/create_code.html', context=ctx)

# 초대 코드 입력(from 그룹 메인 페이지 / 비공개 그룹 가입)
def join_group(request):    
    user = request.user
    input_code = request.GET.get('code')
    print(input_code)

    mygroup = list(Group.objects.filter(members__nickname__contains=user))
    try:
        if input_code != None:
            group = get_object_or_404(Group, code=input_code)
            print(group)
            # 예외처리 or 조건문
            if group in mygroup:
                message = "이미 가입된 그룹입니다."
                ctx = { 'message': message }

                return render(request, template_name='group/join_group.html', context=ctx)

            else:   # user != 방장
                # if (group):   #queryset이 비어있을 때 반대로 생각하기
                group.members.add(user)
                group.save()
                # status = group_status(group, user)

                
                return redirect('group:group_home')
        else:
            message = "아무것도 입력하지 않았습니다."
            ctx = { 'message': message }

            return render(request, template_name='group/join_group.html', context=ctx)

    except:
        print('존재하지 않는 그룹입니다.')
        message = "존재하지 않는 코드입니다."
        ctx = { 'message': message }

        return render(request, template_name='group/join_group.html', context=ctx)

# def input_code(request):
#     input_code = request.GET.get('code')
#     ctx = { 'input': input_code }

#     return render(request, template_name='group/input_code.html', context=ctx)


######## 공개 그룹 ########

# 그룹 모아보기 게시판(그룹 찾기)
def group_list(request):
    group = Group.objects.filter(mode='PUBLIC')
    groups = Group.objects.all()
    print(group)
    print(groups)
    ctx = { 
        'groups': group,
        'ani_image': static('image/helphelp.png')    
    }

    return render(request, template_name='group/group_list.html', context=ctx)

# 그룹 가입하기
def public_group_join(request, pk):
    user = request.user
    group = get_object_or_404(Group, pk=pk)
    members = group.members.all()

    if user not in members:
        group.waits.add(user)
        group.save()

    redirect('group:group_detail', pk)

# 그룹 가입 요청 리스트(user == 방장일 때만 확인 가능)
def join_list(request, pk):
    user = request.user
    group = get_object_or_404(Group, pk=pk)
    waits = group.waits.all()
    members = group.members.all()
    result = request.GET.get('accept')  # 수락/거절 중 user가 선책한 값

    if user == group.maker:
        ctx = { 
            'group': group,
            'members': members,
            'waits': waits,
            'profile_img': static('image/none_image_user.jpeg'),
        }
        
        return render(request, template_name='group/join_list.html', context=ctx)
    else:
        # alert 창 띄우기 (방장이 아니므로 열람할 수 없습니다)
        redirect('group:group_detail')

## Ajax
# 내 그룹 - 찜 기능 ajax
@csrf_exempt
def star_ajax(request):
    req = json.loads(request.body)
    group_id = req['id']
    group = get_object_or_404(Group, id=group_id)
    
    if (group.is_star == True):
        group.is_star = False

    else:
        group.is_star = True

    is_stared = group.is_star
    group.save()

    return JsonResponse({ 'id': group_id, 'is_star': is_stared })

# 공개 그룹 좋아요 수 = 인기 그룹 선정 기준
@csrf_exempt
def group_interest_ajax(request):
    req = json.loads(request.body)
    group_id = req['id']
    group = Group.objects.get(id=group_id)

    group.like += 1
    group.save()

    return JsonResponse({ 'id': group_id })