import datetime, os

from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

#from django.test import TestCase
from ddws.functests.basefunctest import BaseTest

from ddws.functests.hardcode import *
from dscv.models import DscvLp
from ddws.dscv.hardcode import *
from ddws.dscv.forms import DscvLpInputForm
from ddws.hardcode import *

BASE_DIR = os.getcwd()

class DscvTests(BaseTest):
    """ tests dscv app"""

    upload_file = open(TESTFILE, 'rb')
    form_data = {'algorythm': OTHER_ALGORYTM,
                 'dscv_lp_hint' : 'E100',
                  'dscv_lp_country' : 'Russia',}
    form_file = {'lpfile': SimpleUploadedFile(upload_file.name, upload_file.read())}
    

    def register_user(self):
        self.selenium.get('%s%s' % (self.live_server_url, LOGIN_PAGE_ADRESS))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys(test_user['id_username'])
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys(test_user['id_password1'])
        self.selenium.find_element_by_tag_name('button').click()
    

    def input_data_to_lp_form(self, algorythm):
        """
        fill lp recognition form
        """
        self.selenium.get('%s%s' % (self.live_server_url, DSCV_ADRESS + DSCV_FORM_PAGE_ADRESS))
        lp_hint_input = self.selenium.find_element_by_id("id_dscv_lp_hint")
        lp_hint_input.send_keys('E100')
        lp_country_input = self.selenium.find_element_by_id("id_dscv_lp_country")
        lp_country_input.send_keys('Russia')
        algorythm_input = self.selenium.find_element_by_id("id_algorythm")
        algorythm_input.send_keys(algorythm)
        lp_image_input = self.selenium.find_element_by_id("id_lpfile")
        lp_image_input.send_keys(os.path.join(os.getcwd(),TESTFILE))
        self.selenium.find_element_by_id('lp_form_submit').click()


    def test_lp_input(self):
        print('\nTest lp input view and form data correctness: ...\\dscv\\reclp\\')
        self.register_user()
        upload_file = open(TESTFILE, 'rb')
        #test form:            
        self.selenium.get('%s%s' % (self.live_server_url, DSCV_ADRESS + DSCV_FORM_PAGE_ADRESS))        
        form = DscvLpInputForm(data = self.form_data, files = self.form_file)
        self.assertTrue(form.is_valid())
        
    def test_lp_form_page_and_rec_page(self):
        #test get: 
        self.register_user()       
        self.selenium.get('%s%s' % (self.live_server_url, DSCV_ADRESS + DSCV_FORM_PAGE_ADRESS)) #self.client.get(reverse('dscv:dscv_reclp'))
        page_title = self.selenium.find_element_by_id('page_title').text
        self.assertIn(DSCV_RECOGNITION_FORM_TITLE, page_title)        
        #test recognition functionality and correct redirect:
        if is_port_in_use():
            #other algo:
            self.input_data_to_lp_form(OTHER_ALGORYTM)
            self.assertEqual(self.selenium.find_element_by_id('page_title').text, DSCV_LPRES_PAGE_TITLE)
            tabl = self.selenium.find_element_by_id('result').text
            self.assertIn('ML recognition result User recognition result Country', tabl)
            self.assertIn('Test option', tabl)
            self.assertIn(self.form_data['dscv_lp_hint'], tabl)
            self.assertIn(self.form_data['dscv_lp_country'], tabl)
            #tessimple algo:
            self.input_data_to_lp_form(TESSERACT_SIMPLE_ALGORYTHM)
            self.assertEqual(self.selenium.find_element_by_id('page_title').text, DSCV_LPRES_PAGE_TITLE)
            tabl = self.selenium.find_element_by_id('result').text
            self.assertIn('ML recognition result User recognition result Country', tabl)
            self.assertNotIn('Test option', tabl)
            self.assertIn('11XK', tabl)
            self.assertIn(self.form_data['dscv_lp_hint'], tabl)
            self.assertIn(self.form_data['dscv_lp_country'], tabl)
        else:
            self.input_data_to_lp_form('other')
            self.assertEqual(self.selenium.find_element_by_id('page_title').text, ERROR_PAGE_TITLE)
            self.input_data_to_lp_form('tessimple')
            self.assertEqual(self.selenium.find_element_by_id('page_title').text, ERROR_PAGE_TITLE)
            self.assertIn(ERR_ML_SERVICE_SWITCHED_OFF, self.selenium.find_element_by_id('err_ess').text)





        
