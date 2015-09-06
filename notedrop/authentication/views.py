from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import LoginForm

def login_user(request):
    context = {}
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

    form = LoginForm()
    context['form'] = form
    context['next'] = request.GET.get('next', None) or '/'
    return render(request, 'authentication/login.html', context)

def logout_user(request):
    logout(request)
    return redirect('feed')

def signup(request):
    context = {}
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('enroll')
        else:
            context['form'] = form
            return render(request, 'authentication/signup.html', context)
    form = UserCreationForm()
    context['form'] = form
    return render(request, 'authentication/signup.html', context)
