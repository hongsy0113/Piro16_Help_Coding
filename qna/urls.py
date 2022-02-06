from django.urls import path
from . import views

app_name = 'qna'

urlpatterns = [
    path('', views.question_list, name='question_list'),
    path('search_result/', views.search_result, name='search_result'),
    path('question_create/', views.question_create, name='question_create'),
    path('<int:pk>/', views.question_detail, name='question_detail'),
    path('answer_ajax/', views.answer_ajax, name='answer_ajax'),
    path('reply_ajax/', views.reply_ajax, name='reply_ajax'),
]