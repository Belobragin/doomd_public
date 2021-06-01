"""
Tests for layout
"""
import time 

from functests.basefunctest import BaseTest
from functests.hardcode import *
from ddws.hardcode import *

class NewVisitorTest(BaseTest):
    """
    tests layout
    """
    FULL_WINDOW_SELENIUM = True #False #set True to run 1920x1080

        
    def test_dashboard_layout(self):
        """ tests dashboard page layout"""

        print('\nDashboard page layout test')
        self.selenium.get('%s%s' % (self.live_server_url, LOGIN_PAGE_ADRESS))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys(test_user['id_username'])
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys(test_user['id_password1'])
        self.selenium.find_element_by_tag_name('button').click() 
        self.selenium.get('%s%s' % (self.live_server_url, DASHBOARD_PAGE_ADRESS))
        #self.selenium.set_window_size(TEST_WINDOW_1_HEIGHT, TEST_WINDOW_1_WIDTH) #- dynamic resizing must be tested too!
        inputbox = self.selenium.find_element_by_id(DASHBOARD_MAIN_ID)
        time.sleep(5)
        self.assertAlmostEqual(inputbox.location['x'], DASHBOARD_MAIN_ID_LAYOUT_X, delta=5)
        self.assertAlmostEqual(inputbox.location['y'], DASHBOARD_MAIN_ID_LAYOUT_Y, delta=1)
       

 
