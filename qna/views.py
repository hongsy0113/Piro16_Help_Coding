from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from .models import * 
from django.db.models import Q
# Create your views here.
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def question_detail(request, pk):
    question = get_object_or_404(Question, pk=pk)

    # 해당 게시글에 대한 tag, 유저, 좋아요 수 등 가져오기
    # 이외에 필드들은 template 에서 {{question.필드 }} 로 접근
    tags = question.tags.all()
    username = question.user.nickname
    total_likes = len(question.like_user.all())

    # 해당 게시글에 대한 답변 가져오기
    answers = Answer.objects.filter(question_id = question.id) # 나중에 답변 정렬도 고려. 최신순 또는 좋아요 순
    answers_count = len(answers)
    ctx = {
        'question':question,
        'username': username,
        'tags' : tags,
        'total_likes' : total_likes,
        'answers' : answers,
        'answers_count' : answers_count,
    }

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
