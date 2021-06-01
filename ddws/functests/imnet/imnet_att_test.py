import datetime, os, time

from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

#from django.test import TestCase
from ddws.functests.basefunctest import BaseTest

from ddws.functests.hardcode import *
#from imnet.models import 
from ddws.imnet.hardcode import *
from ddws.imnet.forms import ImnetRecInputForm, ImnetAttInputForm
from ddws.hardcode import is_port_in_use, TESTFILEPIG,\
                        ERROR_PAGE_TITLE, ERR_ML_SERVICE_SWITCHED_OFF


class ImnetAttTests(BaseTest):
    """ tests imnet recognize app """

    upload_file = open(TESTFILEPIG, 'rb')
    form_data =   {'algorythm': OTHER_ALGORYTM,
                   #'targeted' : None,
                   #'target_goal':None,
                   #'number_of_steps':
                   #'acall' : None,
                    }
    form_file = {'imagefile': SimpleUploadedFile(upload_file.name, upload_file.read())}

    def input_data_im_att_form(self,
                                algorythm, 
                                targeted = None,
                                target_goal = None,
                                number_of_steps = 2,
                                ):
        """
        fill image attack form
        """
        self.selenium.get('%s%s' % (self.live_server_url, '/'+APP_PATH+IMNET_ATT_PAGE))
        self.selenium.find_element_by_id("id_algorythm").send_keys(algorythm)
        self.selenium.find_element_by_id("id_imagefile").send_keys(os.path.join(os.getcwd(),TESTFILEPIG))
        if targeted: self.selenium.find_element_by_id("boxchecked").click()
        if target_goal: self.selenium.find_element_by_id("hidden").send_keys(target_goal)
        if number_of_steps: self.selenium.find_element_by_id("id_number_of_steps").send_keys(number_of_steps)
        self.selenium.find_element_by_id('im_att_submit').click()


    def test_im_att_form(self):
        """
        test image recognition form
        """
        #test form:            
        self.selenium.get('%s%s' % (self.live_server_url, '/'+APP_PATH+ IMNET_ATT_PAGE))        
        form = ImnetAttInputForm(data = self.form_data, files = self.form_file)
        self.assertTrue(form.is_valid())
        self.form_data.update({'algorythm':FGSM_ATTACK_ALGORYTHM})
        form = ImnetAttInputForm(data = self.form_data, files = self.form_file)
        self.assertTrue(form.is_valid())
        self.form_data.update({'algorythm':BASIC_ITERATIVE})
        form = ImnetAttInputForm(data = self.form_data, files = self.form_file)
        self.assertTrue(form.is_valid())
        self.form_data.update({'algorythm':'ALGO_FROM_NOWHERE'})
        form = ImnetAttInputForm(data = self.form_data, files = self.form_file)
        self.assertFalse(form.is_valid())
        self.form_data.update({'algorythm':BASIC_ITERATIVE,
                                'targeted' : True,
                                'target_goal':186,
                                'number_of_steps':3,
                                'acall' : True
                                })
        form = ImnetAttInputForm(data = self.form_data, files = self.form_file)
        self.assertTrue(form.is_valid())
        self.form_data.update({'algorythm':BASIC_ITERATIVE,
                                'targeted' : True,
                                'target_goal':'zaraza',
                                'number_of_steps':3,
                                'acall' : True
                                })
        form = ImnetAttInputForm(data = self.form_data, files = self.form_file)
        self.assertFalse(form.is_valid())
        self.form_data.update({'algorythm':BASIC_ITERATIVE,
                                'targeted' : True,
                                'target_goal':202,
                                'number_of_steps':100003,
                                'acall' : True
                                })
        form = ImnetAttInputForm(data = self.form_data, files = self.form_file)
        self.assertFalse(form.is_valid())


    def test_get_im_att_page(self):
        #test get:       
        self.selenium.get('%s%s' % (self.live_server_url, '/'+APP_PATH+ IMNET_ATT_PAGE))
        page_title = self.selenium.find_element_by_id('page_title').text
        self.assertIn(IMATT_PAGE_TITLE, page_title)        
    
    def test_post_im_att_page_other(self):
        #test get:       
        if is_port_in_use():
            #other algo:
            self.input_data_im_att_form(OTHER_ALGORYTM) #Algorythm in developing - ???
            self.assertEqual(self.selenium.find_element_by_id('page_title').text, IMATTRES_PAGE_TITLE)
            tabl = self.selenium.find_element_by_id('result').text
            self.assertIn('imagenetID label class_idx confidence', tabl)
            self.assertIn('Test option', tabl)
        else:
            self.input_data_im_att_form(OTHER_ALGORYTM)
            self.assertEqual(self.selenium.find_element_by_id('page_title').text, ERROR_PAGE_TITLE)
            self.assertIn(ERR_ML_SERVICE_SWITCHED_OFF, self.selenium.find_element_by_id('err_ess').text)
            
    def test_post_im_att_page_fgsm(self):
        #test get:       
        if is_port_in_use():
            #FGSM_ATTACK_ALGORYTHM algo:
            self.input_data_im_att_form(FGSM_ATTACK_ALGORYTHM)
            self.assertEqual(self.selenium.find_element_by_id('page_title').text, IMATTRES_PAGE_TITLE)
            tabl = self.selenium.find_element_by_id('result').text
            self.assertIn('imagenetID label class_idx confidence', tabl)
            self.assertIn('Not implemented', tabl)
        else:
            self.input_data_im_att_form(FGSM_ATTACK_ALGORYTHM)
            self.assertEqual(self.selenium.find_element_by_id('page_title').text, ERROR_PAGE_TITLE)
            self.assertIn(ERR_ML_SERVICE_SWITCHED_OFF, self.selenium.find_element_by_id('err_ess').text)

    def test_post_im_att_page_basic_iterative_untarg(self):
        #test get:       
        if is_port_in_use():        
            #BASIC_ITERATIVE untargeted algo:
            self.input_data_im_att_form(BASIC_ITERATIVE, number_of_steps = 30)
            self.assertEqual(self.selenium.find_element_by_id('page_title').text, IMATTRES_PAGE_TITLE)
            tabl = self.selenium.find_element_by_id('result').text
            self.assertIn('imagenetID label class_idx confidence', tabl)
            self.assertIn('n01883070 wombat 106 78', tabl) 
        else:
            self.input_data_im_att_form(BASIC_ITERATIVE)
            self.assertEqual(self.selenium.find_element_by_id('page_title').text, ERROR_PAGE_TITLE)
            self.assertIn(ERR_ML_SERVICE_SWITCHED_OFF, self.selenium.find_element_by_id('err_ess').text)

    def test_post_im_att_page_basic_iterative_targ(self):
        #test get:       
        if is_port_in_use():        
            #BASIC_ITERATIVE targeted algo:
            self.input_data_im_att_form(BASIC_ITERATIVE, number_of_steps = 200, targeted = True, target_goal = 189)
            self.assertEqual(self.selenium.find_element_by_id('page_title').text, IMATTRES_PAGE_TITLE)
            tabl = self.selenium.find_element_by_id('result').text
            self.assertIn('imagenetID label class_idx confidence', tabl)
            self.assertIn('n02095570 Lakeland_terrier 189 100', tabl)
        else:
            self.input_data_im_att_form(BASIC_ITERATIVE, number_of_steps = 200, targeted = True, target_goal = 189)
            self.assertEqual(self.selenium.find_element_by_id('page_title').text, ERROR_PAGE_TITLE)
            self.assertIn(ERR_ML_SERVICE_SWITCHED_OFF, self.selenium.find_element_by_id('err_ess').text)

            
        



        
