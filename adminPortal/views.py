from django.shortcuts import get_object_or_404,render, redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.decorators import login_required
from django import forms
from django.contrib.auth import authenticate, login, logout
from .models import Link, Student_Timetable, Announcement
import pandas as pd
import json
import os
from django.conf import settings
from django.utils.safestring import mark_safe

User = get_user_model()


def signup(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.refresh_from_db()
            user.save()
            return HttpResponseRedirect(reverse('adminPortal:user_login'))
            
      
    else:
        user_form = UserForm()
        return render(request,'student_portal/signup.html',{'user_form':user_form})


class homeView(ListView):
    model = Link
    template_name = 'admin_portal/base.html' 
    queryset = Link.objects.all()

    def get_context_data(self, **kwargs):
        context = super(homeView , self).get_context_data(**kwargs)
        return context
    
class TimetableV(ListView):
    model = Student_Timetable
    template_name = 'admin_portal/timetable.html' 
    queryset = Student_Timetable.objects.all()

    def get_context_data(self, **kwargs):
        context = super(TimetableView , self).get_context_data(**kwargs)
        timetable = Student_Timetable.objects.get(std=1)
        tt = excel_to_json(timetable.excel_file.url)
        context['timetable'] = tt
        return context
    

def TimetableView(request):
    tt_json_array = []
    tt = Student_Timetable.objects.all()
    for i in tt:
        url = i.excel_file.url
        tt_json_array.append(excel_to_json(url))
    tt_array = json.dumps(tt_json_array)

    if request.method == 'POST':
        tt_file = request.FILES['excel_file']
        std = request.POST['std']
        tt_model = Student_Timetable.objects.get(std=std)
        tt_model.excel_file = tt_file
        tt_model.save()

        tt_json_array = []
        tt = Timetable.objects.all()
        for i in tt:
            url = i.excel_file.url
            tt_json_array.append(excel_to_json(url))
        tt_array = json.dumps(tt_json_array)

        return render(request, 'admin_portal/timetable.html', {'tt_array':tt_array})

    else:
        return render(request, 'admin_portal/timetable.html', {'tt_array':tt_array})



class UpdateLinkView(UpdateView):
    model = Link
    template_name="admin_portal/update.html"
    fields = ("link_url",)
    success_url = reverse_lazy("adminPortal:home")


class UpdateTTView(UpdateView):
    model = Student_Timetable
    template_name="admin_portal/upload_tt.html"
    fields = ("excel_file",)
    success_url = reverse_lazy("adminPortal:timetable")



def NoticeboardView(request):
    notices = Announcement.objects.filter(is_open=True)
    if request.method == 'POST' and 'new_notice' in request.POST:
        user = request.user
        mssg = request.POST['mssg']
        model = Announcement(user=user, mssg=mssg)
        model.save()

        return render(request, 'admin_portal/notice.html',{'notices':notices})
    
    if request.method == 'POST' and 'close_notice' in request.POST:
        notice_id = request.POST['notice_id']
        notice = Announcement.objects.get(id=notice_id)
        notice.is_open = False
        notice.save()

        return render(request, 'admin_portal/notice.html',{'notices':notices})

    else:
        
        return render(request, 'admin_portal/notice.html',{'notices':notices})




def user_login(request):
    if request.method == 'POST':
          username = request.POST['username']
          password = request.POST['password']
          user = authenticate(username=username, password=password)
          if user is not None and user.is_admin == True:
              if user.is_active:
                  login(request, user)
                  # Redirect to index page.
                  return HttpResponseRedirect(reverse("adminPortal:home"))
              else:
                  # Return a 'disabled account' error message
                  return HttpResponse("You're account is disabled.")
          else:
              # Return an 'invalid login' error message.
              return HttpResponse("invalid login details ")
    else:
        # the login is a  GET request, so just show the user the login form.
        return render(request,'admin_portal/registration/login.html')

    
 
def excel_to_json(url):
    url_ = "F:/FrostHack/Project"+url
    file_ = pd.read_excel(url_)
    df = pd.DataFrame(file_)
    result = df.to_json(orient="columns")
    parsed = json.loads(result)
    table_json = mark_safe(json.dumps(parsed))
    return table_json

