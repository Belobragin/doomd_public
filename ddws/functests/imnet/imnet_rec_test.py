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


class ImnetRecTests(BaseTest):
    """ tests imnet recognize app """

    upload_file = open(TESTFILEPIG, 'rb')
    form_data =   {'algorythm': RESNET50_REC_ALGORYTHM,
                   #'targeted' : None,
                   #'target_goal':None,
                   #'number_of_steps':
                   #'acall' : None,
                    }
    form_file = {'imagefile': SimpleUploadedFile(upload_file.name, upload_file.read())}

    def input_data_im_rec_form(self, algorythm):
        """
        fill image recognition form
        """
        self.selenium.get('%s%s' % (self.live_server_url, '/'+APP_PATH+IMNET_REC_PAGE))
        algorythm_input = self.selenium.find_element_by_id("id_algorythm")
        algorythm_input.send_keys(algorythm)
        image_input = self.selenium.find_element_by_id("id_imagefile")
        image_input.send_keys(os.path.join(os.getcwd(),TESTFILEPIG))

        self.selenium.find_element_by_id('im_rec_submit').click()


    def test_im_rec_form(self):
        """
        test image recognition form
        """
        #test form:            
        self.selenium.get('%s%s' % (self.live_server_url, '/'+APP_PATH+ IMNET_REC_PAGE))        
        form = ImnetRecInputForm(data = self.form_data, files = self.form_file)
        self.assertTrue(form.is_valid())
        
    def test_get_im_rec_page(self):
        #test get:       
        self.selenium.get('%s%s' % (self.live_server_url, '/'+APP_PATH+ IMNET_REC_PAGE))
        page_title = self.selenium.find_element_by_id('page_title').text
        self.assertIn(IMREC_PAGE_TITLE, page_title)        
        #test recognition functionality and correct redirect:
    
    def test_post_im_rec_page_and_recres_page(self):
        #test get:       
        if is_port_in_use():
            #other algo:
            self.input_data_im_rec_form(OTHER_ALGORYTM) #Algorythm in developing - ???
            self.assertEqual(self.selenium.find_element_by_id('page_title').text, IMRECRES_PAGE_TITLE)
            tabl = self.selenium.find_element_by_id('result').text
            self.assertIn('imagenetID label class_idx confidence', tabl)
            self.assertIn('None', tabl)
            #RESNET50_REC_ALGORYTHM algo:
            self.input_data_im_rec_form('ResNet50 - weights ImageNet') #THIS IS A MYSTERIOUS SWAP OF ALGO and ALGO_LABEL
                                                                       #DO NOT UNDERSTAND, WHY SEND LABEL, not VALUE
            self.assertEqual(self.selenium.find_element_by_id('page_title').text, IMRECRES_PAGE_TITLE)
            tabl = self.selenium.find_element_by_id('result').text
            self.assertIn('imagenetID label class_idx confidence', tabl)
            self.assertNotIn('None', tabl)
            self.assertIn('n02395406 hog 341 99', tabl)
            
        else:
            self.input_data_im_rec_form(OTHER_ALGORYTM)
            self.assertEqual(self.selenium.find_element_by_id('page_title').text, ERROR_PAGE_TITLE)
            self.input_data_im_rec_form(RESNET50_REC_ALGORYTHM)
            self.assertEqual(self.selenium.find_element_by_id('page_title').text, ERROR_PAGE_TITLE)
            self.assertIn(ERR_ML_SERVICE_SWITCHED_OFF, self.selenium.find_element_by_id('err_ess').text)

class ImnetAttTests(BaseTest):
    """ tests imnet attack app """
    pass


        
