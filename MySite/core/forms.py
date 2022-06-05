from django import forms
from core.models import Student, Teacher


class AddStudentForm(forms.Form):
    model = Student
    name = forms.CharField()
    email = forms.EmailField()

    def save(self):
        Student.objects.create(
            name=self.cleaned_data['name'],
            email=self.cleaned_data['email']
        )


class AddTeacherForm(forms.ModelForm):

    class Meta:
        model = Teacher
        fields = '__all__'   # or exclude = ('name_field, name_field') eto dlyz isclucheniya polei

    def save(self):
        teacher = super(AddTeacherForm, self).save()
        teacher.save()