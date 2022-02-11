from email import message
import re
from tokenize import blank_re
import uuid
import base64
import codecs
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.templatetags.static import static
from django.db.models import Q
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from .models import *
from .forms import *
from django.core.paginator import Paginator 

######## 그룹 메인 페이지 ########

# 나의 그룹
def group_home(request):
    user = request.user  # 현재 접속한 사용자

    # 해당 유저의 그룹 리스트
    groups = user.group_set.all()
    
    # 페이징 처리
    page = request.GET.get('page', '1')

    # 정렬하기
    sort = request.GET.get('sort', 'star')
    if sort == 'name':
        groups = groups.order_by('name')
    elif sort == 'star':
        groups = groups.order_by('-is_star')
    # elif sort == 'member':
    #     groups = groups.order_by('-members')
    # elif sort == 'date':  # django에서 기본 제공하는 create날짜 있는지 체크
    #     groups = groups.order_by('date')
    ### user의 닉네임이랑 같은 경우에 처리해야 하는 부분 이후 추가
    pagintor = Paginator(groups, 6)
    page_obj = pagintor.get_page(page)

    ctx = { 
        'user': user,  #나중에는 쓸모 X 
        'groups': page_obj,
        'sort_by': sort,
        'ani_image': static('image/helphelp.png')    
    }

    return render(request, template_name='group/group_home.html', context=ctx)

# 그룹 검색하기(나의 그룹 홈)
def group_search(request):
    if 'search' in request.GET:
        query = request.GET.get('search')
        groups = Group.objects.filter(
            name__icontains=query
            # Q(members__nickname__icontains=query)
        )
        ctx = { 
            'groups': groups,
            'query': query, 
            'ani_image': static('image/helphelp.png')    
        }

    return render(request, 'group/group_search.html', context=ctx)

# 그룹 검색하기(공개 그룹 찾기)
def group_search_public(request):
    if 'search' in request.GET:
        query = request.GET.get('search')
        groups = Group.objects.all().filter(Q(name__icontains=query) & Q(mode='PUBLIC'))
        ctx = { 
            'groups': groups,
            'query': query
        }

    return render(request, 'group/group_search_public.html', context=ctx)



######## 그룹 CRUD ########

# 그룹 생성
def group_create(request):
    user = request.user
    groups = Group.objects.values('name')

    if request.method == 'POST':
        form = GroupForm(request.POST, request.FILES)

        if form.is_valid():
            name = request.POST.get('name')
            intro = request.POST.get('intro')

            if not name:
                error_name = '그룹명을 입력하세요.'

                ctx = { 
                        'error_name': error_name,
                        'name': name,
                        'intro': intro
                    }

                return render(request, template_name='group/group_form.html', context=ctx)
            else:
                if Group.objects.filter(name=name):  # 그룹명은 식별자 => 이미 존재하는 이름이면 생성된 그룹 삭제
                    error_name = '이미 존재하는 이름입니다.'

                    ctx = { 
                        'error_name': error_name,
                        'name': name,
                        'intro': intro
                    }

                    return render(request, template_name='group/group_form.html', context=ctx)

    
            if not request.POST.get('group-mode__tag'):
                error_mode = '그룹 공개모드를 선택하세요.'

                ctx = {
                    'error_mode': error_mode,
                    'name': name,
                    'intro': intro
                }

                return render(request, template_name='group/group_form.html', context=ctx)

            group = form.save()
            group.mode = request.POST.get('group-mode__tag')
        # image = request.FILES.get('image')
        # group.image = image
            print(group.mode)
            group.maker = user    # 방장 = 접속한 유저
            group.members.add(user)  # 방장도 그룹의 멤버로 추가
            group.save()

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
    prev_name = group.name

    if request.method == 'POST':
        form = GroupForm(request.POST, instance=group)
        group.name = request.POST.get('name')
        if group.name != prev_name:
            if Group.objects.filter(name=group.name).exclude(name=prev_name):  # 그룹명은 식별자 => 이미 존재하는 이름이면 생성된 그룹 삭제
                error_name = '이미 존재하는 이름입니다.'
                ctx = { 
                    'error_name': error_name 
                }

                return render(request, template_name='group/group_form.html', context=ctx)


        if not request.POST.get('group-mode__tag'):
            error_mode = '그룹 공개모드를 선택하세요.'

            ctx = {
                'error_mode': error_mode
            }

            return render(request, template_name='group/group_form.html', context=ctx)


        if form.is_valid():
            group = form.save()
            # 이미지 수정 -> 파일 탐색기
            group.mode = request.POST.get('group-mode__tag')
            # 기존 이미지는 유지
            if request.FILES.get('image'):
                image = request.FILES.get('image')
                group.image = image
            group.intro = request.POST.get('intro')
            
            group.save()

        return redirect('group:group_detail', pk)
    else:
        form = GroupForm(instance=group)
        ctx = { 'group': group, 'form': form }

        return render(request, template_name='group/group_form.html', context=ctx)

