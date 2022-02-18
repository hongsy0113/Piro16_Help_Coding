#-*-coding:utf-8-*-
from datetime import date
from wsgiref.simple_server import sys_version
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.db.models import Q
import json
import shutil, os
from django.http import JsonResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator 
from django.db.models import Count
from django.views.generic import ListView, View
from hitcount.views import HitCountDetailView
from django.views.generic.detail import SingleObjectMixin
from django.core.files.storage import FileSystemStorage
from config.settings import MEDIA_ROOT
import mimetypes
from user.update import *
from .forms import FileFieldForm
from django.contrib.auth.models import AnonymousUser

basic_tags = ['동작', '형태', '소리', '이벤트', '제어',' 감지', '연산', '변수', '내 블록', '기타']

def question_tag_filter(questions, tag_filter_by_list):
    num = len(tag_filter_by_list)
    if num == 1:
        questions= questions.filter(s_or_e_tag=tag_filter_by_list[0]) 
    elif num == 2:
        questions= questions.filter(Q(s_or_e_tag=tag_filter_by_list[0]) | Q(s_or_e_tag=tag_filter_by_list[1]))
    elif num==3:
        pass
    return questions

def question_answer_filter(questions, answer_filter_by):
    if answer_filter_by == 'NOT_ANSWERED':
        questions= questions.filter(answer = None)
    else:
        questions = questions.annotate(answer_count=models.Count("answer")).filter(answer_count__gt = 0)
    return questions

### Error messages
# 이름이 user.view에 있는 것과 겹쳐서, 헷갈릴 여지가 있을 것 같습니다.
# QnaErrorMessages가 좋을 것 같습니다.
 # TODO : validation 체크할 때 request 객체와 form을 넘겨주는 건 어떨까요?
# TODO : 넘겨주는 인자가 너무 많고, 순서 헷갈릴 여지도 있어보입니다.
class QnaErrorMessages():
    title, content, image, attached_file, s_or_e_tag, tags = '', '', '', '', '', ''

    def validation_check(self, request, command):
        if 'create' in command or 'update' in command:
            if not request.POST.get('title'):
                self.title = '제목을 입력해주세요'
            elif len(request.POST.get('title'))>50:
                self.title = '제목은 50자 이내로 입력해주세요'
            if not request.POST.get('content'):
                self.content = '내용을 입력해주세요'
            if not request.POST.get('s_or_e_tag'):
                self.s_or_e_tag = '카테고리를 선택해주세요'

    def has_error(self):
        return self.title or self.content or self.image or self.attached_file or self.s_or_e_tag or self.tags

class OriginalInformation():
    def remember(self, request, command):
        self.title = request.POST.get('title')
        self.content = request.POST.get('content')
        self.image = request.FILES.get('image')
        self.attached_file = request.FILES.get('attached_file')
        self.s_or_e_tag = request.POST.get('s_or_e_tag')
        self.tags = request.POST.getlist('detail_tag')
        self.command = command

##### view 시작

def question_list(request):
    questions = Question.objects.all().order_by('-created_at')
    page = request.GET.get('page', '1')    # 페이지
    #questions = Question.objects.order_by('-created_at')   # [기본 정렬] 최신순으로 정렬

    # 게시글 필터
    tag_filter_by = request.GET.getlist('tag_filter_by')
    if tag_filter_by:
        questions = question_tag_filter(questions, tag_filter_by)
    answer_filter_by = request.GET.get('answer_filter_by')
    if answer_filter_by:
        questions = question_answer_filter(questions, answer_filter_by)

    # 게시물 정렬
    sort_by = request.GET.get('sort', 'recent')
    if sort_by == 'recent':    # 최신순
        questions = questions.order_by('-created_at')
    elif sort_by == 'liked':   # 좋아요순
        questions = questions.annotate(total_likes=Count('like_user')).order_by('-total_likes')
    elif sort_by == 'view':    # 조회수순
        questions = questions.order_by('-hit_count_generic__hits')
    # 페이징 처리
    paginator = Paginator(questions, 5)    # 페이지당 5개씩 보여주기
    page_obj = paginator.get_page(page)

    dict ={}
    for page in page_obj:
        answers_count = Answer.objects.filter(question_id =page, answer_depth=0, is_deleted = False).count()
        dict[page] = answers_count
    ctx = {
        'questions': page_obj,
        'sort_by':sort_by,
        'filter_by':tag_filter_by+[answer_filter_by],
        'question_answer_count':dict,
    }

    return render(request, 'qna/question_list.html', context=ctx)

