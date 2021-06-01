"""This module is for hardcode constants for functests"""

PATH_TO_PROJECT = '/run/media/admin/bvv1/Myprojects/doomd'

import datetime,  sys
sys.path.append(PATH_TO_PROJECT)

#postgres init parameters - we do not commit them:
from ddparameters import dbase_init
from django.contrib.auth.models import User

#main data for the site:
PATH_TO_CHROME_DRIVER = '/opt/chromedriver84/chromedriver'

#test users:
test_user = {'id_username':'daodenis',
            'id_first_name':'Denis',
            'id_last_name':"Test",
            'id_email':'bvprobe19@rambler.ru',
            'id_password1':'ddd',
            'id_password2':'ddd',
            'id_dduser-0-birthdate':'10/14/1974',
            }
no_kill_test_user = {'id_username':'testuser',
                     'id_first_name':'vtest',
                     'id_last_name':"vtest",
                     'id_password1':'vvv',
                     'id_email':'vbelobragin@pm.me',
                    }

#test_formset_data:                   
dduser_formset_data = ['birthdate', ]
user_extend_table_name = 'dduser'
user_extend_table_name_id = user_extend_table_name +'_id'

#test psw:
new_test_psw = 'kkk' #any valid string to test new password

#test window
TEST_WINDOW_1_HEIGHT = 1024
TEST_WINDOW_1_WIDTH = 768

#pages testing:
DASHBOARD_MAIN_ID = 'user_greetings'
DASHBOARD_MAIN_ID_LAYOUT_X = 490
DASHBOARD_MAIN_ID_LAYOUT_Y = 180




#useful functions:
def assert_decorator(foo, *args):
    """return true if foo(*args) validates; otherwise return false"""
    try:
        foo(*args)
        return True
    except:
        return False

def create_test_user(tuser = test_user):
        """
        creates test user with data .hardcode.no_kill_test_user
        """
        return User.objects.create_user(username = tuser['id_username'],
                                        first_name = tuser['id_first_name'],
                                        last_name = tuser['id_last_name'],
                                        email =  tuser['id_email'],
                                        password =  tuser['id_password1'],)