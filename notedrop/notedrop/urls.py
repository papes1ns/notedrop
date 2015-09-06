from django.conf.urls import include, url
from django.contrib import admin
from main.views import feed, select_course, post_course, course_form
from authentication.views import login_user, logout_user, signup

urlpatterns = [
    url(r'^$', feed, name='feed'),
    url(r'^login/', login_user, name='login'),
    url(r'^logout/$', logout_user, name='logout'),
    url(r'^courses/$', select_course, name='state_selection'),
    url(r'^courses/(?P<state>[a-zA-Z- ]+)/$', select_course, name='school_selection'),
    url(r'^courses/(?P<state>[a-zA-Z- ]+)/(?P<school>[a-zA-Z- ]+)/$', select_course, name='designator_selection'),
    url(r'^courses/(?P<state>[a-zA-Z- ]+)/(?P<school>[a-zA-Z- ]+)/(?P<designator>[a-zA-Z]+)/$', select_course, name='course_selection'),
    url(r'^post-course/$', post_course, name='post_course'),
    url(r'^course-form/', course_form, name='course_form'),
    url(r'^signup/$', signup, name='signup'),
    url(r'^helm/', include(admin.site.urls)),
]
