import requests
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.views import View
from urllib.parse import urlencode
from accounts.forms import RegisterForm, LoginForm, ForgetPasswordForm, ResetPasswordForm
from accounts.models import User
from accounts.utils import login_required
from config import settings


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password'))
            user.save()
            # data = form.cleaned_data
            # User.objects.create_user(
            #     username=data.get('username'),
            #     password=data.get('password')
            # )
            return redirect('post:list')
        else:
            return render(request, 'accounts/register.html', {'form': form})
    else:
        form = RegisterForm()
        return render(request, 'accounts/register.html', {'form': form})


def login_(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data.get('user')
            login(request, user)
            return redirect('post:list')
        else:
            return render(request, 'accounts/login.html', {'form': form})

    else:
        form = LoginForm()
        return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_(request):
    logout(request)
    return redirect('login')


class ForgotPasswordView(View):
    def get(self, request):
        form = ForgetPasswordForm()
        return render(request, 'registration/forgot_password.html', {'form': form})

    def post(self, request):
        form = ForgetPasswordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('restore_password')
        else:
            return render(request, 'registration/forgot_password.html', {'form': form})


class RestoreView(View):
    def get(self, request):
        form = ResetPasswordForm()
        return render(request, 'registration/restore_password.html', {'form': form})

    def post(self, request):
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            return render(request, 'registration/restore_password.html', {'form': form})


def google_redirect(request):
    base_url = settings.GOOGLE_AUTH_URL

    params = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
    }

    url = f"{base_url}?{urlencode(params)}"
    return redirect(url)


def google_callback(request):
    code = request.GET.get("code")

    token_data = {
        "code": code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    token_json = requests.post(
        settings.GOOGLE_TOKEN_URL, data=token_data
    ).json()
    access_token = token_json.get("access_token")

    # 2. Foydalanuvchi ma'lumotlari
    user_info = requests.get(
        settings.GOOGLE_USER_INFO_URL,
        headers={"Authorization": f"Bearer {access_token}"}
    ).json()

    user, _ = User.objects.get_or_create(email=user_info.get("email"))
    user.first_name = user_info["given_name"]
    user.last_name = user_info["family_name"]
    user.save()
    login(request, user)
    return redirect('post:list')
