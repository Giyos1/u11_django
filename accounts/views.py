from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect

from accounts import forms
from accounts.forms import RegisterForm, LoginForm


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
            data = form.cleaned_data
            user = authenticate(username=data.get('username'), password=data.get('password'))
            if user:
                login(request, user)
                return redirect('post:list')
            else:
                return HttpResponse('xato')
        else:
            return render(request, 'accounts/login.html', {'form': form})

    else:
        form = LoginForm()
        return render(request, 'accounts/login.html', {'form': form})
