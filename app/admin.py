from django.contrib import admin
from . import models


admin.site.register(models.School)
admin.site.register(models.Subject)
admin.site.register(models.Teacher)
admin.site.register(models.SchoolClass)
admin.site.register(models.Student)
