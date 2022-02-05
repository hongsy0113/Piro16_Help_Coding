from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from .forms import LoginForm, SignupForm
from .models import User

def main(request):
    return render(request, 'user/main.html')

# Login
class LoginView(View):
    def post(self, request):
      form = LoginForm(request.POST)
      if form.is_valid():
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username = email, password = password)
        if user is not None:
          login(request, user)
          return redirect('user:main')
      ctx = {'form': form}
      return render(request, 'user/login.html', ctx)

    def get(self, request):
      form = LoginForm()
      return render(request, 'user/login.html', {'form': form})

# Logout
def log_out(request):
    logout(request)
    return redirect('user:main')

def sign_up(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            user = User.objects.create_user(
                username = request.POST['email'],
                email = request.POST['email'],
                password = request.POST['password1'],
                nickname = request.POST['nickname'],
                birth = request.POST['birth'],
                img = request.FILES.get('img'),
                introduction = request.POST['introduction'],
                total_like = 0,
                job = request.POST['job'],
            )
            login(request, user)
            return redirect('user:main')
    else:
        form = SignupForm()
        return render(request, 'user/signup.html', {"form": form})


# Sign Up
'''
def sign_up(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            user = User.objects.create_user(
                username = request.POST['email'],
                email = request.POST['email'],
                password = request.POST['password1'],
                nickname = request.POST['nickname'],
                birth = request.POST['birth'],
                img = request.POST['img'],
                introduction = request.POST['introduction'],
                total_like = 0,
                job = request.POST['job'],
            )
            login(request, user)
            return redirect('user:main')
    else:
        form = SignupForm()
        return render(request, 'user/signup.html', {"form": form})
'''