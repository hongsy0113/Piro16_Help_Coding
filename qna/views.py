from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.db.models import Q

# Create your views here.
def question_list(request):
    questions = Question.objects.all()
    ctx = {'questions': questions}

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
        if form.is_valid():
            question = form.save()
            return redirect('qna:question_list')
    else:
        form = QuestionForm()
    ctx = {'form': form}
    return render(request, 'qna/question_form.html', context=ctx)