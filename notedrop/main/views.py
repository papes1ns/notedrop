import json

from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import slugify
from django.forms import widgets

from .models import School, Course
from .forms import CourseForm

@login_required
def feed(request):
    return render(request, 'main/feed.html', {
        'user': request.user,
        'schools': request.user.profile.schools.all(),
        'courses': request.user.profile.courses.all()
    })

@login_required
def select_course(request, state=None, school=None, designator=None):
    if designator and school and state:
        school_str = school.replace('-', ' ')
        school = School.objects.filter(name__icontains=school_str)[0]
        courses = Course.objects.filter(designator__icontains=designator)
        return render(request, 'main/courses.html', {
            'courses': courses,
            'school': school,
            'designator': designator
        })

    if school and state:
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

@login_required
def post_course(request):
    if request.is_ajax():
        course_pk = request.POST['course_pk']
        course = Course.objects.get(pk=course_pk)
        request.user.profile.courses.add(course)
        request.user.profile.schools.add(course.school)
        return HttpResponse('GOOD')
    return HttpResponseBadRequest('BAD')

@login_required
def course_form(request):
    context = {}
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.save()
            request.user.profile.courses.add(course)
            request.user.profile.schools.add(course.school)
            return redirect('feed')
        else:
            context['form'] = form
            return render(request, 'main/course_form.html', context)

    form = CourseForm()
    if 'school' in request.GET:
        school_str = request.GET['school'].replace('-', ' ')
        school = School.objects.filter(name__icontains=school_str)
        if school:
            school = school[0]
            form.fields['school'].widget = widgets.HiddenInput()
            form.fields['school'].initial = school
            context['school'] = school

    if 'designator' in request.GET:
        designator = request.GET['designator'].upper()
        form.fields['designator'].initial = designator
        context['designator'] = designator

    context['form'] = form
    return render(request, 'main/course_form.html', context)
