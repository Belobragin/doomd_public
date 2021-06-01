"""ddgui URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
#from django.conf import settings 

from . import views

app_name='ddgui'
urlpatterns = [
    path('', views.ddgui_initial, name = 'ddgui_initial'),
    path('user/doom_event_form/new/', views.ddgui_new_doom_event_form, name='ddgui_new_doom_event_form'),
    path('user/doom_event_form/edit/', views.ddgui_edit_doom_events_form, name='ddgui_edit_doom_event_form'),
    path('user/', views.ddgui_user, name='ddgui_user'), #path('user/<int:user_id>/', views.ddgui_user, name='ddgui_user')
     
 ]
