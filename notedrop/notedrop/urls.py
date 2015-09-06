from django.conf.urls import include, url
from django.contrib import admin
from main.views import feed, add_course
from authentication.views import login_user, logout_user, signup

urlpatterns = [
    url(r'^$', login_user, name='login'),
    url(r'^logout/$', logout_user, name='logout'),
    url(r'^feed/', feed, name='feed'),
    url(r'^courses/$', add_course, name='state_selection'),
    url(r'^courses/(?P<state>[a-zA-Z ]+)/$', add_course, name='school_selection'),
    url(r'^courses/(?P<state>[a-zA-Z ]+)/(?P<school>[a-zA-Z-&\' ]+)/$', add_course, name='course_selection'),
    url(r'^signup/$', signup, name='signup'),
    url(r'^helm/', include(admin.site.urls)),
]
