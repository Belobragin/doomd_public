import datetime, os

from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from django.test import TestCase
#from ddws.functests.basefunctest import BaseTest

from functests.hardcode import *
from dscv.models import DscvLp
from dscv.hardcode import *
from dscv.forms import DscvLpInputForm
#from ddws.hardcode import *


class DscvTestPages_Tests(TestCase):
    
    def setUp(self):
        self.credentials = {
            'username': no_kill_test_user['id_username'],
            'password': no_kill_test_user['id_password1'],}
        User.objects.create_user(**self.credentials)

    def test_dscv_pages_no_login(self):
        """tests /dscv for non-logged user"""
        
        print('\nTest urls in dscv app: ...\\dscv\\ - non-logged user')        
        response = self.client.get(reverse('dscv:dscv_initial'))
        self.assertEqual(response.status_code, 302)
        print('\nTest urls in dscv app: ...\\dscv\\reclp\\  - non-logged user')
        response = self.client.get(reverse('dscv:dscv_reclp'))
        self.assertEqual(response.status_code, 302)

    def test_dscv_pages_exist_logged(self):
        """tests /dscv for logged user"""
        
        print('\nTest urls in dscv app: ...\\dscv\\ - logged user')
        self.client.post('/login/', self.credentials, follow=True)
        response = self.client.get(reverse('dscv:dscv_initial'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Hello '+ self.credentials['username'], response.content.decode())
        print('\nTest urls in dscv app: ...\\dscv\\reclp\\  - logged user')
        response = self.client.get(reverse('dscv:dscv_reclp'))
        self.assertEqual(response.status_code, 200)

class DscvTestForm_Tests(TestCase):
    """ tests dscv app"""

    def setUp(self):
        self.credentials = {
            'username': no_kill_test_user['id_username'],
            'password': no_kill_test_user['id_password1'],}
        User.objects.create_user(**self.credentials)    

    def test_lp_input(self):
        print('\nTest lp input view and form data correctness: ...\\dscv\\reclp\\')
        self.client.post('/login/', self.credentials, follow=True) 
        upload_file = open(TESTFILE, 'rb')
        #test form:
        form_data = {'algorythm': OTHER_ALGORYTM,
                     'dscv_lp_hint' : 'E100',
                     'dscv_lp_country' : 'Russia',}
        form_file = {'lpfile': SimpleUploadedFile(upload_file.name, upload_file.read())}
        form = DscvLpInputForm(data = form_data, files = form_file)
        print(form.errors)
        self.assertTrue(form.is_valid())
        #test get:
        response = self.client.get(reverse('dscv:dscv_reclp'))
        self.assertEqual(200, response.status_code)
        #print(response.content.decode())
        self.assertIn(DSCV_RECOGNITION_FORM_TITLE, response.content.decode())
        
        #test post:
        form_data.update(form_file)
        response = self.client.post(reverse('dscv:dscv_reclp'), form_data,)
        self.assertEqual(302, response.status_code)

        
