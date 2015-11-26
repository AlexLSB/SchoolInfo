# -*- coding: utf-8 -*-
from django.db import models
from app.tools import TitleMixin, FullNameMixin
from django.core.urlresolvers import reverse


  # Школы
class School(TitleMixin, models.Model):

    class Meta:

        verbose_name = u'Школа'
        verbose_name_plural = u'Школы'


  # Учебные предметы.
class Subject(TitleMixin):

    class Meta:
        verbose_name = u'Предмет'
        verbose_name_plural = u'Предметы'

    def get_absolute_url(self):
        return reverse('subject_students', args=[self.slug])


  # Преподаватели. Каждый преподаватель работает по крайней мере в одной школе, возможно в нескольких. Преподаватель имеет фамилию, имя, отчество, а также предмет, который он преподает.
class Teacher(FullNameMixin, models.Model):

    class Meta:
        verbose_name = u'Преподаватель'
        verbose_name_plural = u'Преподаватели'

    school = models.ManyToManyField('School', verbose_name=u'Школа', related_name='teachers')
    subject = models.ForeignKey('Subject', verbose_name=u'Предмет', max_length=255, related_name='teachers')

    def get_absolute_url(self):
        return reverse('teacher_students', args=[self.slug])


  # Классы. Классы характеризуются школой, которой они принадлежат, номером параллели и литерой класса. Каждому классу сопоставлены несколько преподавателей.
class SchoolClass(models.Model):

    class Meta:
        verbose_name = u'Класс'
        verbose_name_plural = u'Классы'

    school = models.ForeignKey('School', verbose_name=u'Школа', related_name='classes')
    grade = models.IntegerField(verbose_name=u'Параллель', db_index=True)
    liter = models.CharField(verbose_name=u'Литера', max_length=1)
    teacher = models.ManyToManyField('Teacher', verbose_name=u'Учитель', related_name='classes')

    def __unicode__(self):
        return u'%s%s (Школа %s)' % (self.grade, self.liter, self.school)

    def get_absolute_url(self):
        return reverse('school_class_detail', args=[self.pk])


  # Ученики.
class Student(FullNameMixin, models.Model):

    class Meta:
        verbose_name = u'Ученик'
        verbose_name_plural = u'Ученики'

    school_class = models.ForeignKey('SchoolClass', verbose_name=u'Класс', related_name='students')
