from django.urls import path
from . import views
from .views import FileDownloadView

app_name = 'qna'

urlpatterns = [
    #path('',views.QuestionView.as_view(), name='question_list'),
    path('',views.question_list, name='question_list'),
    path('search_result/', views.search_result, name='search_result'),
    path('question_create/', views.question_create, name='question_create'),
    #path('question_create/', views.FileFieldFormView.as_view(), name='question_create'),
    #path('<int:pk>/', views.question_detail, name='question_detail'),
    path('<int:pk>/', views.QuestionDetailView.as_view(), name='question_detail'),
    path('<int:pk>/update', views.question_update, name='question_update'),
    path('<int:pk>/delete', views.question_delete, name='question_delete'),
    path('answer_ajax/', views.answer_ajax, name='answer_ajax'),
    path('reply_ajax/', views.reply_ajax, name='reply_ajax'),
    path('question_like_ajax/', views.question_like_ajax, name='question_like_ajax'),
    path('answer_like_ajax/', views.answer_like_ajax, name='answer_like_ajax'),
    path('answer_delete_ajax/', views.answer_delete_ajax, name='answer_delete_ajax'),
    path('answer_edit_ajax/', views.answer_edit_ajax, name='answer_edit_ajax'),
    path('answer_edit_submit_ajax/', views.answer_edit_submit_ajax, name='answer_edit_submit_ajax'),
    path('<int:pk>/download/', FileDownloadView.as_view(), name="download"),
]
