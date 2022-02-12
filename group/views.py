from calendar import c
from email import message
import re
from tkinter import E
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
import mimetypes
from user.update import *

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

command = []
# 그룹 생성
def group_create(request):
    user = request.user

    if request.method == 'POST':
        form = GroupForm(request.POST, request.FILES)

        name = request.POST.get('name')
        intro = request.POST.get('intro')
        image = request.FILES.get('image')
        mode = request.POST.get('group-mode__tag')

        origin_group = Group.objects.filter(name=name)
        global command
        command += ['group_create']

        # 에러 메세지 
        error = GroupErrorMessage()
        error.validation_group(name, mode, '', command)
        
        if not error.has_error_group():
            group = form.save()
            group.mode = mode
            image = request.FILES.get('image')
            group.image = image
            group.maker = user    # 방장 = 접속한 유저
            group.members.add(user)  # 방장도 그룹의 멤버로 추가
            group.save()

            return redirect('group:group_home')

        ctx = { 
            'error': error,
            'name': name,
            'mode': mode,
            'intro': intro,
            'image': image
        }
        
        return render(request, template_name='group/group_form.html', context=ctx)
        
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
        global command
        command += ['group_create']

        group.name = request.POST.get('name')
        name = group.name

        group.intro = request.POST.get('intro')
        intro = group.intro

        if group.image:
            image = group.image
        # 기존 이미지는 유지
        if request.FILES.get('image'):
            image = request.FILES.get('image')
            group.image = image
        
        # group.image = image

        mode = request.POST.get('group-mode__tag')
        group.mode = mode

        # 에러 메세지
        error = GroupErrorMessage()
        error.validation_group(name, mode, prev_name, command)

        if not error.has_error_group():
            group.save()

            return redirect('group:group_detail', pk)

        ctx = { 
            'error': error,
            'name': name,
            'intro': intro,
            'mode': mode
        }

        return render(request, template_name='group/group_form.html', context=ctx)

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


######## 그룹 생성 Form 오류 사항 체크 ########
class GroupErrorMessage():

    name, mode = '', ''

    def validation_group(self, name, mode, prev, command):

        # 미입력 시 에러 메세지
        if 'group_create' in command or 'group_update' in command:
            if not name:       
                self.name = '그룹명을 입력하세요.'
            if not (mode in ['PUBLIC', 'PRIVATE']):    
                self.mode = '그룹 공개모드를 선택하세요.'
        
        # 기존에 있던 입력과 비교
        if 'group_update' in command:
            if Group.objects.filter(name=name) and name != prev:
                self.name = '이미 사용 중인 그룹명입니다.'
        else:
            if Group.objects.filter(name=name):
                self.name = '이미 사용 중인 그룹명입니다.'

    def has_error_group(self):
        return self.name or self.mode


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

# 그룹 가입 대기자 명단 [미완]
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

    JsonResponse({
        'groupName': group.name,
        'waits': waits,
        'waits_img': waits_img
    })



