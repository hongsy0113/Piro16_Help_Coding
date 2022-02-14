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
    path('mypage/reward/', views.RewardView.as_view(), name="mypage_reward"),
    path('mypage/reward/representative_ajax/',
         views.representative_reward_ajax, name="representative_reward_ajax"),
    path('mypage/point/', views.PointView.as_view(), name="mypage_point"),
    path('mypage/alert/', views.AlertView.as_view(), name="mypage_alert"),
    path('mypage/alert/check_ajax/',
         views.check_alert_ajax, name="check_alert_ajax"),
    path('mypage/alert/check_all_ajax/',
         views.check_all_alert_ajax, name="check_all_alert_ajax"),
]
