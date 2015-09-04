from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm

from .forms import LoginForm


def splash(request, template='splash/splash.html'):

    return render(request, template)
    
def feed(request, template='feed/main.html'):
    return HttpResponse("GOOD Logged in as {0}".format(request.user))

def login_user(request, template='user/login.html'):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'],
                                        password=form.cleaned_data['password'])
            if user is not None:
                print "USER is NONE"
                if user.is_active:
                    login(request, user)
                    return redirect('feed')
                else:
                    error_msg = 'Your account has been deactivated'
                    return render(request, template, {
                        'login_error': error_msg,
                        'form': form,
                    })
            else:
                error_msg = 'Could not find a user with those credentials'
                return render(request, template, {
                    'login_error': error_msg,
                    'form': form,
                })
        else:
            return render(request, template, {'form': form})
    
    return render(request, template, {'form': form})
    
            
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
    return HttpResponse("Congrats on signing up")