# 그룹 삭제
def group_delete(request, pk):
    user = request.user
    group = get_object_or_404(Group, pk=pk)

    if user == group.maker:
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
            group.save()
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
    user = request.user
    group = get_object_or_404(Group, pk=pk)

    mygroup = user.group_set.all()
    members = group.members.all()
    group.maker = members[0]
    maker = group.maker
    group.save()

    total_likes = len(group.interests.all())
    is_liked = user in group.interests.all()

    print(group.interests.all())
    print(is_liked)
    print(total_likes)

    ctx = { 
        'group': group, 
        'mygroup': mygroup,
        'members': members,
        'maker': maker,
        'total_likes': total_likes,
        'is_liked': is_liked,
        'user': user,
        'ani_image': static('image/helphelp.png'),    
        'profile_img': static('image/none_image_user.jpeg'),
    }

    return render(request, template_name='group/group_detail.html', context=ctx)


######## 초대 코드 ########

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
    group.code = get_invite_code()
    group.save()
    code = group.code

    return JsonResponse({ 'name': group.name, 'code': code })


# 초대 코드 입력하기 (나의 그룹 홈페이지)
@csrf_exempt
def join_code_ajax(request):
    req = json.loads(request.body)
    
    user = request.user
    input_code = req['code']
    mygroup = list(user.group_set.all())

    try:
        if input_code != None:
            group = get_object_or_404(Group, code=input_code)
            if group in mygroup:
                message = '이미 가입된 그룹입니다.'
            else:
                group.members.add(user)
                group.save()
                message = '가입에 성공했습니다.'

        else:
            message = '가입에 성공했습니다.'

    except:
        message = '존재하지 않는 코드입니다.'

    return JsonResponse({ 'message': message })


######## 공개 그룹 ########

# 그룹 모아보기 게시판(그룹 찾기)
def group_list(request):
    group = Group.objects.filter(mode='PUBLIC')
    # group = Group.objects.all()
    groups = group.order_by('name')
    # 페이징 처리
    page = request.GET.get('page', '1')


    sort = request.GET.get('sort', 'interest')
    if sort == 'name':
        groups = group.order_by('name')
    elif sort == 'interest':
        groups = group.annotate(total_likes=Count('interests')).order_by('-total_likes')

    pagintor = Paginator(groups, 6)
    page_obj = pagintor.get_page(page)

    ctx = { 
        'groups': page_obj,
        'sort_by': sort,
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

    return redirect('group:group_detail', pk)

# 그룹 가입 요청 리스트(user == 방장일 때만 확인 가능)
def join_list(request, pk):
    user = request.user
    group = get_object_or_404(Group, pk=pk)
    waits = group.waits.all()
    members = group.members.all()
    group.maker = members[0]
    maker = group.maker

    for wait in waits:
        if request.GET.get('accept'):
            group.waits.remove(wait)
            group.members.add(wait)
            group.save()
        elif request.GET.get('reject'):
            group.waits.remove(wait)
            group.save()
    
    if user == group.maker:

        ctx = { 
            'group': group,
            'members': members,
            'waits': waits,
            'maker': maker,
            'profile_img': static('image/none_image_user.jpeg'),
        }
        
        return render(request, template_name='group/join_list.html', context=ctx)
    else:
        # alert 창 띄우기 (방장이 아니므로 열람할 수 없습니다)
        return redirect('group:group_detail', pk)

# 그룹 가입 대기자 명단
@csrf_exempt
def wait_list_ajax(request):
    req = json.loads(request.body)
    group_id = req['id']
    group = get_object_or_404(Group, pk=group_id)
    waits = group.waits.all()
    waits_img = group.waits.get('image')
    
    for wait in waits:
        if request.GET.get('accept'):
            group.waits.remove(wait)
            group.members.add(wait)
            group.save()
        elif request.GET.get('reject'):
            group.waits.remove(wait)
            group.save()
    print(waits)
    JsonResponse({
        'groupName': group.name,
        'waits': waits,
        'waits_img': waits_img
    })



######################### 그룹 내 커뮤니티 게시판 ##############################
# 게시글 목록
def post_list(request, pk):
    posts = GroupPost.objects.filter(group__pk=pk).order_by('-created_at')
    group = Group.objects.get(pk=pk)
    page = request.GET.get('page', '1')    # 페이지

    # 게시물 정렬
    sort = request.GET.get('sort', 'recent')
    if sort == 'recent':    # 최신순
        posts = posts.order_by('-created_at')
    elif sort == 'view':    # 조회수순
        posts = posts.objects.order_by('-hit')

    # 페이징 처리
    paginator = Paginator(posts, 5)    # 페이지당 5개씩 보여주기
    page_obj = paginator.get_page(page)

    ctx = {
        'posts': page_obj,
        'group': group,
        'sort_by': sort
    }

    return render(request, 'group/group_post_list.html', context=ctx)

# 게시글 검색
def search_result(request):
    if 'search' in request.GET:
        query = request.GET.get('search')
        posts = GroupPost.objects.all().filter(
            Q(title__icontains=query) | # 제목으로 검색
            Q(content__icontains=query) # 내용으로 검색
        )

    return render(request, 'group/search_result.html', {'query': query, 'posts': posts})

# 게시글 작성
def post_create(request, pk):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.group = get_object_or_404(Group, pk=pk)   # 그룹 pk로 받아오기
            # post.category_tag = request.POST.get('category_choice')  # 그룹게시글 카테고리 (대분류)
            post.user = request.user
            post = form.save()

        return redirect('group:post_list', pk=pk)

    else:
        form = PostForm()
        ctx = {'form': form}

        return render(request, 'group/group_post_create.html', context=ctx)


############################################################################

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

    return JsonResponse({ 'groupId': group_id, 'total_likes': total_likes, 'is_liked': not(is_liked) })


