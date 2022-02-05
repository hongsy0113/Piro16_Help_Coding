from django.urls import path
from . import views

app_name = "user"

urlpatterns = [
  path('', views.main, name="main"),
  path('login/', views.LoginView.as_view(), name="login"),
  path('signup/', views.sign_up, name="signup"),
  path('logout/', views.log_out, name="logout"),
  path('mypage/', views.my_page, name="mypage")
]