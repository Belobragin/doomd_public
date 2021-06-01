"""
base test class for all functional tests
"""


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
#from selenium.webdriver.common.keys import Keys

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from functests.hardcode import *
from ddws.hardcode import *


class BaseTest(StaticLiveServerTestCase):
    """
    tests layout
    """
    FULL_WINDOW_SELENIUM = True #False #set True to run 1920x1080

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        create_test_user()
        chrome_options = Options()
        if cls.FULL_WINDOW_SELENIUM:
            chrome_options.add_argument("--window-size=1920,1080")
        cls.selenium = webdriver.Chrome(PATH_TO_CHROME_DRIVER, chrome_options=chrome_options)
        cls.selenium.implicitly_wait(3)

    def setUp(self):
        self.credentials = {
            'username': no_kill_test_user['id_username'],
            'password': no_kill_test_user['id_password1'],}
        User.objects.create_user(**self.credentials)
        
        
    @classmethod
    def tearDownClass(cls):
        #cls.selenium.quit()
        cls.selenium.close()
        super().tearDownClass()
    
    def tearDown(self):
        pass