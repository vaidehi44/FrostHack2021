from django.contrib import admin
from .models import Teacher, Teacher_Timetable, Assignment, Submission

admin.site.register(Teacher)
admin.site.register(Teacher_Timetable)
admin.site.register(Assignment)
admin.site.register(Submission)