from django.conf.urls import include, url
from django.contrib import admin
from main.views import feed, select_course, post_course, course_form, profile, post_options, users, posts, post_delete, starred, note_drop
from authentication.views import login_user, logout_user, signup


from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^$', feed, name='feed'),
    url(r'^posts/(?P<post_pk>[0-9]+)/$', posts, name='posts'),
    url(r'^posts/delete/(?P<post_pk>[0-9]+)/$', post_delete, name='post_delete'),
    url(r'^users/(?P<username>[a-zA-Z0-9-@]+)/$', users, name='users'),
    url(r'^starred/$', starred, name='starred'),
    url(r'^courses/$', select_course, name='state_selection'),
    url(r'^courses/(?P<state>[a-zA-Z- ]+)/$', select_course, name='school_selection'),
    url(r'^courses/(?P<state>[a-zA-Z- ]+)/(?P<school>[a-zA-Z- ]+)/$', select_course, name='designator_selection'),
    url(r'^courses/(?P<state>[a-zA-Z- ]+)/(?P<school>[a-zA-Z- ]+)/(?P<designator>[a-zA-Z]+)/$', select_course, name='course_selection'),
    url(r'^post-course/$', post_course, name='post_course'),
    url(r'^post-note/$', note_drop, name='note_drop'),
    url(r'^post-options/', post_options, name='post_options'),
    url(r'^course-form/', course_form, name='course_form'),
    url(r'^profile/$', profile, name='profile'),
    url(r'^login/', login_user, name='login'),
    url(r'^logout/$', logout_user, name='logout'),
    url(r'^signup/$', signup, name='signup'),
    url(r'^helm/', include(admin.site.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
