"""unittest forr bot app"""


import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import resolve, reverse
from django.contrib.auth.models import User

from ddws.bot.hardcode import *
from ddws.bot.views import *

class BotPages_Tests(TestCase):
    """ tests if all pages have there views """


    def test_url_to_proper_page_view(self):
        """test:
        1. if all views exist for all pages
        2. all matching pages exist
        """        
        
        response = self.client.get(reverse('bot:main'))
        self.assertEqual(response.status_code, 200)
       
        # url_found = resolve(APP_PATH+'/user/') 
        # self.assertEqual(url_found.func, ddgui_user)        
        # response = self.client.get(reverse('ddgui:ddgui_user'))
        # self.assertEqual(response.status_code, 302)
        


