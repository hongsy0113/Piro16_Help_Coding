from distutils.command.clean import clean
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib import messages
from django.db.models import Q

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