def search_result(request):
    if 'search' in request.GET:
        query = request.GET.get('search')
        questions = Question.objects.all().filter(
            Q(title__icontains=query) | # 제목으로 검색
            Q(content__icontains=query)| # 내용으로 검색
            Q(tags__tag_name__icontains=query) # 태그로 검색
        )

    # 게시물 정렬
    sort_by = request.GET.get('sort', 'recent')
    if sort_by == 'recent':    # 최신순
        questions = questions.order_by('-created_at')
    elif sort_by == 'liked':   # 좋아요순
        questions = questions.annotate(total_likes=Count('like_user')).order_by('-total_likes')
    elif sort_by == 'view':    # 조회수순
        questions = questions.order_by('-hit_count_generic__hits')

    page = request.GET.get('page', '1')    # 페이지
    paginator = Paginator(questions, 5)    # 페이지당 5개씩 보여주기
    page_obj = paginator.get_page(page)
    
    dict ={}
    for page in page_obj:
        answers_count = Answer.objects.filter(question_id =page, answer_depth=0, is_deleted = False).count()
        dict[page] = answers_count

    ctx = {
        'query': query, 
        'questions': page_obj, 
        'question_answer_count':dict,
        'sort_by':sort_by,
    }
    return render(request, 'qna/search_result.html', context=ctx)



