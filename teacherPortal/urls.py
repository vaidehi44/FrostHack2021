from django.urls import path, include
from . import views


app_name = 'teacherPortal'

urlpatterns = [

    path('login', views.user_login, name='user_login'),
    path('<int:pk>/home',views.TeacherHomeView.as_view() , name='home'),
    path('home/', include('django.contrib.auth.urls'),name="logout"),
    path('noticeboard', views.NoticeboardView.as_view(),name="notice"),
    path('class_links', views.LinksView.as_view(),name="links"),
    path('assignments', views.AssignmentView,name="assg"),
] 