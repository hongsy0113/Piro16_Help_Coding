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
    path('mypage/reward/', views.my_page_reward, name="mypage_reward"),
    path('mypage/reward/representative_ajax/',
         views.representative_reward_ajax, name="representative_reward_ajax"),
    path('mypage/reward/date_ajax/',
         views.date_reward_ajax, name="date_reward_ajax"),
    path('mypage/point/', views.PointView.as_view(), name="mypage_point"),
    path('mypage/alert/', views.AlertView.as_view(), name="mypage_alert"),
    path('mypage/alert/check_ajax/',
         views.check_alert_ajax, name="check_alert_ajax"),
    path('mypage/alert/check_all_ajax/',
         views.check_all_alert_ajax, name="check_all_alert_ajax"),
    path('mypage/alert/load_new_ajax/',
         views.load_new_alert_ajax, name="load_new_alert_ajax"),
    path('<int:pk>/public_userpage/',
         views.public_userpage, name='public_userpage'),
    path('group_wait_profile/', view=views.group_wait_profile,
         name='group_wait_profile'),
    path('drop/', views.drop, name="drop"),
    path('drop_success/', views.drop_success, name="drop_success"),
    path('periodic_tasks/', views.periodic_tasks, name="periodic_tasks"),
    path('periodic_tasks_immediate/', views.periodic_tasks_immediate, name="periodic_tasks_immediate"),
    path('initialize_rewards/', views.initialize_rewards, name="initialize_rewards"),
]
