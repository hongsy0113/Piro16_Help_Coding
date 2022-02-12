
from multiprocessing.dummy import JoinableQueue
import queue
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib import messages
from django.db.models import Q
import json
from django.http import JsonResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator 
from django.db.models import Count
from django.views.generic import ListView, View
from hitcount.views import HitCountDetailView
from django.views.generic.detail import SingleObjectMixin
from django.core.files.storage import FileSystemStorage
import mimetypes
from user.update import *

basic_tags = ['동작', '형태', '소리', '이벤트', '제어',' 감지', '연산','변수', '내 블록', '기타']

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
class ErrorMessages():
    title, content, image, attached_file, s_or_e_tag, tags = '', '', '', '', '', ''
    def validation_check(self,title, content, image, attached_file, s_or_e_tag, tags, command):
        if 'create' in command or 'update' in command:
            if not title:
                self.title = '제목을 입력해주세요'
            elif len(title)>50:
                self.title = '제목은 50자 이내로 입력해주세요'
            if not content:
                self.content = '내용을 입력해주세요'
            if not s_or_e_tag:
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

    ctx = {
        'questions': page_obj,
        'sort_by':sort_by,
        'filter_by':tag_filter_by+[answer_filter_by],
    }

    return render(request, 'qna/question_list.html', context=ctx)

def search_result(request):
    if 'search' in request.GET:
        query = request.GET.get('search')
        questions = Question.objects.all().filter(
            Q(title__icontains=query) | # 제목으로 검색
            Q(content__icontains=query) # 내용으로 검색
        )

    return render(request, 'qna/search_result.html', {'query': query, 'questions': questions})

