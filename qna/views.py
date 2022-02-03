from django.shortcuts import render, redirect, get_object_or_404
from .models import *

# Create your views here.
def question_list(request):
    questions = Question.objects.all()
    ctx = {'questions': questions}
    return render(request, 'qna/question_list.html', context=ctx)