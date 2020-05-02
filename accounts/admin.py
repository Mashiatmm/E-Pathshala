from django.contrib import admin

from .models import Student, Teacher
# Register your models here.

myModels = [Student,Teacher]  # iterable list
admin.site.register(myModels)