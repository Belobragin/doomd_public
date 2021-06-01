"""This module is for imnet hardcode constants"""
import os
from django.conf import settings 

APP_PATH = 'imnet'
IMNET_PATH_TO_FILEFOLDER =  os.path.join(settings.MEDIA_ROOT, APP_PATH)

#pages data:
APP_ERROR_REDIR = ' ' #this is not ''!
IMNET_INITIAL = 'imnet:imnet_initial'
IMNET_RECRES = 'imnet:imrecres'
IMNET_REC = 'imnet:imrec'
IMNET_ATTRES = 'imnet:imattres'
IMNET_ATT = 'imnet:imatt'

#imnet templates:
IMNET_INITIAL_TEMPLATE = 'imnet/imnet_initial.html'
IMNET_REC_TEMPLATE = 'imnet/imnet_rec.html'
IMNET_RECRES_TEMPLATE = 'imnet/imnet_recres.html'
IMNET_ATT_TEMPLATE = 'imnet/imnet_att.html'
IMNET_ATTRES_TEMPLATE = 'imnet/imnet_attres.html'
IMNET_REDIR_TEMPLATE = 'imnet/imnet_redir.html'
IMNET_ERR_REDIR_TEMPLATE = 'imnet/imnet_err_redir.html'
IMNET_SPOOF_TEMPLATE = 'imnet/imnet_spoof.html'

#pages titles:
IMNET_INITIAL_PAGE_TITLE = 'Recognize and/or attack image from Imagenet set'
IMREC_PAGE_TITLE = 'Image input form:'
IMRECRES_PAGE_TITLE = 'Image recognition result:'
IMATTRES_PAGE_TITLE = 'Image attack result:'
IMATT_PAGE_TITLE = 'Image attack form:'
IMNET_ERROR_PAGE_TITLE = 'Error occured'
IMNET_SPOOF_PAGE_TITLE = 'Spoof attack form'

#messages:
IMNET_REDIRECT_MESSAGE = 'You will get recognition results soon.'
SUCCESS_MESSAGE_IMREC_FORM = 'Image %s sent to recognition'
ERROR_MESSAGE_IMREC_FORM = 'Image %s error on recognition'
SUCCESS_MESSAGE_IMATT_FORM = 'Image %s sent to attack processing'
ERROR_MESSAGE_IMATT_FORM = 'Image %s attack processing error'

#permissions:
SPOOF_PERMISSIONS = 'auth.can_promo' #'can_spoof'

#Algorythms:
BASE_ALGO_DESCRIPTION = 'No description'
OTHER_ALGORYTM = 'other'
#attack algorythms:
FGSM_ATTACK_ALGORYTHM = 'fgsm'
BASIC_ITERATIVE = 'bim'
ATT_ALGO_CHOICES = (
        (OTHER_ALGORYTM, 'Algorythm in developing'),
        (FGSM_ATTACK_ALGORYTHM, 'FGSM attack'),
        (BASIC_ITERATIVE, 'Basic Iterative'),
)
NUM_STEPS_CHOICES = ((1, '1'),
                     (2, '2'),
                     (3, '3'),
                     (5, '5'),
                     (10, '10'),
                     (20, '20'),
                     (30, '30'),
                     (40, '40'),
                     (50, '50'),
                     (100, '100'),
                     (200, '200'),
                     (400, '400'),
                     (500, '500'),
                     (1000, '1000')
)
IMNET_ATT_FILES_PATH_TO_FILEFOLDER = os.path.join(settings.MEDIA_ROOT, 'imnet_att_initial_images')

#recognize algorythms:
RESNET50_REC_ALGORYTHM = 'NN_ResNet50'
REC_ALGO_CHOICES = (
        (OTHER_ALGORYTM, 'Algorythm in developing'),
        (RESNET50_REC_ALGORYTHM, 'ResNet50 - weights ImageNet'),
)

#tests:
IMNET_REC_PAGE = '/imrec/'
IMNET_RECRES_PAGE = '/imrecres/'
IMNET_ATT_PAGE = '/imatt/'
IMNET_ATTRES_PAGE = 'imattres'
#TESTFILE = 'test_data/12346.jpeg'
#TESTFILEPIG = 'test_data/pig.jpg'

