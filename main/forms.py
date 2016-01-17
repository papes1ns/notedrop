from django import forms

from .models import Course, UserProfile, Post


class PostForm(forms.ModelForm):
    course = forms.ModelChoiceField(queryset=Course.objects.all())
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 50}))

    class Meta:
        model = Post
        fields = ('course', 'content', 'image')
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super(PostForm, self).__init__(*args, **kwargs)
        if user is not None:
            self.fields["course"].queryset = user.profile.courses.all()


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
