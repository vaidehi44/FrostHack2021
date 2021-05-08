from django.contrib import admin
from .models import Link, Student_Timetable, Announcement, Admin

admin.site.register(Link)
admin.site.register(Student_Timetable)
admin.site.register(Admin)
admin.site.register(Announcement)
