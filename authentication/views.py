from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse

from .forms import LoginForm, SignupForm


def login_user(request):
    context = {}
    error = ""
    if request.user.is_authenticated():
        return redirect('feed')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    if request.user.profile.courses.count() == 0:
                        return redirect('state_selection')
                    r = request.GET.get('next', None) or '/'
                    return redirect(r)
                else:
                    error = 'This account is no longer active.'
            else:
                error = 'Username or Password is incorrect.'
        else:
            for k, v in form.errors.as_data().iteritems():
                field = k.title()
                for msg in v:
                    error += '{field}: {msg}\n'.format(field=field, msg=str(msg[0]))

    context['error'] = error
    context['form'] =  LoginForm()
    context['next'] = request.GET.get('next', None) or '/'
    return render(request, 'authentication/login.html', context)

def logout_user(request):
    logout(request)
    return redirect('feed')

def signup(request):
    context = {}
    error = ""
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(username=request.POST['username'], password=request.POST['password1'])
            login(request, user)
            return redirect('feed')
        else:
            for k, v in form.errors.as_data().iteritems():
                field = k.title()
                for msg in v:
                    error += '{field}: {msg}\n'.format(field=field, msg=str(msg[0]))

            context['error'] = error
            context['form'] = form
            return render(request, 'authentication/signup.html', context)

    context['form'] = SignupForm()
    return render(request, 'authentication/signup.html', context)
