import django_filters
from django import forms
from .models import Post
from django.db.models.query import QuerySet

class RatingChoiceFilter(django_filters.ChoiceFilter):

    def filter(self, qs, value):
        if value == '1':
            return sorted(qs, key=lambda p: p.rating, reverse=True)
        elif value == '-1':
            return sorted(qs, key=lambda p: p.rating, reverse=False)
        else:
            return qs


class PostFilter(django_filters.FilterSet):
    class Meta:
        model = Post
        fields = ['course', 'created', 'rating']

    # def __init__(self, *args, **kwargs):
    #     self.user = kwargs.pop("user", None)
    #
    #     q = self.user.profile.courses.all()
    #     super(PostFilter, self).__init__(*args, **kwargs)

    RATING_CHOICES = (
        ('0', 'All'),
        ('1', 'High'),
        ('-1', 'Low')
    )

    # course = django_filters.ModelChoiceFilter(queryset=q)
    created = django_filters.DateRangeFilter()
    rating = RatingChoiceFilter(choices=RATING_CHOICES)
