from django.conf.urls import include, url
from django.contrib import admin
from main.views import feed, school_selection
from authentication.views import login_user, logout_user, signup

urlpatterns = [
    url(r'^$', login_user, name='login'),
    url(r'^logout/$', logout_user, name='logout'),
    url(r'^feed/', feed, name='feed'),
    url(r'^school-selection/$', school_selection, name='state-selection'),
    url(r'^school-selection/(?P<state>[a-zA-Z ]+)/$', school_selection, name='school-selection'),
    url(r'^signup/$', signup, name='signup'),
    url(r'^helm/', include(admin.site.urls)),
]