def question_create(request):
    user = request.user
    if user == AnonymousUser():
        return redirect('user:main')

    if request.method == 'POST':
        form = QuestionForm(request.POST, request.FILES)
        
        error_messages = QnaErrorMessages()

        error_messages.validation_check(request, ['create'])
        if not error_messages.has_error():
            question = Question.objects.create(
                title=request.POST.get('title'),
                content=request.POST.get('content'),
                # image=request.FILES.get('image'),
                # #attached_file=form.data['attached_file'],
                # attached_file=request.FILES.get('attached_file'),
                s_or_e_tag=request.POST.get('s_or_e_tag'),
                user=request.user
            )
            
            tags = request.POST.getlist('detail_tag')
            for tag in tags:
                if len(QnaTag.objects.filter(tag_name=tag)) == 0:
                    QnaTag.objects.create(
                        tag_name = tag,
                    )

                # QnaTag db에 없으면 오류 발생
                newtag = get_object_or_404(QnaTag, tag_name=tag)
                question.tags.add(newtag)

            # image, file 부분
            date_dir = datetime.today().strftime('/%Y/%m/%d/')
            os.makedirs(MEDIA_ROOT + '/qna/uploads' + date_dir, exist_ok=True)

            if request.FILES.get('image'):
                question.image = request.FILES.get('image')
            elif request.POST['img_recent']:
                os.makedirs(MEDIA_ROOT + '/temp/', exist_ok=True)
                shutil.copyfile('./media/temp/{}'.format(request.POST['img_recent']),
                                './media/qna/uploads'+ date_dir +'{}'.format(request.POST['img_recent'])) ###
                question.image =  './qna/uploads'+ date_dir + '{}'.format(request.POST['img_recent']) ###

                ## temp 파일 삭제
                if os.path.isfile('./media/temp/{}'.format(request.POST['img_recent'])):
                    os.remove('./media/temp/{}'.format(request.POST['img_recent']))
        
            if request.FILES.get('attached_file'):
                question.attached_file = request.FILES.get('attached_file')
            elif request.POST['file_recent']:
                os.makedirs(MEDIA_ROOT + '/temp/', exist_ok=True)
                shutil.copyfile('./media/temp/{}'.format(request.POST['file_recent']),
                                './media/qna/uploads'+ date_dir +'{}'.format(request.POST['file_recent'])) ###
                question.attached_file = './qna/uploads'+ date_dir +'{}'.format( request.POST['file_recent']) ###

                ## temp 파일 삭제
                if os.path.isfile('./media/temp/{}'.format(request.POST['file_recent'])):
                    os.remove('./media/temp/{}'.format(request.POST['file_recent']))

            question.save()
            update_question(question, request.user)

            

            return redirect('qna:question_detail', question.pk)

        else:
            global basic_tags
            tags = request.POST.getlist('detail_tag')

            basic_tag_names = []
            extra_tag_names = []
            for tag in tags:
                if tag in basic_tags:
                    basic_tag_names.append(tag)
                else:
                    extra_tag_names.append(tag)

            original_information = OriginalInformation()
            original_information.remember(request, ['create'])

            if request.FILES.get('image'):
                os.makedirs(MEDIA_ROOT + '/temp/', exist_ok=True)
                with open('./media/temp/{}'.format(request.FILES['image'].name), 'wb+') as destination:
                    for chunk in request.FILES['image'].chunks():
                        destination.write(chunk)
            if request.FILES.get('attached_file'):
                os.makedirs(MEDIA_ROOT + '/temp/', exist_ok=True)
                with open('./media/temp/{}'.format(request.FILES['attached_file'].name), 'wb+' ) as destination:
                    for chunk in request.FILES['attached_file'].chunks():
                        destination.write(chunk)

            original_information.image = request.POST['img_recent']
            original_information.attached_file = request.POST['file_recent']
            
            ctx = {
                'form': form, 
                'error_messages': error_messages,
                'original_information': original_information,
                'basic_tag_names': basic_tag_names,  
                'extra_tag_names': extra_tag_names,
                'temp_img_location':'/media/temp/',
                'temp_file_location':'/media/temp/',
                }
            return render(request, 'qna/question_form.html', context=ctx)
    else:
        form = QuestionForm()
        ctx = {
            'form': form,
            'temp_img_location':'/media/temp/',
            'temp_file_location':'/media/temp/',
            }
        
        return render(request, 'qna/question_form.html', context=ctx)

class QuestionDetailView(HitCountDetailView):
    model = Question
    template_name = 'qna/detail.html'
    count_hit = True
    context_object_name = 'question'

    def get_context_data(self, **kargs):
        context = super().get_context_data(**kargs)
        # self.object로 question 객체에 접근할 수 있음
        try:
            previous_pk = Question.get_previous_by_created_at(self.object).pk
        except:
            # 이전글 없을 때
            previous_pk = -1
        try:
            next_pk = Question.get_next_by_created_at(self.object).pk
        except:
            # 이전글 없을 때
            next_pk = -1
        context['next_pk'] = next_pk
        context['previous_pk'] = previous_pk

        tags = self.object.tags.all()
        if self.object.user:
            username = self.object.user.nickname
        else:
            username = '(알 수 없음)'
        total_likes = len(self.object.like_user.all())
        
        # 해당 게시글에 대한 답변 가져오기
        answers = Answer.objects.filter(question_id = self.object.id, answer_depth=0).order_by('answer_order')   #  나중에 답변 정렬도 고려. 최신순 또는 좋아요 순
        answers_count = answers.filter(is_deleted=False).count()
        
        answers_reply_dict ={}
        for answer in answers:
            replies =  Answer.objects.filter(parent_answer= answer).order_by('answer_order')
            answers_reply_dict[answer] = replies

        # 좋아요 눌렀는지 안 눌렀는지
        is_liked = self.request.user in  self.object.like_user.all()

        context['username']= username
        context['tags'] = tags
        context['total_likes'] = total_likes
        context['answers']= answers
        context['answers_count']= answers_count
        context['answers_reply_dict']= answers_reply_dict
        context['is_liked']= is_liked

        return context

