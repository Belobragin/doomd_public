"""
Tests for registration new user view
"""

import time, datetime

from selenium import webdriver
#from selenium.webdriver.common.keys import Keys

from django.test import LiveServerTestCase

from functests.hardcode import *
from ddws.hardcode import *
from ddgui.models import Dduser

class RegistrationFunctionalTests(LiveServerTestCase):
    """
    tests registration new user page properties:
    """
        
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium =  webdriver.Chrome(PATH_TO_CHROME_DRIVER)
        cls.selenium.implicitly_wait(3)

    @classmethod
    def tearDownClass(cls):
        #cls.selenium.quit()
        cls.selenium.close()
        super().tearDownClass()


    def test_successful_registration(self):
        """ tests login with correct username/password"""
        
        print('\nRegister new user test')        
        create_test_user(tuser = no_kill_test_user)
        old_all_user_id = list(User.objects.values('id')) #
        old_user_id = old_all_user_id[0]
        old_all_dduser_id = list(Dduser.objects.values('dduser_id'))
        old_dduser_id = old_all_dduser_id[0]
        self.selenium.get('%s%s' % (self.live_server_url, REGISTER_PAGE_ADRESS))
        for k, v in test_user.items():
            inputbox = self.selenium.find_element_by_id(k)
            inputbox.send_keys(v)
            #print(k, v)
        signupbutton = self.selenium.find_element_by_id('submit_button').click()
        new_all_user_id = list(User.objects.values('id')) 
        new_all_dduser_id = list(Dduser.objects.values('dduser_id'))
        self.assertTrue(len(old_all_user_id)+1 == len(new_all_user_id))
        self.assertTrue(old_user_id != new_all_user_id[-1])        
        self.assertTrue(len(old_all_dduser_id)+1 == len(new_all_dduser_id))
        self.assertTrue(old_dduser_id != new_all_dduser_id[-1])
    
