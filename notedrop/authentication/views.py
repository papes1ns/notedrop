from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import LoginForm


def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    if request.user.profile.courses.count() == 0:
                        return redirect('state-selection')
                    return redirect('feed')
                else:
                    return render(request, 'authentication/login.html', {'form': form})
            else:
                return render(request,'authentication/login.html', {'form': form})
    form = LoginForm()
    return render(request, 'authentication/login.html', {'form': form})

def logout_user(request):
    logout(request)
    return redirect('login')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('enroll')
        else:
            return render(request, 'authentication/signup.html', {'form': form})
    form = UserCreationForm()
    return render(request, 'authentication/signup.html', {'form': form})
