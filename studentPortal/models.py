from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Student(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, null=True, related_name='student')
    std = models.IntegerField()
    roll_no = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.user}-{self.std}-{self.roll_no}"

