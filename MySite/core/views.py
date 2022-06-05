from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView, FormView
from core.models import Student, Group, Teacher
from faker import Faker
from core.forms import AddStudentForm, AddTeacherForm

fake = Faker()


class MainPage(View):
    def get(self, request):
        return render(request=request, template_name='MainPage.html')


class GenerateStudent(TemplateView):
    template_name = 'GenerateStudent.html'
    success_url = 'generate-student/'

    def get_context_data(self, **kwargs):
        context = super(GenerateStudent, self).get_context_data(**kwargs)
        return context

    def post(self, request, **kwargs):

        context = super(GenerateStudent, self).get_context_data(**kwargs)

        Student.objects.create(name=fake.name(), email=fake.email())
        student = Student.objects.last()
        context.update({
            'student': student
        })
        return render(request, template_name='GenerateStudent.html', context=context)


class GenerateStudents(TemplateView):
    template_name = 'GenerateStudents.html'
    success_url = 'generate-students/'

    def get_context_data(self, **kwargs):
        context = super(GenerateStudents, self).get_context_data(**kwargs)
        return context

    def post(self, request, **kwargs):

        context = super(GenerateStudents, self).get_context_data(**kwargs)

        for count in range(int(request.POST.get('count'))):
            Student.objects.create(name=fake.name(), email=fake.email())
            student = Student.objects.order_by("-id")[0:int(request.POST.get('count'))]
            context.update({
                'student': student
            })

        return render(request=request, template_name='GenerateStudents.html', context=context)


class AllData(TemplateView):
    template_name = 'AllData.html'
    success_url = 'AllData/'

    def get_context_data(self, **kwargs):
        context = super(AllData, self).get_context_data(**kwargs)
        student = Student.objects.all
        teacher = Teacher.objects.all
        group = Group.objects.all
        context.update({
            'student': student,
            'teacher': teacher,
            'group': group,
        })
        return context


class StudentCreate(TemplateView):
    template_name = 'StudentCreate.html'

    def get_context_data(self, **kwargs):
        context = super(StudentCreate, self).get_context_data(**kwargs)
        student = Student.objects.last
        context.update({
            'student': student,
            'form': AddStudentForm,
        })
        return context

    def post(self, request):
        form = AddStudentForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('/create-student/')


class TeacherCreate(FormView):
    template_name = 'TeacherCreate.html'
    form_class = AddTeacherForm
    success_url = '/create-teacher/'

    def get_context_data(self, **kwargs):
        context = super(TeacherCreate, self).get_context_data(**kwargs)
        teacher = Teacher.objects.last()
        context.update({
            'teacher': teacher,
            'form': AddTeacherForm(),
        })
        return context

    def form_valid(self, form):
        form.save()
        return super(TeacherCreate, self).form_valid(form)
