from django import forms

from .models import Course, UserProfile, Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('course', 'content',)

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('school', 'designator', 'number', 'name',)

    number = forms.IntegerField(min_value=1, max_value=999)

    def clean_designator(self):
        designator = self.cleaned_data['designator']
        if len(designator) < 3:
            raise forms.ValidationError(
                'Ensure this value has 3 characters.',
                code='ValueLengthError'
            )
        designator = designator.upper()
        return designator

    def clean_number(self):
        number = self.cleaned_data['number']

        if number / 100 >= 1:
            number = str(number)
        elif number / 10 >= 1:
            number = '0' + str(number)
        else:
            number = '00' + str(number)

        return number

    def clean_name(self):
        name = self.cleaned_data['name']
        name = name.title()
        return name
