import json
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.forms import widgets

from .models import School, Course, UserProfile, Post, PostData
from .forms import CourseForm, PostForm
from .filters import PostFilter


@login_required
def feed(request):
    context = {}
    posts = []
    f = PostFilter(request.GET, queryset=Post.objects.filter(archived=False, course__in=request.user.profile.courses.all()).order_by('-created'))
    
    for p in f:
        post_data, created = PostData.objects.get_or_create(post=p, user=request.user)
        posts.append({
            'obj': p,
            'noted': post_data.noted,
            'upvote': post_data.upvote
        })

    
    paginator = Paginator(posts, 5)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)

    context['posts'] = posts
    form = PostForm()
    if 'course' in request.GET:
        form.fields['course'].initial = request.GET['course']
    context['form'] = form
    context['filter'] = f
    return render(request, 'main/feed.html', context)


@login_required
def note_drop(request):
    referer =  request.META.get('HTTP_REFERER', None)
    if request.method == 'POST':
        form = PostForm(request.POST)
        errors = []
        if form.is_valid():
            form = form.save(commit=False)
            form.author = request.user
            form.save()
            return HttpResponse(referer)
        else:
            for k, v in form.errors.as_data().iteritems():
                field = k.title()
                for msg in v:
                    errors.append('{field}: {msg}'.format(field=field, msg=str(msg[0])))
            return HttpResponseBadRequest(json.dumps(errors))

@login_required
def profile(request, username=None):
    context = {}
    if request.is_ajax():
        if request.POST.get('course_pk', None):
            course = Course.objects.get(pk=request.POST['course_pk'])
            if request.POST['action'] == 'Unfollow':
                request.user.profile.courses.remove(course)
            else:
                request.user.profile.courses.add(course)
            schools = School.objects.filter(pk__in=request.user.profile.courses.all().values('school').distinct())
            data = serializers.serialize('json', schools, fields=('name','state', 'city',))
            return HttpResponse(data)
        
        if request.POST.get('notify_count', None):
            profile = UserProfile.objects.get(user=request.user)
            profile.notify_count = request.POST['notify_count']
            profile.save()
            return HttpResponse(profile.notify_count)
        
    context['notify_count'] = request.user.profile.notify_count
    context['posts'] = Post.objects.filter(archived=False, author=request.user)
    context['schools'] = School.objects.filter(pk__in=request.user.profile.courses.all().values('school').distinct())
    context['courses'] = request.user.profile.courses.all()
    return render(request, 'main/profile.html', context)

@login_required
def select_course(request, state=None, school=None, designator=None):
    context = {}
    if designator and school and state:
        school_str = school.replace('-', ' ')
        courses = Course.objects.filter(designator__icontains=designator).exclude(userprofile__user=request.user)
        courses_users = []
        for c in courses:
            courses_users.append([c, UserProfile.objects.filter(courses=c).count()])

        context['courses_users'] = courses_users
        context['school'] = school = School.objects.filter(name__icontains=school_str)[0]
        context['designator'] = designator
        return render(request, 'main/courses.html', context)

    if school and state:
        school_str = school.replace('-', ' ')
        school = School.objects.filter(name__icontains=school_str)[0]
        context['school'] = school
        context['designators'] = Course.objects.filter(school=school).values_list('designator', flat=True).distinct().order_by('designator')
        return render(request, 'main/designators.html', context)

    if state:
        state_str = state.replace('-', ' ')
        schools = School.objects.filter(state__icontains=state_str).order_by('name')
        context['schools'] = schools
        return render(request, 'main/schools.html', context)

    context['states'] = School.objects.values_list('state', flat=True).distinct().order_by('state')
    return render(request, 'main/states.html', context)

@login_required
def post_course(request):
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

@login_required
def post_options(request):
    if 'noted_pk' in request.POST:
        post_data = PostData.objects.get(post=request.POST['noted_pk'], user=request.user)
        if post_data.noted is False:
            post_data.noted = True
        else:
            post_data.noted = False
        post_data.save()
        return HttpResponse(json.dumps(post_data.noted))

    if 'up_pk' in request.POST:
        post_data = PostData.objects.get(post=request.POST['up_pk'], user=request.user)
        if post_data.upvote is not True:
            post_data.upvote = True
        else:
            post_data.upvote = None
        post_data.save()
        return HttpResponse(json.dumps({'post_pk': post_data.post.pk, 'rating': post_data.post.rating, 'upvote': post_data.upvote}))

    if 'down_pk' in request.POST:
        post_data = PostData.objects.get(post=request.POST['down_pk'], user=request.user)
        if post_data.upvote is not False:
            post_data.upvote = False
        else:
            post_data.upvote = None
        post_data.save()
        return HttpResponse(json.dumps({'post_pk': post_data.post.pk, 'rating': post_data.post.rating, 'upvote': post_data.upvote}))

    return HttpResponseBadRequest()

@login_required
def users(request, username=None):
    context = {}
    q = UserProfile.objects.get(user__username=username)
    context['username'] = q.user.username
    context['posts'] = Post.objects.filter(author=q.user)
    context['courses'] = q.courses.all()
    context['schools'] = School.objects.filter(pk__in=q.courses.all().values('school').distinct())
    return render(request, 'main/users.html', context)

@login_required
def posts(request, post_pk=None):
    context = {}
    post = Post.objects.filter(pk=int(post_pk))
    if post:
        context['post'] = post[0]
    return render(request, 'main/posts.html', context)

def post_delete(request, post_pk=None):
    if post_pk:
        post_pk = int(post_pk)
        if any(p.pk == post_pk for p in Post.objects.filter(author=request.user)):
            post = Post.objects.get(pk=post_pk)
            post.archived = True
            post.save()

    return redirect('profile')
    
@login_required
def starred(request):
    context = {}
    context['posts'] = PostData.objects.filter(user=request.user, noted=True)
    return render(request, 'main/starred.html', context)
