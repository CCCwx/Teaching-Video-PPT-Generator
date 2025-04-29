"""
URL configuration for fy_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from myapp import views


    
urlpatterns = [
    path('', views.home, name='home'),  
    path('admin/', admin.site.urls),
    path('process_presentation/', views.process_presentation, name='process_presentation'),
    path('presentation-editor/', views.presentation_editor, name='presentation_editor'),
    path('get_slides_data/', views.get_slides_data, name='get_slides_data'),
    path('get_script_text/', views.get_script_text, name='get_script_text'),
    path('save_script/', views.save_script, name='save_script'),
    path('generate_video/', views.generate_video, name='generate_video'),
    path('generate_ppt/', views.generate_ppt, name='generate_ppt'),
    path('save_voice/', views.save_voice, name='save_voice'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
