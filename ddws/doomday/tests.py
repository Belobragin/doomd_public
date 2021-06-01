import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from ddgui.models import Dduser, Ddevent, DoomEventDocsBucket

from functests.hardcode import *
from ddws.hardcode import *

class InitialTests(TestCase):
    """ tests all BASE properties"""

    # def setUp(self):
    #     self.credentials = {
    #         'username': no_kill_test_user['id_username'],
    #         'password': no_kill_test_user['id_password1'],}
    #     User.objects.create_user(**self.credentials)

    def test_allPagesExist(self):
        """
        tests if all BASE pages are alive
        Note: there are no unnamed pages
        """
        print('\nTest urls in doomday')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        
        response = self.client.get(reverse('password_change'))
        self.assertEqual(response.status_code, 302)
        
        response = self.client.get(reverse('password_change_done'))
        self.assertEqual(response.status_code, 302)
        
        response = self.client.get(reverse('password_reset'))
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get(reverse('password_reset_done'))
        self.assertEqual(response.status_code, 200)
        #response = self.client.get(reverse('password_reset_confirm'))
        #self.assertEqual(response.status_code, 200)
        
        response = self.client.get(reverse('password_reset_complete'))
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        #response = self.client.get(reverse('edit_user'))
        #self.assertEqual(response.status_code, 200)
        #response = self.client.get(reverse('social_django'))
        #self.assertEqual(response.status_code, 200)
        

class LoginRegisterUser_Tests(TestCase):
    """ creates a user and tests proper authentication"""

    def setUp(self):
        self.credentials = {
            'username': no_kill_test_user['id_username'],
            'password': no_kill_test_user['id_password1'],}
        User.objects.create_user(**self.credentials)
    
    def test_login(self):
        print('\nTest user login - doomday - TestCase')
        # send login data
        response = self.client.post('/login/', self.credentials, follow=True)
        # should be logged in now
        self.assertTrue(response.context['user'].is_active)
        self.assertTrue(self.client.login(username=self.credentials['username'], 
                                          password=self.credentials['password']))
        #should not be logged in - incorrect password:
        self.assertFalse(self.client.login(username=self.credentials['username'], 
                                          password="mypassword" ))
