from django.shortcuts import render, redirect, get_object_or_404
from .models import *

# 나의 그룹
def group_home(request):
    user = get_object_or_404(User)  #현재 접속한 사용자

    #해당 유저의 그룹 리스트
    group = Participation.objects.all().filter(member_id=user.id)
    # member = Participation.objects.all()   #해당 그룹에 가입한 멤버 리스트
    member_cnt = member.member.count()  #그룹의 총 멤버 수
    ctx = { 'groups': group, 'member_cnt': member_cnt }

    return render(request, template_name='group/group_home.html', context=ctx)
    

# 그룹 모아보기 게시판(그룹 찾기)
def group_list(request):
    group = Group.objects.all()
    ctx = { 'groups': group }

    return render(request, template_name='group/group_list.html', context=ctx)