######################### 그룹 내 커뮤니티 게시판 ##############################
### Error messages
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
class ErrorMessages():
    title, content, image, attached_file, attached_link, category = '', '', '', '', '', ''
    def validation_check(self,title, content, image, attached_file, attached_link, category, command):
        if 'create' in command or 'update' in command:
            if not title:
                self.title = '제목을 입력해주세요'
            elif len(title)>50:
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
    
    # 게시물 정렬
    sort_by = request.GET.get('sort', 'recent')
    if sort_by == 'recent':    # 최신순
        posts = posts.order_by('-created_at')
    elif sort_by == 'liked':   # 좋아요순
        posts = posts.annotate(total_likes=Count('like_user')).order_by('-total_likes')
    elif sort_by == 'view':    # 조회수순
        posts = posts.order_by('-hit_count_generic__hits')

    # 페이징 처리
    paginator = Paginator(posts, 6)    # 페이지당 6개씩 보여주기
    page_obj = paginator.get_page(page)

    ctx = {
        'posts': page_obj,
        'group': group,
        'sort_by': sort_by
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
    group = get_object_or_404(Group, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        error_messages = ErrorMessages()
        error_messages.validation_check(
            request.POST.get('title'),
            request.POST.get('content'),
            request.FILES.get('image'),
            request.FILES.get('attached_file'),
            request.POST.get('attached_link'),
            request.POST.get('category'),
            'create'
        )
        if not error_messages.has_error():
            post = GroupPost.objects.create(
                title=request.POST.get('title'),
                content=request.POST.get('content'),
                image=request.FILES.get('image'),
                attached_file=request.FILES.get('attached_file'),
                attached_link=request.POST.get('attached_link'),
                category=request.POST.get('category'),
                user=request.user,
                group=group
            )
            post.save()
            return redirect ('group:post_detail', pk, post.pk)
        # if form.is_valid():
        #     post = form.save(commit=False)
        #     post.group = get_object_or_404(Group, pk=pk)   # 그룹 pk로 받아오기
        #     post.category = request.POST.get('category')  # 그룹게시글 카테고리 (대분류)
        #     post.user = request.user
        #     post = form.save()
            ### TODO
            # 게시글 디테일 페이지로 이동
        else:
            original_information = OriginalInformation()
            original_information.remember(request, ['create'])
            
            ctx = {
                'form': form, 
                'error_messages': error_messages,
                'original_information': original_information,
                'group': group
                }
            return render(request, 'group/group_post_form.html', context=ctx)

    else:
        form = PostForm()
        ctx = {'form': form, 'group': group}

        return render(request, 'group/group_post_form.html', context=ctx)


def post_update(request,pk ,post_pk):
    post = get_object_or_404(GroupPost, pk=post_pk)
    group = get_object_or_404(Group, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance = post)

        error_messages = ErrorMessages()
        error_messages.validation_check(
            request.POST.get('title'),
            request.POST.get('content'),
            request.FILES.get('image'),
            request.FILES.get('attached_file'),
            request.POST.get('attached_link'),
            request.POST.get('category'),
            ['update']
        )
        if not error_messages.has_error():
            post = form.save()
            return redirect('group:post_detail', pk, post.pk)
        else:
            original_information = OriginalInformation()
            original_information.remember(request, ['update'])

            ctx = {
                'form': form, 
                'error_messages': error_messages,
                'original_information': original_information,
                'group': group,
                }
            return render(request, 'group/group_post_form.html', context=ctx)
        # if form.is_valid():
        #     post = form.save()  

        #     return redirect('group:post_detail', pk, post_pk)
        # else:
        #     ctx = {'form': form,}
        #     return render(request, 'group/group_post_form.html', context=ctx)
    else:
        form = PostForm(instance=post)

        ctx = {'form': form, 'post': post, 'group': group,}

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
            previous_pk = GroupPost.get_previous_by_created_at(self.object, group=self.object.group).pk
        except:
            # 이전글 없을 때
            previous_pk = -1
        try:
            next_pk =  GroupPost.get_next_by_created_at(self.object, group=self.object.group).pk
        except:
            # 이전글 없을 때
            next_pk = -1
        context['next_pk'] = next_pk
        context['previous_pk'] = previous_pk

        post = self.object
        username = post.user.nickname
        total_likes = len(post.like_user.all())
        is_liked = self.request.user in  post.like_user.all()

        # 해당 게시글에 대한 답변 가져오기
        answers = GroupAnswer.objects.filter(post_id = post.id, parent_answer__isnull=True).order_by('answer_order')   #  나중에 답변 정렬도 고려. 최신순 또는 좋아요 순
        answers_count = len(answers)
        
        answers_reply_dict ={}
        for answer in answers:
            replies =  GroupAnswer.objects.filter(parent_answer= answer).order_by('answer_order')
            answers_reply_dict[answer] = replies

        context['group'] = post.group
        context['username']= username
        context['total_likes'] = total_likes
        context['is_liked']= is_liked
        context['answers']= answers
        context['answers_count']= answers_count
        context['answers_reply_dict']= answers_reply_dict
        return context

class FileDownloadView(SingleObjectMixin, View):
    queryset = GroupPost.objects.all()

    def get(self, request, pk):
        object = get_object_or_404(GroupPost, pk=pk)
        
        file_path = object.attached_file.path
        file_type, _ = mimetypes.guess_type(file_path)
        #file_type = object.attached_file.name.split('.')[-1]  # django file object에 content type 속성이 없어서 따로 저장한 필드
        fs = FileSystemStorage(file_path)
        response = FileResponse(fs.open(file_path, 'rb'), content_type=file_type)
        response['Content-Disposition'] = f'attachment; filename={object.get_filename()}'
        
        return response

@csrf_exempt
def answer_ajax(request):
    req = json.loads(request.body)
    post_id = req['postId']
    content = req['content']
    user_id = req['user']
    user = get_object_or_404(User, pk=user_id)
    username = user.nickname
    
    #### TODO ##########
    ## user 대표이미지 넘겨주는 건 유저 조금 구체화 된 다음에 추가

    ## 새 답변의 order 필드를 정해주기 위한 부분. 
    current_answers = GroupAnswer.objects.filter(post_id=post_id).order_by('answer_order')
    if len(current_answers)==0:
        new_order = 1
    else:
        new_order = current_answers.last().answer_order + 1

    this_post = get_object_or_404(GroupPost, pk=post_id)

    ## 새로운 답변
    new_answer = GroupAnswer.objects.create(post_id=this_post, content=content, answer_order=new_order, user = user)
    # 템플릿에서 쉽게 띄울 수 있도록 답변 게시일자 포맷팅해서 json에 전달
    created_at = new_answer.created_at.strftime('%y.%m.%d %H:%M')

    return JsonResponse({'id': new_answer.id ,'content': content,'user':username, 'created_at':created_at} )

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
    
    ## 새 답변의 order 필드를 정해주기 위한 부분. 
    current_answers = GroupAnswer.objects.filter(post_id=this_post.id).order_by('answer_order')
    if len(current_answers)==0:
        new_order = 1
    else:
        new_order = current_answers.last().answer_order + 1

    ## 새로운 대댓글
    new_answer = GroupAnswer.objects.create(
        post_id=this_post, 
        content=content, 
        answer_order=new_order, 
        user = user,
        parent_answer = this_answer
    )

    # 템플릿에서 쉽게 띄울 수 있도록 답변 게시일자 포맷팅해서 json에 전달
    created_at = new_answer.created_at.strftime('%y.%m.%d %H:%M')

    response = JsonResponse({
        'reply_id': new_answer.id,
        'answer_id' : this_answer.id,
        'content': content,
        'user':username, 
        'created_at':created_at,
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

    is_liked = request.user in  liked_users.all()

    if is_liked:
        liked_users.remove(request.user)
    else:
        liked_users.add(request.user)

    total_likes = len(liked_users.all())
    return JsonResponse({'post_id':post_id, 'total_likes':total_likes, 'is_liking': not(is_liked)})

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

    return JsonResponse({'answer_id':answer_id, 'total_likes':total_likes,  'is_liking': not(is_liked)})


# 답변(대댓글 포함) 삭제
@csrf_exempt
def answer_delete_ajax(request):
    req = json.loads(request.body)
    answer_id = req['id']

    answer = get_object_or_404(GroupAnswer, pk=answer_id)

    answer.delete()

    return JsonResponse({'id':answer_id})

# 답변(대댓글 포함) 수정
# 수정버튼 눌렀을 때 해당하는 폼 띄우는 기능
@csrf_exempt
def answer_edit_ajax(request):
    req = json.loads(request.body)
    answer_id = req['id']

    answer = get_object_or_404(GroupAnswer, pk=answer_id)
    # TODO : 고려해볼 사항. 원래 작성되어 있던 내용을 지금은 db에서 찾아서 넘겨주고 있는데
    # 그렇게 말고 data전송을 최소화화면서 프론트 단에서 그냥 현재 입력된 내용 받앙오기
    

    return JsonResponse({'id':answer_id})

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

    return JsonResponse({'id':answer_id, 'content':new_content})

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


