from django.contrib import admin
from main.models import VTUResult, Student, Semester, SGPA, Subject, Result
# Register your models here.

@admin.register(VTUResult)
class VTUResultAdmin(admin.ModelAdmin):
    list_display = ['code']

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['usn', 'name']
    search_fields = ('usn', 'name')

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ['student', 'semester', 'subject', 'internal', 'external', 'total', 'result']

@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ['semester']

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'sem', 'credits']
    search_fields = ('code', 'name')


@admin.register(SGPA)
class SGPAAdmin(admin.ModelAdmin):
    list_display = ["student", "semester", "result", "sgpa"]