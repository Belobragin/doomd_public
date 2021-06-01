"""dscv URL Configuration"""

from django.conf import settings 
from django.urls import path
from django.conf.urls.static import static

from dnews.views import *
from dnews.hardcode import *
from dnews.apps import DnewsConfig

app_name=DnewsConfig.name


urlpatterns = [
    path('', DnewsInitialView.as_view(), name = 'dnews_list'),
    path('<int:pk>/', DnewsDetailsView.as_view(), name = 'dnews_info'),
         
 ] #+static(settings.MEDIA_URL, document_root=PATH_TO_FILEFOLDER)


