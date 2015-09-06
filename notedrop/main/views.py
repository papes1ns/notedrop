import json

from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import slugify

from .models import School, Course

@login_required
def feed(request):
    context = {
        'user': request.user,
        'schools': request.user.profile.schools.all(),
        'courses': request.user.profile.courses.all()
    }
    print context
    return HttpResponse('Logged in as {0}'.format(request.user))

@login_required
def select_course(request, state=None, school=None, designator=None):
    if designator:
        courses = Course.objects.filter(designator__icontains=designator)
        return render(request, 'main/courses.html', {'courses': courses})

    if school:
        school_str = school.replace('-', ' ')
        school = School.objects.filter(name__icontains=school_str)[0]
        designators = Course.objects.filter(school=school).values_list('designator', flat=True).distinct().order_by('designator')
        return render(request, 'main/designators.html', {
            'designators': designators,
            'school': school
        })

    if state:
        state_str = state.replace('-', ' ')
        schools = School.objects.filter(state__icontains=state_str).order_by('name')
        return render(request, 'main/schools.html', {'schools': schools})

    states = School.objects.values_list('state', flat=True).distinct().order_by('state')
    return render(request, 'main/states.html', {'states': states})

def post_course(request):
    if request.is_ajax():
        course_pk = request.POST['course_pk']
        course = Course.objects.get(pk=course_pk)
        request.user.profile.courses.add(course)
        request.user.profile.schools.add(course.school)
        return HttpResponse('GOOD')
    return HttpResponseBadRequest('BAD')
