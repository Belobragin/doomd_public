import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import resolve, reverse
from django.contrib.auth.models import User
from .models import Dduser, Ddevent, DoomEventDocsBucket
from .views import  ddgui_initial,\
                    ddgui_user, ddgui_new_doom_event_form,\
                    ddgui_edit_doom_events_form

from .hardcode import *


class NewPages_Tests(TestCase):
    """ tests if all pages have there views """

    def test_url_to_proper_page_view(self):
        """test:
        1. if all views exist for all pages
        2. all matching pages exist
        """        
        
        url_found = resolve(APP_PATH+'/') 
        self.assertEqual(url_found.func, ddgui_initial)
        response = self.client.get(reverse('ddgui:ddgui_initial'))
        self.assertEqual(response.status_code, 302)
       
        url_found = resolve(APP_PATH+'/user/') 
        self.assertEqual(url_found.func, ddgui_user)        
        response = self.client.get(reverse('ddgui:ddgui_user'))
        self.assertEqual(response.status_code, 302)
        
        url_found = resolve(APP_PATH+'/user/doom_event_form/edit/') 
        self.assertEqual(url_found.func, ddgui_edit_doom_events_form)
        response = self.client.get(reverse('ddgui:ddgui_edit_doom_event_form'))
        self.assertEqual(response.status_code, 302)
        
        url_found = resolve(APP_PATH+'/user/doom_event_form/new/') 
        self.assertEqual(url_found.func, ddgui_new_doom_event_form)
        response = self.client.get(reverse('ddgui:ddgui_new_doom_event_form'))
        self.assertEqual(response.status_code, 302)

