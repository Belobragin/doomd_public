import datetime, os, warnings

from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from django.test import TestCase

#from dscv.models import DscvLp
from ddws.imnet.hardcode import *
from ddws.imnet.forms import ImnetRecInputForm, ImnetAttInputForm
from ddws.hardcode import DEPLOY_RECIT_PORT, is_port_in_use,\
                          ERR_REDIR


class ImnetTests(TestCase):
    """ tests imnet app"""

    def setUp(self):
        warnings.simplefilter("ignore")
        self.ffile =    {'input_image': open(TESTFILEPIG, 'rb'),
                        "input_image_path":'',
                        "image_parameters": '{}',
                        }
        self.testfile = TESTFILEPIG

    def test_imnet_pages(self):
        """tests /imnet """
        
        print('\nTest urls in imnet app: ...\\imnet\\ - no login required')        
        response = self.client.get(reverse('imnet:imnet_initial'))
        self.assertEqual(response.status_code, 200)
        print('\nTest urls in imnet app: ...\\imnet\\imrec\\ - no login required')   
        response = self.client.get(reverse('imnet:imrec'))
        self.assertEqual(response.status_code, 200)
        print('\nTest urls in imnet app: ...\\imnet\\imrecres\\ - no login required')   
        response = self.client.get(reverse('imnet:imrecres'))
        self.assertEqual(response.status_code, 200)
        print('\nTest urls in imnet app: ...\\imnet\\imatt\\ - no login required') 
        response = self.client.get(reverse('imnet:imatt'))
        self.assertEqual(response.status_code, 200)
        print('\nTest urls in imnet app: ...\\imnet\\imattres\\ - no login required')   
        response = self.client.get(reverse('imnet:imattres'))
        self.assertEqual(response.status_code, 200) 

    def test_image_recognition_form(self):
        """
        tests inout form validness and get for \imnet\imrec page
        """
        upload_file = open(self.testfile, 'rb')
        #test form:
        form_data = {'algorythm': OTHER_ALGORYTM,}
        form_file = {'imagefile': SimpleUploadedFile(upload_file.name, upload_file.read())}
        form = ImnetRecInputForm(data = form_data, files = form_file)
        #print(form.errors)
        self.assertTrue(form.is_valid())
        
        #test get:
        response = self.client.get(reverse('imnet:imrec'))
        self.assertEqual(200, response.status_code)
        #print(response.content.decode())
        self.assertIn('Image input form', response.content.decode())        

    def test_image_post_no_recognition(self):    
        """
        page imnet/imrec
        test form post and redir result if fastapi is NOT run
        """
        if is_port_in_use(int(DEPLOY_RECIT_PORT)):
            raise ValueError('For this test FastApi app must be switched off')
        with open(self.testfile, 'rb') as upload_file:
            response = self.client.post(reverse(IMNET_REC), {'imagefile':upload_file, 'algorythm': RESNET50_REC_ALGORYTHM}) #OTHER_ALGORYTM})        
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, reverse(ERR_REDIR, args = (APP_PATH, APP_ERROR_REDIR,)))

    def test_image_post_recognition(self):    
        """
        page imnet/imrec
        test form post and redir result if fastapi is in run
        """
        if not(is_port_in_use(int(DEPLOY_RECIT_PORT))):
            raise ValueError('For this test FastApi app must be turned ON')
        with open(self.testfile, 'rb') as upload_file:
            response = self.client.post(reverse(IMNET_REC), {'imagefile':upload_file, 'algorythm': RESNET50_REC_ALGORYTHM}) #OTHER_ALGORYTM})        
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, reverse(IMNET_RECRES)) #, args = (APP_PATH, APP_ERROR_REDIR,)))


    def test_image_att_form(self):
        """
        page imnet/imatt
        test form and get for imnet/imatt 
        """
        upload_file = open(self.testfile, 'rb')
        form_file = {'imagefile': SimpleUploadedFile(upload_file.name, upload_file.read())}
        form_data = [{'algorythm': OTHER_ALGORYTM,
                     'number_of_steps':20,
                    },
                    {'algorythm': FGSM_ATTACK_ALGORYTHM,
                     'number_of_steps':1,
                    },
                    {'algorythm': BASIC_ITERATIVE,
                     'number_of_steps':1,
                    },
                    {'algorythm': BASIC_ITERATIVE,
                     'number_of_steps':1,
                     'targeted':True,
                     'target_goal':189,
                    },
                    {'algorythm': BASIC_ITERATIVE,
                     'number_of_steps':1,
                     'targeted':True,
                     'target_goal':None,
                    },
                    {'algorythm': FGSM_ATTACK_ALGORYTHM,
                     'nuer_of_steps':1,
                    },                    
                    {'algorythm': BASIC_ITERATIVE,
                     'number_of_steps':1,
                     'targ':True,
                     'target_goal':189,
                    },
                    {'algorythm': BASIC_ITERATIVE,
                     'number_of_steps':1,
                     'targeted':True,
                     'target':None,
                    },
                    ]
        fake_form_data = [{'algo': OTHER_ALGORYTM,
                     'number_of_steps':20,
                    },
                    {'algorythm': RESNET50_REC_ALGORYTHM,
                     'number_of_steps':1,
                    },
                    ]
        #test form:
        for form_d in form_data:
            form = ImnetAttInputForm(data = form_d, files = form_file)
            self.assertTrue(form.is_valid())
        for form_d in fake_form_data:
            form = ImnetAttInputForm(data = form_d, files = form_file)
            self.assertFalse(form.is_valid())
        form = ImnetAttInputForm(data = form_data[0])
        self.assertFalse(form.is_valid())    
        
        #test get:
        response = self.client.get(reverse('imnet:imatt'))
        self.assertEqual(200, response.status_code)
        #print(response.content.decode())
        self.assertIn('Image attack form', response.content.decode())        
        self.assertIn('Algorythm', response.content.decode()) 
        self.assertIn('Targeted', response.content.decode()) 
        self.assertIn('Target goal', response.content.decode()) 
        self.assertIn('Image to attack', response.content.decode()) 
        self.assertIn(FGSM_ATTACK_ALGORYTHM, response.content.decode())
        self.assertNotIn(RESNET50_REC_ALGORYTHM, response.content.decode())
        #test post
        with open(self.testfile, 'rb') as upload_file:
            cont_dict = {'imagefile':upload_file,
                        'algorythm': FGSM_ATTACK_ALGORYTHM,
                        'number_of_steps':'2',}                        
            if is_port_in_use(int(DEPLOY_RECIT_PORT)):         
                response = self.client.post(reverse(IMNET_ATT), cont_dict)
                self.assertEqual(302, response.status_code)
                self.assertRedirects(response, reverse(IMNET_ATTRES))
                response = self.client.post(reverse(IMNET_ATT), cont_dict.update({'algorythm': BASIC_ITERATIVE}))      
                self.assertEqual(302, response.status_code)
                self.assertRedirects(response, reverse(IMNET_ATTRES))
            else:
                response = self.client.post(reverse(IMNET_ATT), {'imagefile':upload_file, 
                                                                'algorythm': FGSM_ATTACK_ALGORYTHM})
                self.assertEqual(302, response.status_code)
                self.assertRedirects(response, reverse(ERR_REDIR, args = (APP_PATH, APP_ERROR_REDIR,))) 
                
