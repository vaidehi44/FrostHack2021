from django.db import models
from django.contrib.auth.forms import UserCreationForm#for signup form
from django.contrib.auth.forms import AuthenticationForm#for login form
from django.contrib.auth.models import User
from django import forms
from django.forms.widgets import PasswordInput, TextInput



class CustomAuthForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class':'validate','placeholder': 'Username','autocomplete':'off'}))
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder':'Password'}))


class UserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'password1','password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder':('Username')})
        self.fields['password1'].widget.attrs.update({'placeholder':('Password')})        
        self.fields['password2'].widget.attrs.update({'placeholder':('Re-enter password')})
