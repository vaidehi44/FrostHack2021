from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Link(models.Model):
    link_url = models.CharField(max_length = 1000, blank=True)
    std = models.IntegerField(unique=True)

    def __str__(self):
        return f"{self.link_url}-{self.std}"

    class Meta:
       ordering = ['std']


class Student_Timetable(models.Model):
    excel_file = models.FileField(null=True, upload_to='timetable/students', default="timetable/blank.xlsx",blank=True)
    std = models.IntegerField(unique=True)

    def __str__(self):
        return f"{self.std}-{self.excel_file}"

    class Meta:
       ordering = ['std']


class Announcement(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, null=True)
    mssg = models.TextField(null = True)
    date = models.DateTimeField(auto_now_add=True)
    is_open = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user}-{self.mssg}"


class Admin(models.Model):
    name = models.OneToOneField(User, on_delete = models.CASCADE, null=True)

    def __str__(self):
        return f"{self.name}"

