"""
Tests for new user update view
"""

from .basefunctest import BaseTest
from functests.hardcode import *
from ddws.hardcode import *
from ddgui.models import Dduser


class RegistrationFunctionalTests(BaseTest):
    """
    tests registration new user page properties:
    """
    
    def test_find_update_page(self):
        """ tests update page exists"""
        
        print("\nTry to find update page")
        self.selenium.get('%s%s' % (self.live_server_url, LOGIN_PAGE_ADRESS))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys(test_user['id_username'])
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys(test_user['id_password1'])
        self.selenium.find_element_by_tag_name('button').click()
        cookie = self.selenium.get_cookie(name = 'sessionid')
        self.selenium.get('%s%s' % (self.live_server_url, UPDATE_PAGE_ADRESS))
        self.assertTrue(assert_decorator(self.selenium.find_element_by_id, 'update_login'))

        print("\nUpdate page test - test field change")
        self.selenium.get('%s%s' % (self.live_server_url, UPDATE_PAGE_ADRESS))
        inputbox = self.selenium.find_element_by_id("id_last_name")
        id_last_name = inputbox.get_attribute("value")
        self.assertTrue(id_last_name == test_user['id_last_name'])
        inputbox.send_keys('_change')
        self.selenium.find_element_by_tag_name('button').click()
        temp_val = list(User.objects.values('last_name'))[0]['last_name']
        self.assertTrue(temp_val == test_user['id_last_name']+'_change')

