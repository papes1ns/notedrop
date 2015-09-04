from django.shortcuts import render


def splash(request, template="splash/splash.html"):
    return render(request, template)
