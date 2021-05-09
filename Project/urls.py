
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('Student_Portal/', include('studentPortal.urls')),
    path('Admin_Portal/', include('adminPortal.urls')),
    path('Teacher_Portal/', include('teacherPortal.urls')),
    path('portals/', views.main, name='portals'),

    
]+ static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

