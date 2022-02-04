import uuid
import base64
import codecs
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *

# 나의 그룹
def group_home(request):
    user = get_object_or_404(User)  # 현재 접속한 사용자

    # 해당 유저의 그룹 리스트
    group = Participation.objects.all().filter(member_id=user.id)
    # member = Participation.objects.all()   # 해당 그룹에 가입한 멤버 리스트
    member_cnt = group.member.count()  # 그룹의 총 멤버 수
    ctx = { 'groups': group, 'member_cnt': member_cnt }

    return render(request, template_name='group/group_home.html', context=ctx)

# 그룹 생성
def group_create(request):
    user = get_object_or_404(User, user=request.nickname)
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            group.maker = user    # 방장 = 접속한 유저
            group.save()

            return redirect('group:group_detail', pk=group.id)
    else:
        form = GroupForm()
        users = User.objects.all().exclude(user=request.nickname)
        form.fields['maker'].queryset = users
        ctx = { 'form': form }
        
        return render(request, 'group/group_form.html', context=ctx)

# 그룹 정보 수정
def group_update(request, pk):
    group = get_object_or_404(Group, pk=pk)

    if request.method == 'POST':
        form = GroupForm(request.POST, instance=group)
        # 이미지 수정 -> 파일 탐색기
        image = request.FILES.get('image')
        group.image = image
        group.save()

        if form.is_valid():
            group = form.save()

            return redirect('group:group_detail', pk)
    else:
        form = GroupForm(instance=group)
        ctx = {'form': form}

        return render(request, template_name='group/group_form.html', context=ctx)

# 그룹 탈퇴
def group_delete(request, pk):
    group = get_object_or_404(Group, pk=pk)
    group.delete()

    return redirect('group:group_home')


# 초대 코드 생성
def get_invite_code(length=6):
    return base64.urlsafe_b64encode(
        codecs.encode(uuid.uuid4().bytes, 'base64').rstrip()
    ).decode()[:length]

# 그룹 모아보기 게시판(그룹 찾기)
def group_list(request):
    group = Group.objects.all()
    ctx = { 'groups': group }

    return render(request, template_name='group/group_list.html', context=ctx)