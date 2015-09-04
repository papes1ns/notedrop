from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponseNotAllowed
from django.contrib.auth.forms import UserCreationForm

from .forms import LoginForm


def splash(request, template='splash/splash.html'):
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
                    error_msg = 'Your account has been deactivated'
                    return render(request, template, {'login_error': error_msg})
            else:
                error_msg = 'Could not find a user with those credentials'
                return render(request, template, {'login_error': error_msg})
        else:
            return render(request, template, {'login_form': form})
    
    form = LoginForm()
    return render(request, template, {'login_form': form})

            
def signup(request, template='user/signup.html'):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('enroll')
        else:
            return render(request, template, {'form' : form})
    
    form = UserCreationForm()
    return render(request, template, {'form': form })
    
def enroll(request, template='user/enroll.html'):
    pass
