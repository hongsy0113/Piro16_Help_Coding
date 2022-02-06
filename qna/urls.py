from django.urls import path
from . import views

app_name = 'qna'

urlpatterns = [
    path('', views.question_list, name='question_list'),
    path('search_result/', views.search_result, name='search_result'),
    path('question_create/', views.question_create, name='question_create'),
]