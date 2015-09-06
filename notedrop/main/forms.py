from django import forms

from .models import Course


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('school', 'designator', 'number', 'name', 'section')

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
        number = str(self.cleaned_data['number'])
        if len(number) < 3:
            raise forms.ValidationError(
                'Ensure this value has 3 characters.',
                code='ValueLengthError'
            )
        return number

    def clean_name(self):
        name = self.cleaned_data['name']
        name = name.title()
        return name
