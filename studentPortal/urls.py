from django.urls import path, include
from . import views
from . forms import CustomAuthForm
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import AuthenticationForm

app_name = 'studentPortal'

urlpatterns = [

    path('login', views.user_login, name='user_login'),
    path('<int:pk>/home',views.StudentHomeView.as_view() , name='home'),
    path('home/', include('django.contrib.auth.urls'),name="logout"),
    path('noticeboard', views.NoticeboardView.as_view(),name="notice"),
    path('assignments', views.AssignmentView.as_view(),name="assg"),
    path('assignments/submission', views.CollectSubmission,name="sub"),

] 