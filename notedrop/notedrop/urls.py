from django.conf.urls import include, url
from django.contrib import admin
from main.views import feed, enroll, school_search
from authentication.views import login_user, signup

urlpatterns = [
    url(r'^helm/', include(admin.site.urls)),
    url(r'^$', login_user, name='login'),
    url(r'^signup/$', signup, name='signup'),
    url(r'^enroll/$', enroll, name='enroll'),
    url(r'^feed/', feed, name='feed'),
    url(r'^search/', school_search, name='search'),
]
