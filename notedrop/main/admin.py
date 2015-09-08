from django.contrib import admin
from .models import (
    UserProfile,
    Course,
    School,
    Post,
    PostData
)


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'modified',)
    list_filter = ('courses',)

admin.site.register(UserProfile, UserProfileAdmin)


class CourseAdmin(admin.ModelAdmin):
    list_display = ('designator', 'number',)
    list_filter = ('school', 'designator')

admin.site.register(Course, CourseAdmin)


class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'state', 'city')
    list_filter = ('state',)

admin.site.register(School, SchoolAdmin)


class PostAdmin(admin.ModelAdmin):
    list_display = ('content', 'author', 'course', 'created', 'archived')
    list_filter = ('course', 'created', 'archived')

admin.site.register(Post, PostAdmin)


class PostDataAdmin(admin.ModelAdmin):
    list_display = ('post','user', 'upvote', 'noted')

admin.site.register(PostData, PostDataAdmin)
