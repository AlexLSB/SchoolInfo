# -*- coding: utf-8 -*-
from django.views import generic
from django.shortcuts import get_object_or_404
from django.db.models import F
from app.models import Student, Teacher, SchoolClass, Subject, School

class HomeView(generic.TemplateView):
    template_name = 'base.html'


class TeacherListView(generic.ListView):
    '''Список всех учителей'''
    model = Teacher

    def get_queryset(self):
        queryset = Teacher.objects.all().prefetch_related('subject')
        return queryset


class SchoolListView(generic.ListView):
    '''Список всех учителей'''
    model = School


class SchoolDetailView(generic.DetailView):
    '''Список всех учителей'''
    model = School

    def get_queryset(self):
        qs = super(SchoolDetailView, self).get_queryset()
        return qs.prefetch_related('classes')


class SubjectListView(generic.ListView):
    '''Список всех предметов'''
    model = Subject


class SchoolClassDetailView(generic.DetailView):
    '''Страница класса'''
    model = SchoolClass

    def get_queryset(self):
        qs = super(SchoolClassDetailView, self).get_queryset()
        return qs.prefetch_related('students', 'teacher', 'teacher__subject')


class TeacherStudentsView(generic.ListView):
    '''Список учеников данного преподавателя'''
    template_name = 'app/teacher_students.html'

    def get_context_data(self, **kwargs):
        context = super(TeacherStudentsView, self).get_context_data(**kwargs)
        context['teacher'] = Teacher.objects.get(slug=self.kwargs['slug'])
        return context

    def get_queryset(self):
        queryset = Student.objects.filter(school_class__teacher__slug=self.kwargs['slug'])
        return queryset


class TeacherGradeStudentsByClassView(TeacherStudentsView):
    '''1 (1). Список учеников данного преподавателя конкретной параллели (например,
        по десятым классам) всех школ с группировкой по классам и сортировкой по
    алфавиту внутри каждого класса, с указанием школы и класса для каждого ученика'''
    template_name = 'app/teacher_grade_students_by_class.html'
    context_object_name = 'teachers_classes'

    def get_context_data(self, **kwargs):
        context = super(TeacherGradeStudentsByClassView, self).get_context_data(**kwargs)
        context['grade'] = self.kwargs['grade']
        return context

    def get_queryset(self):
        queryset = SchoolClass.objects.filter(
            teacher__slug=self.kwargs['slug'], grade=self.kwargs['grade']
        ).prefetch_related('students', 'students__school_class', 'students__school_class__school')
        return queryset


class TeacherGradeStudentsView(TeacherGradeStudentsByClassView):
    '''1 (2). Список учеников данного преподавателя конкретной параллели (например,
        по десятым классам) всех школ без группировки, с сортировкой по алфавиту
     и с указанием школы и класса для каждого ученика.'''
    template_name = 'app/teacher_grade_students.html'
    context_object_name = 'student_list'

    def get_queryset(self):
        queryset = Student.objects.filter(
            school_class__teacher__slug=self.kwargs['slug'], school_class__grade=self.kwargs['grade']
        ).order_by('full_name').prefetch_related('school_class', 'school_class__school')
        return queryset


class SubjectStudentsView(generic.ListView):
    '''2.2. Список учеников, обучающихся по данному предмету общим
    алфавитным списком с указанием школы, класса и ФИО преподавателя'''
    template_name = 'app/subject_students.html'

    def get_context_data(self, **kwargs):
        context = super(SubjectStudentsView, self).get_context_data(**kwargs)
        context['subject'] = get_object_or_404(Subject, slug=self.kwargs['slug'])
        return context

    def get_queryset(self):
        queryset = Student.objects.filter(
            school_class__teacher__subject__slug=self.kwargs['slug']) \
            .order_by('full_name').prefetch_related('school_class', 'school_class__school',) \
            .annotate(teacher=F('school_class__teacher__full_name'))
        return queryset


class SubjectStudentsByTeacherView(SubjectStudentsView):
    '''2.1. Список учеников, обучающихся по данному предмету с группировкой по преподавателям
    с указанием для каждого ученика школы и класса'''
    template_name = 'app/subject_students_by_teacher.html'

    def get_queryset(self):
        queryset = Teacher.objects.filter(subject__slug=self.kwargs['slug']).prefetch_related(
            'classes__students', 'classes')
        return queryset


class SubjectStudentsByClassView(SubjectStudentsView):
    '''2.1. Список учеников, обучающихся по данному предмету с группировкой по классам'''
    template_name = 'app/subject_students_by_class.html'

    def get_queryset(self):
        queryset = SchoolClass.objects.filter(teacher__subject__slug=self.kwargs['slug']).prefetch_related(
            'students')
        return queryset
