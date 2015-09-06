import json

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import School

@login_required
def feed(request):
    return HttpResponse('Logged in as {0}'.format(request.user))


@login_required
def add_course(request, state=None, school=None):
    if school:
        courses = []
        return render(request, 'main/courses.html', {'courses': courses})

    if state:
        schools = School.objects.filter(state=state).order_by('name')
        return render(request, 'main/schools.html', {'schools': schools})

    states = School.objects.values_list('state', flat=True).distinct().order_by('state')
    return render(request, 'main/states.html', {'states': states})
