import uuid
import base64
import codecs
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .forms import *

## 그룹 메인 페이지

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
    # elif sort == 'date':  # django에서 기본 제공하는 create날짜 있는지 체크
    #     groups = groups.order_by('date')
    ### user의 닉네임이랑 같은 경우에 처리해야 하는 부분 이후 추가

    ctx = { 'groups': groups }

    return render(request, template_name='group/group_home.html', context=ctx)


## 그룹 CRUD

# 그룹 생성
def group_create(request):
    user = request.user
    if request.method == 'POST':
        form = GroupForm(request.POST, request.FILES)
        if form.is_valid():
            group = form.save()
            
            # group.image = request.POST.get('image')
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
        # group.name = request.POST.get('name')
        # 이미지 수정 -> 파일 탐색기
        image = request.FILES.get('image')
        group.image = image
        # group.intro = request.POST.get('intro')
        
        group.save()

        if form.is_valid():
            group = form.save()

            return redirect('group:group_detail', pk)
    else:
        form = GroupForm(instance=group)
        ctx = {'group': group, 'form': form}

        return render(request, template_name='group/group_form.html', context=ctx)

# 그룹 탈퇴
def group_delete(request, pk):
    group = get_object_or_404(Group, pk=pk)
    group.delete()

    return redirect('group:group_home')


## 초대 코드 

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

# 초대 코드 입력(from 메인 페이지)
def join_group(request):    
    user = request.user
    input_code = request.GET.get('code')

    mygroup = list(Group.objects.filter(members__nickname__contains=user))
    try:
        group = get_object_or_404(Group, code=input_code)
        print(group)
        # 예외처리 or 조건문
        if group in mygroup:
            message = "이미 가입된 그룹입니다."
            ctx = { 'message': message }

            return render(request, template_name='group/join_group.html', context=ctx)

        else:
            if (group):
                group.members.add(user)  # 방장도 그룹의 멤버로 추가
                group.save()

                return redirect('group:group_home')
    except:
        print('존재하지 않는 그룹입니다.')
        message = "존재하지 않는 코드입니다."
        ctx = { 'message': message }

        return render(request, template_name='group/join_group.html', context=ctx)



# 그룹 상세 페이지
def group_detail(request, pk):
    groups = get_object_or_404(Group, pk=pk)
    members = groups.members.all()

    print(members)

    ctx = { 'group': groups, 'members': members }

    return render(request, template_name='group/group_detail.html', context=ctx)

# 그룹 모아보기 게시판(그룹 찾기)
def group_list(request):
    group = Group.objects.all()
    ctx = { 'groups': group }

    return render(request, template_name='group/group_list.html', context=ctx)


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