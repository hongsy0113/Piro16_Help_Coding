from django.urls import path
from . import views

app_name = "user"

urlpatterns = [
  path('', views.main, name="main"),
  path('login/', views.LoginView.as_view(), name="login"),
  path('logout/', views.log_out, name="logout"),
  path('signup/', views.sign_up, name="signup"),
  path('activate/<uid64>/<token>/', views.activate, name="activate"),
  path('mypage/', views.my_page, name="mypage"),
  path('mypage/revise/', views.my_page_revise, name="mypage_revise"),
  path('mypage/question/', views.QuestionView.as_view(), name="mypage_question"),
  path('mypage/answer/', views.AnswerView.as_view(), name="mypage_answer"),
]