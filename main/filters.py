import django_filters
from django import forms
from .models import Post, Course


class RatingChoiceFilter(django_filters.ChoiceFilter):

    def filter(self, qs, value):
        if value == '1':
            return sorted(qs, key=lambda p: p.rating, reverse=True)
        elif value == '-1':
            return sorted(qs, key=lambda p: p.rating, reverse=False)
        else:
            return qs


class PostFilter(django_filters.FilterSet):
    RATING_CHOICES = (
        ('0', 'All'),
        ('1', 'High'),
        ('-1', 'Low')
    )

    course = django_filters.ModelChoiceFilter(queryset=Course.objects.all())
    created = django_filters.DateRangeFilter()
    rating = RatingChoiceFilter(choices=RATING_CHOICES)

    class Meta:
        model = Post
        fields = ['course', 'created', 'rating']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super(PostFilter, self).__init__(*args, **kwargs)
        if user is not None:
            self.form.fields["course"].queryset = user.profile.courses.all()