class FileDownloadView(SingleObjectMixin, View):
    queryset = Question.objects.all()

    def get(self, request, pk):
        object = get_object_or_404(Question, pk=pk)
        
        file_path = object.attached_file.path
        file_type, _ = mimetypes.guess_type(file_path)
        #file_type = object.attached_file.name.split('.')[-1]  # django file object에 content type 속성이 없어서 따로 저장한 필드
        fs = FileSystemStorage(file_path)
        response = FileResponse(fs.open(file_path, 'rb'), content_type=file_type)
        response['Content-Disposition'] = f'attachment; filename={object.get_filename()}'
        
        return response



def question_update(request, pk):
    user = request.user
    if user == AnonymousUser():
        return redirect('user:main')

    question = get_object_or_404(Question, pk=pk)

    ## file data dir
    date_dir = datetime.today().strftime('/%Y/%m/%d/')

    global basic_tags
    if request.method == "POST":
        form = QuestionForm(request.POST, request.FILES, instance = question)

        error_messages = QnaErrorMessages()

        error_messages.validation_check(request,['update'])
        if not error_messages.has_error() and form.is_valid():
            
            question = form.save()

            tags = request.POST.getlist('detail_tag')
            for tag in tags:
                if len(QnaTag.objects.filter(tag_name=tag)) == 0:
                    QnaTag.objects.create(
                        tag_name = tag,
                    )

                # QnaTag db에 없으면 오류 발생
                newtag = get_object_or_404(QnaTag, tag_name=tag)
                question.tags.add(newtag)

            #file
            if request.FILES.get('image'):  # form valid 시
                question.image = request.FILES.get('image')
                
            elif request.POST['img_recent'] :   # 다른 필드 에러 시(기존 파일 남아있도록)
                if os.path.isfile('./media/qna/uploads'+ date_dir +'{}'.format(request.POST['img_recent'])):
                    question.image = './qna/uploads'+ date_dir +'{}'.format(request.POST['img_recent'])
                else:
                    os.makedirs(MEDIA_ROOT + '/temp/', exist_ok=True)
                    shutil.copyfile('./media/temp/{}'.format(request.POST['img_recent']),
                                './media/qna/uploads'+ date_dir +'{}'.format(request.POST['img_recent'])) ###
                    question.image =  './qna/uploads'+ date_dir + '{}'.format(request.POST['img_recent']) ###
                    # temp 파일 삭제
                if os.path.isfile('./media/temp/{}'.format(request.POST['img_recent'])):
                    os.remove('./media/temp/{}'.format(request.POST['img_recent']))

            if request.FILES.get('attached_file'):  # form valid 시
                question.attached_file = request.FILES.get('attached_file')
                
            elif request.POST['file_recent']:   # 다른 필드 에러 시(기존 파일 남아있도록)
                if os.path.isfile('./media/qna/uploads'+ date_dir +'{}'.format(request.POST['file_recent'])):
                    question.attached_file = './qna/uploads'+ date_dir +'{}'.format(request.POST['file_recent'])
                else:
                    os.makedirs(MEDIA_ROOT + '/temp/', exist_ok=True)
                    shutil.copyfile('./media/temp/{}'.format(request.POST['file_recent']),
                                './media/qna/uploads'+ date_dir +'{}'.format(request.POST['file_recent']))
                    question.attached_file =  './qna/uploads'+ date_dir + '{}'.format(request.POST['file_recent'])
                    # temp 파일 삭제
                if os.path.isfile('./media/temp/{}'.format(request.POST['file_recent'])):
                    os.remove('./media/temp/{}'.format(request.POST['file_recent']))

            question.save()
            update_question(question, request.user)
            return redirect('qna:question_detail', question.pk)
        else:
            
            tags = request.POST.getlist('detail_tag')

            basic_tag_names = []
            extra_tag_names = []
            for tag in tags:
                if tag in basic_tags:
                    basic_tag_names.append(tag)
                else:
                    extra_tag_names.append(tag)

            # if request.FILES.get('image'):
            #     with open( './qna/uploads'+ date_dir +'{}'.format(request.FILES.get('image')), 'wb+') as destination:
            #         for chunk in request.FILES['image'].chunks():
            #             destination.write(chunk)
            # if request.FILES.get('attached_file'):
            #     with open('./qna/uploads'+ date_dir +'{}'.format(request.FILES.get('attached_file')), 'wb+') as destination:
            #         for chunk in request.FILES['attached_file'].chunks():
            #             destination.write(chunk)
            if request.FILES.get('image'):
                os.makedirs(MEDIA_ROOT + '/temp/', exist_ok=True)
                with open('./media/temp/{}'.format(request.FILES['image'].name), 'wb+') as destination:
                    for chunk in request.FILES['image'].chunks():
                        destination.write(chunk)
            if request.FILES.get('attached_file'):
                os.makedirs(MEDIA_ROOT + '/temp/', exist_ok=True)
                with open('./media/temp/{}'.format(request.FILES['attached_file'].name), 'wb+' ) as destination:
                    for chunk in request.FILES['attached_file'].chunks():
                        destination.write(chunk)


            original_information = OriginalInformation()
            original_information.remember(request, ['update'])

            original_information.image = request.POST['img_recent']
            original_information.attached_file = request.POST['file_recent']

            if question.image:
                current_image = str(question.image).split('/')[-1]
            else:
                current_image = ''
            if question.attached_file:
                current_file = str(question.attached_file).split('/')[-1]
            else:
                current_file = ''

            
            ctx = {
                'form': form, 
                'error_messages': error_messages,
                'original_information': original_information,
                'basic_tag_names': basic_tag_names,  
                'extra_tag_names': extra_tag_names,
                'current_image': current_image,
                'temp_img_location': '/media/qna/uploads'+ date_dir,
                'current_file': current_file,
                'temp_img_location': '/media/qna/uploads'+ date_dir,
                }
            return render(request, 'qna/question_form.html', context=ctx)

    else:
        form = QuestionForm(instance=question)
        # TODO : 선택 태그 뭘 선택했었는 지를 ctx로 넘겨주자
        # 기본 태그와 추가 태그 다르게 넘기자
        # TODO :  기본 태그 가 바뀌게 된다면 아래 리스트 수정해야 됨.
        if question.image:
            current_image = str(question.image).split('/')[-1]
        else:
            current_image = ''
        if question.attached_file:
            current_file = str(question.attached_file).split('/')[-1]
        else:
            current_file = ''

        tags = question.tags.all()
        basic_tag_names = []
        extra_tag_names = []
        for tag in tags:
            if tag.tag_name in basic_tags:
                basic_tag_names.append(tag.tag_name)
            else:
                extra_tag_names.append(tag.tag_name)
        ctx = {
            'form': form, 
            'question':question, 
            'basic_tag_names': basic_tag_names,  
            'extra_tag_names': extra_tag_names,
            'current_image': current_image,
            'temp_img_location': '/media/qna/uploads'+ date_dir,
            'current_file': current_file,
            'temp_file_location': '/media/qna/uploads'+ date_dir,
            }

        return render(request, template_name="qna/question_form.html", context=ctx)        

