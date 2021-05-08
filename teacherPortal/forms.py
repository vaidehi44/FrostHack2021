from django import forms
from django.forms import ModelForm

from .models import Assignment


class DateInput(forms.DateInput):
    input_type = 'date'


class AssignmentForm(ModelForm):

    class Meta:
        model = Assignment
        fields = ['std','subject','mssg', 'deadline']
        widgets = {
            'deadline': DateInput(),
        }