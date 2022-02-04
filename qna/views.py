from django.shortcuts import render, redirect, get_object_or_404
from .models import * 
from django.db.models import Q
# Create your views here.

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
    answer_1 = answers.first()
    print(answer_1.like_user.all())
    return render(request, template_name='qna/detail.html', context=ctx)