def question_delete(request, pk):
    user = request.user
    if user == AnonymousUser():
        return redirect('user:main')

    question = get_object_or_404(Question, pk=pk)

    # TODO : 게시글에 댓글이 있는지 확인
    if len(question.answer_set.all()) > 0:
        ### 답변이 달려 있어서 삭제 불가능
        return redirect('qna:question_detail', pk)
    update_question_cancel(question, request.user)
    question.delete()
    return redirect('qna:question_list')

############### ajax 관련 view 합수들

# 답변 작성 
@csrf_exempt
def answer_ajax(request):
    user = request.user
    if user == AnonymousUser():
        return redirect('user:main')

    req = json.loads(request.body)
    question_id = req['questionId']
    content = req['content']
    user_id = req['user']
    user = get_object_or_404(User, pk=user_id)
    username = user.nickname
    user_image_url = user.img.url if user.img else ''
    
    this_question = get_object_or_404(Question, pk=question_id)
    # 작성자 여부
    if this_question.user == None:
        is_author = False
    elif user_id == this_question.user.pk:
        is_author = True
    else: is_author= False

    ## 새 답변의 order 필드를 정해주기 위한 부분. 
    current_answers = Answer.objects.filter(question_id=question_id).order_by('answer_order')
    if len(current_answers)==0:
        new_order = 1
    else:
        new_order = current_answers.last().answer_order + 1

    ## 새로운 답변
    new_answer = Answer.objects.create(
        question_id=this_question, 
        content=content, 
        answer_order=new_order, 
        answer_depth = 0,
        user = user)
    # 템플릿에서 쉽게 띄울 수 있도록 답변 게시일자 포맷팅해서 json에 전달
    created_at = new_answer.created_at.strftime('%y.%m.%d %H:%M')

    update_answer(this_question, new_answer, this_question.user, request.user)

    response = JsonResponse({
        'id': new_answer.id ,
        'content': content,
        'user':username, 
        'created_at':created_at,
        'user_image_url':user_image_url,
        'is_author':is_author,
    })

    return response

