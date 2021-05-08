from django.urls import path, include
from . import views
from studentPortal.forms import CustomAuthForm
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import AuthenticationForm

app_name = 'adminPortal'

urlpatterns = [

    path('login', views.user_login, name='user_login'),
    path('home/', include('django.contrib.auth.urls'),name="logout"),
    path('home',views.homeView.as_view(), name='home'),
    path('class_links/<int:pk>/upload', views.UpdateLinkView.as_view(), name='upload_link' ),
    #path('timetable/<int:pk>/upload', views.UpdateTimetableView.as_view(), name='tt_upload_link' ),
    path('timetable',views.TimetableView, name='timetable'),
    path('timetable/<int:pk>/upload',views.UpdateTTView.as_view(), name='update_tt'),
    path('announcements',views.NoticeboardView, name='notice'),


] 