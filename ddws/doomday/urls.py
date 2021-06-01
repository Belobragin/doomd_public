"""doomday URL Configuration

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
import os
from django.contrib import admin
from django.urls import include, path
from django.conf import settings 
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView,\
                                      PasswordChangeView, PasswordChangeDoneView,\
                                      PasswordResetView, PasswordResetDoneView,\
                                      PasswordResetConfirmView, PasswordResetCompleteView

from doomday import views
from doomday.views import *

urlpatterns = [    
                path('admin/', admin.site.urls),
                #no login required
                path('', DashboardView.as_view(), name='dashboard'),
                path('about/', AboutView.as_view(), name='about'),
                path('register/', RegisterView.as_view(), name = 'register'),
                #authentication urls:
                path('login/', LoginView.as_view(template_name='doomday/login.html'), name='login'),
                path('logout/', LogoutView.as_view(), name='logout'),                
                path('update/', views.edit_user, name = 'edit_user'), #'update/<int:upk>/'   
                #for password change:
                path('password_change/', PasswordChangeView.as_view(template_name='doomday/password_change.html'), name='password_change'),
                path('password_change/done/', PasswordChangeDoneView.as_view(template_name='doomday/password_change_done.html'), name='password_change_done'),                
                #for password reset - reset form submit and redirect:
                path('password_reset/', MyPasswordResetView.as_view(template_name='doomday/password_reset.html'), name='password_reset'),
                path('password_reset/done/', PasswordResetDoneView.as_view(template_name='doomday/password_reset_done.html'), name='password_reset_done'),                
                #for password reset - new passw (token) submit and redirect:
                path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='doomday/password_reset_confirm.html'), name='password_reset_confirm'),
                path('reset/done/', PasswordResetCompleteView.as_view(template_name='doomday/password_reset_complete.html'), name='password_reset_complete'),    
                #Github oath - turn off social auth since 12.04.2021::
                #path("oauth/", include("social_django.urls"), name = "social_django"),                
                #ddgui app (login required):                
                #TODO: that's probably exclude after messages intro:
                path('ddredirect/', DdredirectView.as_view(), name='ddredirect'),
                path('redirecterr/<str:application_page>/<str:redirect_page>', ErrorRedirectView.as_view(), name = 'err_redirect'),
                
                #APPLICATIONS:
                path('news/', include('dnews.urls'), name = 'dnews'),
                path('ddgui/', include('ddgui.urls'), name='ddgui'), 
                path('dscv/', include('dscv.urls'), name='dscv'),
                path('imnet/', include('imnet.urls'), name='imnet'),
                path('bot/', include('bot.urls'), name = 'bot'),

                path('test/', TestView.as_view(), name='test'),
                
                
                #Examples:
                #url(r'^archive/(\d{4})/$', archive, name="archive"),
                #url(r'^archive-summary/(\d{4})/$', archive, name="archive-summary"),
                ] #+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

