"""
Tests fot login view
"""

import time, datetime

from ddws.functests.basefunctest import BaseTest
from functests.hardcode import *
from ddws.hardcode import *


class LoginFunctionalTests(BaseTest):
    """
    tests login page properties:
    """
          
    def test_successful_login(self):
        """ tests login with correct username/password"""

        print('\nSuccessful login test')
        self.selenium.get('%s%s' % (self.live_server_url, LOGIN_PAGE_ADRESS))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys(test_user['id_username'])
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys(test_user['id_password1'])
        self.selenium.find_element_by_tag_name('button').click()        
        self.assertTrue(assert_decorator(self.selenium.find_element_by_id, 'user_greetings'))
        self.selenium.get('%s%s' % (self.live_server_url, '/ddgui/user/'))
        self.assertTrue(assert_decorator(self.selenium.find_element_by_id, 'user_page_header'))

    def test_unsuccess_login(self):
        """ tests login with INcorrect username/password"""
    
        print('\nMalicious login test')
        self.selenium.get('%s%s' % (self.live_server_url, '/login/'))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys(no_kill_test_user['id_first_name'])
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys(no_kill_test_user['id_password1'])
        self.selenium.find_element_by_tag_name('button').click()        
        self.assertFalse(assert_decorator(self.selenium.find_element_by_id, 'user_greetings'))
        self.selenium.get('%s%s' % (self.live_server_url, '/ddgui/user/'))
        try:
             inputbox = self.selenium.find_element_by_id("user_page_header").text[14:-1]
        except Exception as ee:
             self.assertTrue(ee is not None)   
        self.assertFalse(assert_decorator(self.selenium.find_element_by_id, 'user_page_header'))
 
