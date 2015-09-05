import json

from django.http import HttpResponse
from django.shortcuts import render, redirect

from .models import School


def feed(request, template='feed/main.html'):
    return HttpResponse("GOOD Logged in as {0}".format(request.user))


def enroll(request, template='authentication/enroll.html'):
    return HttpResponse("Congrats on signing up")


def school_search(request, template='main/search.html'):
    if request.method == 'POST':
        q = request.POST.get('q', None)
        if q:
            results = list(School.objects.filter(name__icontains=q).values(
                                                    'name', 'city', 'state'))
            results = json.dumps(results)
            print results
            return HttpResponse(results,
                                content_type='application/json')

    return render(request, template)