# 대댓글 작성
@csrf_exempt
def reply_ajax(request):
    user = request.user
    if user == AnonymousUser():
        return redirect('user:main')

    req = json.loads(request.body)

    answer_id = req['answerId']
    content = req['content']
    user_id = req['user']
    user = get_object_or_404(User, pk=user_id)
    username = user.nickname
    # 작성하려는 대댓글이 속한 질문 구하기
    this_answer = get_object_or_404(Answer, pk=answer_id)
    this_question = this_answer.question_id

    user_image_url = user.img.url if user.img else ''
    # 작성자 여부
    if this_question.user == None:
        is_author = False
    elif user_id == this_question.user.pk:
        is_author = True
    else: is_author = False

    
    ## 새 답변의 order 필드를 정해주기 위한 부분. 
    current_answers = Answer.objects.filter(question_id=this_question.id).order_by('answer_order')
    if len(current_answers)==0:
        new_order = 1
    else:
        new_order = current_answers.last().answer_order + 1

    ## 새로운 대댓글
    new_answer = Answer.objects.create(
        question_id=this_question, 
        content=content, 
        answer_order=new_order, 
        answer_depth = 1,
        user = user,
        parent_answer = this_answer
    )

    update_answer_reply(this_question, new_answer, request.user)

    # 템플릿에서 쉽게 띄울 수 있도록 답변 게시일자 포맷팅해서 json에 전달
    created_at = new_answer.created_at.strftime('%y.%m.%d %H:%M')

    response = JsonResponse({
        'reply_id': new_answer.id,
        'answer_id' : this_answer.id,
        'content': content,
        'user':username, 
        'created_at':created_at,
        'user_image_url':user_image_url,
        'is_author':is_author,
    })

    return response

# 게시글(질문) 좋아요 기능
@csrf_exempt
def question_like_ajax(request):
    user = request.user
    if user == AnonymousUser():
        return redirect('user:main')

    req = json.loads(request.body)
    # user id 는 요청 안 보내도 됐을 수도
    question_id = req['questionId']

    question = get_object_or_404(Question, pk=question_id)
    liked_users = question.like_user

    is_liked = request.user in  liked_users.all()

    if is_liked:
        liked_users.remove(request.user)
        update_question_like_cancel(question, question.user, request.user)
    else:
        liked_users.add(request.user)
        update_question_like(question, question.user, request.user)

    total_likes = len(liked_users.all())
    return JsonResponse({'question_id':question_id, 'total_likes':total_likes, 'is_liking': not(is_liked)})

