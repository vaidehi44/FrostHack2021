from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404,render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from .models import Assignment, Teacher_Timetable, Teacher
from .forms import AssignmentForm
from adminPortal.models import Link, Announcement
import pandas as pd
import json
from django.utils.safestring import mark_safe
from django.contrib.auth import get_user_model

User = get_user_model()

def user_login(request):
    if request.method == 'POST':
          username = request.POST['username']
          password = request.POST['password']
          user = authenticate(username=username, password=password)
          if user is not None and user.is_teacher == True:
              if user.is_active:
                  login(request, user)
                  # Redirect to index page.
                  return HttpResponseRedirect(reverse("teacherPortal:home", kwargs={"pk":request.user.id}))
              else:
                  # Return a 'disabled account' error message
                  return HttpResponse("You're account is disabled.")
          else:
              # Return an 'invalid login' error message.
              return HttpResponse("invalid login details ")
    else:
        # the login is a  GET request, so just show the user the login form.
        return render(request,'teacher_portal/registration/login.html')


class TeacherHomeView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'teacher_portal/home.html'
    fields = '__all__'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
        
    def get_context_data(self, **kwargs):
            context = super(TeacherHomeView , self).get_context_data(**kwargs)
            current_teacher = Teacher.objects.get(user=self.request.user)
            context['curr_teacher'] = current_teacher
            tt = Teacher_Timetable.objects.get(teacher=current_teacher)
            tt_json = excel_to_json(tt.excel_file.url)
            context['timetable'] = tt_json
            return context


class LinksView(LoginRequiredMixin,ListView):
    model = Link
    template_name = 'teacher_portal/links.html'
    queryset = Link.objects.all()

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
            context = super(ListView , self).get_context_data(**kwargs)
            current_teacher = Teacher.objects.get(user=self.request.user)
            context['curr_teacher'] = current_teacher
            return context



def AssignmentView(request):
    current_teacher = Teacher.objects.get(user=request.user)
    my_assgs = Assignment.objects.filter(teacher = current_teacher, is_open=True)
    assg_create_form = AssignmentForm()

    if request.method == 'POST' and 'new_assg' in request.POST:
        user = request.user
        teacher = user.teacher
        std = request.POST['std']
        sub = request.POST['subject']
        mssg = request.POST['mssg']
        deadline = request.POST['deadline']
        model = Assignment(teacher=teacher, std=std, subject=sub, mssg = mssg, deadline=deadline)
        model.save()

        return render(request, 'teacher_portal/assg.html',{'form':assg_create_form,'assgs':my_assgs,'curr_teacher':current_teacher})
    
    if request.method == 'POST' and 'close_assg' in request.POST:
        assg_id = request.POST['assg_id']
        assg = Assignment.objects.get(id=assg_id)
        assg.is_open = False
        assg.save()

        return render(request, 'teacher_portal/assg.html',{'form':assg_create_form,'assgs':my_assgs,'curr_teacher':current_teacher})

    else:
        
        return render(request, 'teacher_portal/assg.html',{'form':assg_create_form,'assgs':my_assgs,'curr_teacher':current_teacher})



class NoticeboardView(LoginRequiredMixin, ListView):
    model = Announcement
    template_name = 'teacher_portal/notice.html' 
    queryset = Announcement.objects.filter(is_open=True)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
            context = super(NoticeboardView , self).get_context_data(**kwargs)
            current_teacher = Teacher.objects.get(user=self.request.user)
            context['curr_teacher'] = current_teacher
            return context



def excel_to_json(url):
    url_ = "F:/FrostHack/Project"+url
    file_ = pd.read_excel(url_)
    df = pd.DataFrame(file_)
    result = df.to_json(orient="columns")
    parsed = json.loads(result)
    table_json = mark_safe(json.dumps(parsed))
    return table_json

