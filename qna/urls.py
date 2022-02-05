from django.urls import path
from . import views

app_name = 'qna'

urlpatterns = [
    #path('', views.qna_list, name='qna_list'),
    path('<int:pk>/', views.question_detail, name='question_detail'),
    path('answer_ajax/', views.answer_ajax, name='answer_ajax'),
    path('reply_ajax/', views.reply_ajax, name='reply_ajax'),
]