# -*- coding: utf-8 -*-
from django.db import models
from django.template.defaultfilters import slugify
from unidecode import unidecode
import itertools


class AppLabel(str):
    """
    Читаемое имя для приложения в админке
    class Meta:
        app_label = utils.AppLabel('shared', u'Общие элементы сайта')
    """
    def __new__(cls, value, title):
        instance = str.__new__(cls, value)
        instance._title = title
        return instance

    def title(self):
        return self._title

    __copy__ = lambda self: self
    __deepcopy__ = lambda self, memodict: self


class FullNameMixin(models.Model):
    """
    Миксин для добавления ФИО и ярлыка по ФИО
    """
    class Meta:
        abstract = True

    full_name = models.CharField(verbose_name=u'ФИО', max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def save(self, *args, **kwargs):
        self.slug = orig = slugify(unidecode(self.full_name))
        for x in itertools.count(1):
            if not self.__class__.objects.filter(slug=self.slug).exists():
                break
            self.slug = '%s-%d' % (orig, x)
        return super(FullNameMixin, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.full_name


class TitleMixin(models.Model):
    """
    Миксин для добавления данных текстового заголовка и ярлыка по этому
    заголовку
    """
    class Meta:
        abstract = True
    title = models.CharField(verbose_name=u"Название", max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def save(self, *args, **kwargs):
        self.slug = orig = slugify(unidecode(self.title))
        for x in itertools.count(1):
            if not self.__class__.objects.filter(slug=self.slug).exists():
                break
            self.slug = '%s-%d' % (orig, x)
        return super(TitleMixin, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title
