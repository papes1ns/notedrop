from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from .forms import LoginForm


def login_user(request, template='authentication/login.html'):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('feed')
                else:
                    return render(request, template, {'form': form})
            else:
                return render(request, template, {'form': form})
    form = LoginForm()
    return render(request, template, {'form': form})


def signup(request, template='authentication/signup.html'):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('enroll')
        else:
            return render(request, template, {'form': form})
    form = UserCreationForm()
    return render(request, template, {'form': form})
