from django.contrib import admin
from .models import Semester, Subject

@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'prev_semester', 'next_semester')

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'semester', 'prev_subject', 'next_subject')
    filter_horizontal = ('prerequisites',)
