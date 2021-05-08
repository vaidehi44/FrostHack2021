from django.db import models
from django.db import models
from django.contrib.auth import get_user_model
from studentPortal.models import Student


User = get_user_model()


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, null=True,related_name='teacher')
    age = models.IntegerField()

    def __str__(self):
        return f"{self.user}"



SUB_CHOICES = (
    ('Math', 'Math'),
    ('Science', 'Science'),
    ('History', 'History'),
    ('Geography', 'Geography'),
    ('Economics', 'Economics'),
    ('English', 'English'),
    ('Hindi', 'Hindi'),
    ('EVS', 'EVS'),
    ('GK', 'GK'),
    ('Art and Craft', 'Art and Craft'),
)

class Assignment(models.Model):
    teacher = models.ForeignKey(Teacher, null = True, related_name = 'assignment',on_delete = models.PROTECT)
    std = models.IntegerField()
    subject = models.CharField(max_length=30, choices=SUB_CHOICES)
    mssg = models.CharField(max_length=500)
    date = models.DateField(auto_now_add=True)
    deadline = models.DateField()
    is_open = models.BooleanField(default=True)

    class Meta:
       ordering = ['-date']

    def __str__(self):
        return f"{self.teacher}-{self.std}-{self.subject}"


class Submission(models.Model):
    student = models.ForeignKey(Student, null=True, on_delete = models.CASCADE, related_name='submission')
    answersheet = models.FileField(null=True, upload_to='submissions')
    assignment = models.ForeignKey(Assignment, null=True, related_name='submission',on_delete = models.PROTECT)

    def __str__(self):
            return f"{self.student}-{self.answersheet}"


class Teacher_Timetable(models.Model):
    teacher = models.OneToOneField(Teacher, null = True, related_name = 'timetable', on_delete = models.CASCADE)
    excel_file = models.FileField(null=True, upload_to='timetable/teachers', default="timetable/blank.xlsx",blank=True)

    def __str__(self):
        return f"{self.teacher}-{self.excel_file}"

