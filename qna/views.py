import queue
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib import messages
from django.db.models import Q
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def question_list(request):
    questions = Question.objects.all()
    ctx = {'questions': questions}

    return render(request, 'qna/question_list.html', context=ctx)

# # 검색 조건
# def search_condition(self):
#     search_keyword = self.request.GET.get('query', '')
#     search_type = self.request.GET.get('type', '')
#     questions = Question.objects.order_by('-id')

#     if search_keyword :
#         if len(search_keyword) > 1:
#             if search_type == 'all':
#                 search_questions = questions.filter(Q (title__icontains=search_keyword) | Q (content__icontains=search_keyword) | Q (writer__user_id__icontains=search_keyword))
#             elif search_type == 'title_content':    # 제목, 내용
#                 search_questions = questions.filter(Q (title__icontains=search_keyword) | Q (content__icontains=search_keyword))
#             elif search_type == 'title':    # 제목
#                 search_questions = questions.filter(title__icontains=search_keyword)    
#             elif search_type == 'content':  # 내용
#                 search_questions = questions.filter(content__icontains=search_keyword)    
#             elif search_type == 'writer':   # 작성자
#                 search_questions = questions.filter(writer__user_id__icontains=search_keyword)
            
#             return search_questions

#         else:
#             messages.error(self.request, '검색어는 2글자 이상 입력해주세요.')

#     return questions

# def search_result(self, **kwargs):
#     search_keyword = self.request.GET.get('search', '')
#     search_type = self.request.GET.get('type', '')

#     if len(search_keyword) > 1:
#         context['search'] = search_keyword
#         context['type'] = search_type

#     return context

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
        question = form.save(commit=False)
        question.user = request.user
        question.s_or_e_tag = request.POST.get('s_or_e_tag')
        question.save()
        return redirect('qna:question_list')

        # if form.is_valid():
        #     Question.objects.create(
        #         title = form.cleaned_data['title'],
        #         content = form.cleaned_data['content'],
        #         user = request.user,
        #     )
        # return redirect('qna:question_list')

    else:
        form = QuestionForm()
        ctx = {'form': form}
        
        return render(request, 'qna/question_create.html', context=ctx)
        
        
def question_detail(request, pk):
    question = get_object_or_404(Question, pk=pk)

    # 해당 게시글에 대한 tag, 유저, 좋아요 수 등 가져오기
    # 이외에 필드들은 template 에서 {{question.필드 }} 로 접근
    tags = question.tags.all()
    username = question.user.nickname
    total_likes = len(question.like_user.all())

    # 해당 게시글에 대한 답변 가져오기
    answers = Answer.objects.filter(question_id = question.id, parent_answer__isnull=True).order_by('answer_order')   #  나중에 답변 정렬도 고려. 최신순 또는 좋아요 순
    answers_count = len(answers)
    
    answers_reply_dict ={}
    for answer in answers:
        replies =  Answer.objects.filter(parent_answer= answer).order_by('answer_order')
        answers_reply_dict[answer] = replies

    # 좋아요 눌렀는지 안 눌렀는지
    is_liked = request.user in  question.like_user.all()

    ctx = {
        'question':question,
        'username': username,
        'tags' : tags,
        'total_likes' : total_likes,
        'answers' : answers,
        'answers_count' : answers_count,
        'answers_reply_dict' : answers_reply_dict,
        'is_liked': is_liked,
    }
    # answer 와 reply로 이루어진 dictionary를 context로 넘길 예정
    return render(request, template_name='qna/detail.html', context=ctx)

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

    return JsonResponse({'id': new_answer.id ,'content': content,'user':username, 'created_at':created_at} )

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
    else:
        liked_users.add(request.user)

    total_likes = len(liked_users.all())
    return JsonResponse({'question_id':question_id, 'total_likes':total_likes, 'is_liking': not(is_liked)})