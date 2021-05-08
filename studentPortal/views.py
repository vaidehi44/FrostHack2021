from django.shortcuts import get_object_or_404,render, redirect
from django.http import HttpResponse,HttpResponseRedirect
from .forms import  UserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.decorators import login_required
from django import forms
from django.contrib.auth.decorators import login_required
from adminPortal.models import Link, Student_Timetable, Announcement
from teacherPortal.models import Assignment
from .models import Student
import os, json
import pandas as pd
from django.utils.safestring import mark_safe
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()
       

def signup(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.refresh_from_db()
            user.save()
            return HttpResponseRedirect(reverse('studentPortal:user_login'))
            
      
    else:
        user_form = UserForm()
        return render(request,'student_portal/signup.html',{'user_form':user_form})



def user_login(request):
    if request.method == 'POST':
          username = request.POST['username']
          password = request.POST['password']
          user = authenticate(username=username, password=password)
          if user is not None and user.is_student == True:
              if user.is_active:
                  login(request, user)
                  # Redirect to index page.
                  return HttpResponseRedirect(reverse("studentPortal:home", kwargs={"pk":request.user.id}))
              else:
                  # Return a 'disabled account' error message
                  return HttpResponse("You're account is disabled.")
          else:
              # Return an 'invalid login' error message.
              return HttpResponse("invalid login details ")
    else:
        # the login is a  GET request, so just show the user the login form.
        return render(request,'student_portal/registration/login.html')



class StudentHomeView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'student_portal/home.html'
    fields = '__all__'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
        
    def get_context_data(self, **kwargs):
            context = super(StudentHomeView , self).get_context_data(**kwargs)
            current_student = Student.objects.get(user=self.request.user)
            context['curr_student'] = current_student
            context['link'] = Link.objects.get(std=current_student.std)
            tt = Student_Timetable.objects.get(std=current_student.std)
            tt_json = excel_to_json(tt.excel_file.url)
            context['timetable'] = tt_json
            return context


class AssignmentView(LoginRequiredMixin, ListView):
    model = Assignment
    template_name = 'student_portal/assg.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
            context = super(AssignmentView , self).get_context_data(**kwargs)
            current_student = Student.objects.get(user=self.request.user)
            context['curr_student'] = current_student
            user = self.request.user
            assgs = Assignment.objects.filter(std = user.student.std,is_open=True)
            context['assgs'] = assgs
            return context




def CollectSubmission(request):
    if request.method=='POST':
        user = request.user
        student = Students.objects.get(user=user)
        answer = request.FILES['answer']
        assg_id = request.POST['assg_id']
        assg = Assignment.objects.get(id=assg_id)
        submission_model = Assignment(student=student, answersheet=answer, assignment=assg)
        submission_model.save()

class NoticeboardView(LoginRequiredMixin, ListView):
    model = Announcement
    template_name = 'student_portal/notice.html' 
    queryset = Announcement.objects.all()

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
            context = super(NoticeboardView , self).get_context_data(**kwargs)
            current_student = Student.objects.get(user=self.request.user)
            context['curr_student'] = current_student
            return context

        
def excel_to_json(url):
    url_ = "F:/FrostHack/Project"+url
    file_ = pd.read_excel(url_)
    df = pd.DataFrame(file_)
    result = df.to_json(orient="columns")
    parsed = json.loads(result)
    table_json = mark_safe(json.dumps(parsed))
    return table_json

