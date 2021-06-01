"""dscv URL Configuration"""

from django.conf import settings 
from django.urls import path
from django.conf.urls.static import static

from dscv.views import *
from dscv.hardcode import *
from dscv.apps import DscvConfig

app_name=DscvConfig.name


urlpatterns = [
    path('', DscvInitialView.as_view(), name = 'dscv_initial'),
    path('reclp/', DscvReclpView.as_view(), name='dscv_reclp'),
    path('reclpres/', DscvReclpResView.as_view(), name = 'dscv_reclpres'),
     
 ] +static(settings.MEDIA_URL, document_root=PATH_TO_FILEFOLDER)


