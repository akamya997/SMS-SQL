from django.contrib import admin

from . import models

admin.site.register(models.Department)
admin.site.register(models.Teacher)
admin.site.register(models.Student)
admin.site.register(models.Course)
admin.site.register(models.OpenCourse)
admin.site.register(models.Event)
# Register your models here.