def from_zip_stream_to_att_data_correctnp(r,
                                target_path = None,
                                ):
        """
        this foo takes response object with zip file and extract attack data
        please, refer to:
        - alpm.changeit.tweaks.BasicIterativeAttack 
        AND/OR:
        - alpm.alpmapi.get_altit_algo
        specifications.

        - r :: response object, media_type="application/x-zip-compressed"  
        - target_path - path to save file, default is None (do not save)

        - return: tuple of (back_data, deltaNp, adverImage, delta_image), 
        where:
                - back_data (chunk_01):: regognition data for attacked image (i.e. fake recognitions)
                - deltaNp (chunk_02):: np.array :: delta addition to image (attack add-on), shape the same as image, type np.float32
                - adverImage (chunk_03):: np.array :: attackedge, type np.uint8
                - delta_image (chunk_04):: np.array :: this is a non-strict transformation of deltaNp, for visualising goal only, type np.uint8
                - npshapes (npshapes):: serialized dict like {"chunk_02": [224, 224, 3]} with a shape of adverImage (other np.arrays have the same shape)
                this foo version output IS serializable
        """
        import zipfile, io, json
        import numpy as np

        if r is None:
            raise ValueError('response object must not be None')
            return tuple([None]*5)
        
        try:
            temp_content = r.content
        except:
            raise ValueError('Can not read response content')
        
        if target_path is not None:
            with open(target_path, 'wb') as ff:
                ff.write(temp_content)
        
        temp_data = {}
        y = io.BytesIO()
        y.write(temp_content)
        myzipfile = zipfile.ZipFile(y)
        for name in myzipfile.namelist():
            temp_data[name] = myzipfile.open(name).read()
        back_shape_size = json.loads(temp_data['npshapes'].decode()).get('chunk_02')

        return  json.loads(temp_data['chunk_01'].decode()),\
                np.frombuffer(temp_data['chunk_02'], dtype=np.float32).reshape(back_shape_size).tolist(),\
                np.frombuffer(temp_data['chunk_03'], dtype=np.uint8).reshape(back_shape_size).tolist(),\
                json.dumps(np.frombuffer(temp_data['chunk_04'], dtype=np.uint8).reshape(back_shape_size).tolist())
        

def from_zip_stream_to_disk(r,
                            target_path = os.path.join(IMNET_ATT_FILES_PATH_TO_FILEFOLDER, 'temp_att_file.zip'),
                            ):
        """
        follow explanations at from_zip_stream_to_att_data_correctnp
        """
        import zipfile, io, json, uuid
        
        if r is None:
            raise ValueError('response object must not be None')
            return tuple([None]*5)
        
        try:
            temp_content = r.content
        except:
            raise ValueError('Can not read response content')
        
        if target_path is not None:
            target_path = target_path +str(uuid.uuid4())[:6]
            with open(target_path, 'wb') as ff:
                ff.write(temp_content)
        
        return target_path


def from_zip_file_to_att_data(target_path = None,
                             ):
        """
        follow explanations at from_zip_stream_to_att_data_correctnp
        """

        import zipfile, io, json
        import numpy as np

        temp_data = {}

        if target_path is None:
            raise FileError('Path to file with attack data must be specified')
            return tuple([None]*5)
        try:           
            myzipfile = zipfile.ZipFile(target_path)        
            for name in myzipfile.namelist():
                temp_data[name] = myzipfile.open(name).read()
            back_shape_size = json.loads(temp_data['npshapes'].decode()).get('chunk_02')
            return  json.loads(temp_data['chunk_01'].decode()),\
                    np.frombuffer(temp_data['chunk_02'], dtype=np.float32).reshape(back_shape_size),\
                    np.frombuffer(temp_data['chunk_03'], dtype=np.uint8).reshape(back_shape_size),\
                    np.frombuffer(temp_data['chunk_04'], dtype=np.uint8).reshape(back_shape_size)
        except:
           raise ValueError('Can not read att zip file content')    
        return tuple([None]*5)
          




        