# 답변 (대댓글 포함) 좋아요 기능
@csrf_exempt
def answer_like_ajax(request):
    user = request.user
    if user == AnonymousUser():
        return redirect('user:main')

    req = json.loads(request.body)
    answer_id = req['id']

    answer = get_object_or_404(Answer, pk=answer_id)
    liked_users = answer.like_user

    is_liked = request.user in liked_users.all()
    
    if is_liked:
        liked_users.remove(request.user)
        update_comment_like_cancel(answer, answer.user, request.user)
    else:
        liked_users.add(request.user)
        update_comment_like(answer, answer.user, request.user)

    total_likes = len(liked_users.all())

    return JsonResponse({'answer_id':answer_id, 'total_likes':total_likes,  'is_liking': not(is_liked)})

# 답변(대댓글 포함) 삭제
@csrf_exempt
def answer_delete_ajax(request):
    user = request.user
    if user == AnonymousUser():
        return redirect('user:main')

    req = json.loads(request.body)
    answer_id = req['id']

    answer = get_object_or_404(Answer, pk=answer_id)
    
    if answer.answer_depth == 0:
        update_answer_cancel(answer.question_id, answer, answer.question_id.user, request.user)
    else:
        update_answer_reply_cancel(answer.question_id, answer, request.user)

    # 대댓글이거나 대댓글이 없는 답변의 경우 아예 삭제
    if answer.answer_set.count() == 0:
        # 마지막 대댓글이었다면 부모 답변도 삭제
        if answer.answer_depth == 1 and answer.parent_answer.answer_set.count() == 1 and answer.parent_answer.is_deleted == True:
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
    
    answer_count = Answer.objects.filter(question_id=answer.question_id, is_deleted=False, answer_depth=0).count()

    return JsonResponse({'id':answer_id, 'delete_yes':delete_yes, 'answer_count':answer_count})

# @csrf_exempt
# def answer_delete_ajax(request):
#     req = json.loads(request.body)
#     answer_id = req['id']

#     answer = get_object_or_404(Answer, pk=answer_id)
#     # 대댓글인 경우 아예 지우기
#     if answer.answer_depth == 1:
#         answer.delete()
#         update_answer_reply_cancel(answer.question_id, answer, request.user)
#     # 답변인 경우 내용만 삭제된 것처럼
#     else:
        
        
#         update_answer_cancel(answer.question_id, answer, answer.question_id.user, request.user)
#         answer.content = '삭제된 답변입니다.'
#         answer.user = None
#         answer.save()

#     return JsonResponse({'id':answer_id})

# 답변(대댓글 포함) 수정
# 수정버튼 눌렀을 때 해당하는 폼 띄우는 기능
@csrf_exempt
def answer_edit_ajax(request):
    user = request.user
    if user == AnonymousUser():
        return redirect('user:main')

    req = json.loads(request.body)
    answer_id = req['id']

    answer = get_object_or_404(Answer, pk=answer_id)
    # TODO : 고려해볼 사항. 원래 작성되어 있던 내용을 지금은 db에서 찾아서 넘겨주고 있는데
    # 그렇게 말고 data전송을 최소화화면서 프론트 단에서 그냥 현재 입력된 내용 받앙오기
    

    return JsonResponse({'id':answer_id})

# 답변(대댓글 포함) 수정
# 수정할 내용 입력 후 버튼 눌렀을 때 수정 내용 적용하는 기능
@csrf_exempt
def answer_edit_submit_ajax(request):
    user = request.user
    if user == AnonymousUser():
        return redirect('user:main')
        
    req = json.loads(request.body)
    answer_id = req['id']
    new_content = req['content']
    answer = get_object_or_404(Answer, pk=answer_id)
    answer.content = new_content
    answer.save()

    return JsonResponse({'id':answer_id, 'content':new_content})