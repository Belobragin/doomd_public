"""imnet URL Configuration"""


from django.urls import path
from django.conf import settings 
from django.conf.urls.static import static

from imnet.views import *
from imnet.hardcode import *
from imnet.apps import ImnetConfig

app_name=ImnetConfig.name 

urlpatterns = [
    path('', ImageInitialView.as_view(), name = 'imnet_initial'),
    path('imrec/', ImageRecView.as_view(), name='imrec'), #enter image and algorythm here
    path('imrecres/', ImageRecResultView.as_view(), name = 'imrecres'), #enjoy recognition result
    path('imatt/', ImageAttView.as_view(), name='imatt'), #enter image and attack algo
    path('imattres/', ImageAttResultView.as_view(), name='imattres'), #enjoy attack results
    path('spoofatt/', SpoofAttResultView.as_view(), name='spoofatt'),
    #path('redirect/<str:redirect_page>', ImnetRedirectView.as_view(), name= 'imnet_redirect'), # simple redirect
    # path('user/doom_event_form/edit/', views.ddgui_edit_doom_events_form, name='ddgui_edit_doom_event_form'),
    # path('user/', views.ddgui_user, name='ddgui_user'), #path('user/<int:user_id>/', views.ddgui_user, name='ddgui_user')
     
 ] #+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


