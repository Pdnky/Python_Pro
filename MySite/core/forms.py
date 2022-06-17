from django import forms
from core.models import Student, Teacher


class AddStudentForm(forms.ModelForm):
    model = Student
    name = forms.CharField()
    email = forms.EmailField()

    class Meta:
        model = Student
        fields = '__all__'

    def clean_name(self):

        name = self.cleaned_data['name']
        matching_names = Student.objects.values('id', 'name').filter(name__icontains=name)
        surname = name.split(' ')

        if len(matching_names) == 0 and len(surname) <= 1:
            raise forms.ValidationError('Enter the first and last name and then try again.')

        elif len(matching_names) > 0:
            for item in matching_names:
                surname_students = item['name'].split(' ')

                if len(surname) > 1 and len(surname_students) > 1 and self.initial != {}:
                    if surname[1].lower() == surname_students[1].lower() and self.initial['id'] != item['id']:
                        raise forms.ValidationError('Unfortunately a student with that Surname already exists.')

                elif len(surname) > 1 and len(surname_students) > 1 and self.initial == {}:
                    raise forms.ValidationError('Unfortunately a student with that Surname already exists.')

                else:
                    raise forms.ValidationError('Please Enter Surname.')
        return name

class AddTeacherForm(forms.ModelForm):

    class Meta:
        model = Teacher
        fields = '__all__'

