from django.conf.urls import include, url
from django.contrib import admin
from main import views

urlpatterns = [
    url(r'^helm/', include(admin.site.urls)),
    
    url(r'^$', views.splash, name='splash'),
    
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^enroll/$', views.enroll, name='enroll'),
    url(r'^login/$', views.login_user, name='login'),
    
    url(r'^feed/', views.feed, name='feed'),
    
]