def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST, request.FILES)
        
        error_messages = ErrorMessages()
        error_messages.validation_check(
            form.data['title'],
            form.data['content'],
            request.FILES.get('image'),
            request.FILES.get('attached_file'),
            request.POST.get('s_or_e_tag'),
            request.POST.getlist('detail_tag'),
            ['create']
        )
        if not error_messages.has_error():
            question = Question.objects.create(
                title=form.data['title'],
                content=form.data['content'],
                image=form.data['image'],
                attached_file=form.data['attached_file'],
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

            question.save()
            update_question(question, request.user)
            return redirect('qna:question_detail', question.pk)

        # if form.is_valid():
        #     question = form.save(commit=False)  # 넘겨진 데이터 form에 바로 저장 X
        #     question.s_or_e_tag = request.POST.get('s_or_e_tag')  # 카테고리 (스크래치, 엔트리, 기타) 중 1 선택
        #     question.user = request.user
        #     question.save() 

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
            ctx = {
                'form': form, 
                'error_messages': error_messages,
                'original_information': original_information,
                'basic_tag_names': basic_tag_names,  
                'extra_tag_names': extra_tag_names,
                }
            return render(request, 'qna/question_form.html', context=ctx)
    else:
        form = QuestionForm()
        ctx = {'form': form}
        
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
        username = self.object.user.nickname
        total_likes = len(self.object.like_user.all())
        
        # 해당 게시글에 대한 답변 가져오기
        answers = Answer.objects.filter(question_id = self.object.id, parent_answer__isnull=True).order_by('answer_order')   #  나중에 답변 정렬도 고려. 최신순 또는 좋아요 순
        answers_count = len(answers)
        
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



def question_update(request,pk):
    question = get_object_or_404(Question, pk=pk)
    global basic_tags
    if request.method == "POST":
        form = QuestionForm(request.POST, request.FILES, instance =question)

        error_messages = ErrorMessages()
        error_messages.validation_check(
            form.data['title'],
            form.data['content'],
            request.FILES.get('image'),
            request.FILES.get('attached_file'),
            request.POST.get('s_or_e_tag'),
            request.POST.getlist('detail_tag'),
            ['update']
        )
        if not error_messages.has_error():
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
            original_information = OriginalInformation()
            original_information.remember(request, ['create'])
            ctx = {
                'form': form, 
                'error_messages': error_messages,
                'original_information': original_information,
                'basic_tag_names': basic_tag_names,  
                'extra_tag_names': extra_tag_names,
                }
            return render(request, 'qna/question_form.html', context=ctx)
        # question = form.save()  
        # question.s_or_e_tag = request.POST.get('s_or_e_tag')  # 카테고리 (스크래치, 엔트리, 기타) 중 1 선택

        # # 상세 태그 (기능) 선택
        # tags = request.POST.getlist('detail_tag')
        # for tag in tags:
        #     if len(QnaTag.objects.filter(tag_name=tag)) == 0:
        #         QnaTag.objects.create(
        #             tag_name = tag,
        #         )

        #     # QnaTag db에 없으면 오류 발생
        #     newtag = get_object_or_404(QnaTag, tag_name=tag)
        #     question.tags.add(newtag)

        # question.save()
        # update_question(question, request.user)

        # return redirect('qna:question_detail', pk)

    else:
        form = QuestionForm(instance=question)
        # TODO : 선택 태그 뭘 선택했었는 지를 ctx로 넘겨주자
        # 기본 태그와 추가 태그 다르게 넘기자
        # TODO :  기본 태그 가 바뀌게 된다면 아래 리스트 수정해야 됨.
        
        tags = question.tags.all()
        basic_tag_names = []
        extra_tag_names = []
        for tag in tags:
            if tag.tag_name in basic_tags:
                basic_tag_names.append(tag.tag_name)
            else:
                extra_tag_names.append(tag.tag_name)
        ctx = {'form': form, 'question':question, 'basic_tag_names': basic_tag_names,  'extra_tag_names': extra_tag_names}

        return render(request, template_name="qna/question_form.html", context=ctx)        

def question_delete(request, pk):
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
    req = json.loads(request.body)
    question_id = req['questionId']
    content = req['content']
    user_id = req['user']
    user = get_object_or_404(User, pk=user_id)
    username = user.nickname
    
    #### TODO ##########
    ## user 대표이미지 넘겨주는 건 유저 조금 구체화 된 다음에 추가

    ## 새 답변의 order 필드를 정해주기 위한 부분. 
    current_answers = Answer.objects.filter(question_id=question_id).order_by('answer_order')
    if len(current_answers)==0:
        new_order = 1
    else:
        new_order = current_answers.last().answer_order + 1

    this_question = get_object_or_404(Question, pk=question_id)

    ## 새로운 답변
    new_answer = Answer.objects.create(question_id=this_question, content=content, answer_order=new_order, user = user)
    # 템플릿에서 쉽게 띄울 수 있도록 답변 게시일자 포맷팅해서 json에 전달
    created_at = new_answer.created_at.strftime('%y.%m.%d %H:%M')

    update_answer(this_question, new_answer, this_question.user, request.user)

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
    this_answer = get_object_or_404(Answer, pk=answer_id)
    this_question = this_answer.question_id
    
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
    })

    return response

# 게시글(질문) 좋아요 기능
@csrf_exempt
def question_like_ajax(request):
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
    req = json.loads(request.body)
    answer_id = req['id']

    answer = get_object_or_404(Answer, pk=answer_id)
    if answer.parent_answer:
        update_answer_reply_cancel(answer.question_id, answer, request.user)
    else:
        update_answer_cancel(answer.question_id, answer, answer.question_id.user, request.user)
    answer.delete()

    return JsonResponse({'id':answer_id})

# 답변(대댓글 포함) 수정
# 수정버튼 눌렀을 때 해당하는 폼 띄우는 기능
@csrf_exempt
def answer_edit_ajax(request):
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
    req = json.loads(request.body)
    answer_id = req['id']
    new_content = req['content']
    answer = get_object_or_404(Answer, pk=answer_id)
    answer.content = new_content
    answer.save()

    return JsonResponse({'id':answer_id, 'content':new_content})