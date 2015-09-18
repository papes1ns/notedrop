import django_filters
from django import forms
from .models import Post


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

    RATING_CHOICES = (
        ('0', 'All'),
        ('1', 'High'),
        ('-1', 'Low')
    )

    created = django_filters.DateRangeFilter()
    rating = RatingChoiceFilter(choices=RATING_CHOICES)
