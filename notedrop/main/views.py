from django.core import serializers
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import slugify
from django.forms import widgets

from .models import School, Course, UserProfile
from .forms import CourseForm

@login_required
def feed(request):
    return render(request, 'main/feed.html', {
        'user': request.user,
        'courses': request.user.profile.courses.all()
    })


@login_required
def profile(request):
    context = {}
    if request.is_ajax():
        course = Course.objects.get(pk=request.POST['course_pk'])
        if request.POST['action'] == 'Unfollow':
            request.user.profile.courses.remove(course)
        else:
            request.user.profile.courses.add(course)
        schools = School.objects.filter(pk__in=request.user.profile.courses.all().values('school').distinct())
        data = serializers.serialize('json', schools, fields=('name','state', 'city',))
        return HttpResponse(data)

    schools = School.objects.filter(pk__in=request.user.profile.courses.all().values('school').distinct())
    context['schools'] = schools
    courses = request.user.profile.courses.all()
    context['courses'] = courses
    return render(request, 'main/profile.html', context)

@login_required
def select_course(request, state=None, school=None, designator=None):
    context = {}
    if designator and school and state:
        school_str = school.replace('-', ' ')
        school = School.objects.filter(name__icontains=school_str)[0]
        courses = Course.objects.filter(designator__icontains=designator).exclude(userprofile__user=request.user)
        courses_users = []
        for c in courses:
            courses_users.append([c, UserProfile.objects.filter(courses=c).count()])

        context['courses_users'] = courses_users
        context['school'] = school
        context['designator'] = designator
        return render(request, 'main/courses.html', context)

    if school and state:
        school_str = school.replace('-', ' ')
        school = School.objects.filter(name__icontains=school_str)[0]
        designators = Course.objects.filter(school=school).values_list('designator', flat=True).distinct().order_by('designator')
        context['school'] = school
        context['designators'] = designators
        return render(request, 'main/designators.html', context)

    if state:
        state_str = state.replace('-', ' ')
        schools = School.objects.filter(state__icontains=state_str).order_by('name')
        context['schools'] = schools
        return render(request, 'main/schools.html', context)

    states = School.objects.values_list('state', flat=True).distinct().order_by('state')
    context['states'] = states
    return render(request, 'main/states.html', context)

@login_required
def post_course(request):
    # would rather have this form be a form post
    if request.is_ajax():
        course = Course.objects.get(pk=request.POST['course_pk'])
        if request.POST['action'] == 'Unfollow':
            request.user.profile.courses.remove(course)
        else:
            request.user.profile.courses.add(course)
        return HttpResponse('success')
    return HttpResponseBadRequest('error')

@login_required
def course_form(request):
    context = {}
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.save()
            request.user.profile.courses.add(course)
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
