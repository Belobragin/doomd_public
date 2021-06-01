"""This module is for dscv hardcode constants"""
import os
from django.conf import settings 

FILEFOLDER = 'lps/'
PATH_TO_FILEFOLDER =  os.path.join(settings.BASE_DIR, 'media', FILEFOLDER)
APP_PATH = 'dscv'

ANONYMOUS_USER = 'Anonymous'

#dscv templates:
DSCV_INITIAL_TEMPLATE = 'dscv/dscv_initial.html'
DSCV_INPUT_LP_TEMPLATE = 'dscv/dscv_inputlp.html'
DSCV_LP_RES_TEMPLATE = 'dscv/dscv_recres.html'

#pages parameters:
DSCV_INITIAL_PAGE_TITLE = 'LP recognize'
DSCV_RECOGNITION_FORM_TITLE = 'License plate recognition form:'
DSCV_LPRES_PAGE_TITLE = 'License plate recognition result'

#redirects:
DSCV_LP_RES ="dscv:dscv_reclpres"

#messages:
SUCCESS_MESSAGE_DSCV_LP_FORM = 'License plate image %s sent to recognition'
ERROR_MESSAGE_DSCVREC_FORM = 'License plate %s error on recognition'

#pages adress:
DSCV_FORM_PAGE_ADRESS = 'reclp/'

#pages data:
APP_ERROR_REDIR = ' '
DSCV_REDIRECT_MESSAGE = 'You are redirected now.'

#tesseract recognition:
DEFAULT_DSCV_PARS = ''
DEFAULT_TESSER_PARS = "-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 --psm 7"

#region choices:
RUSSIA_LP_BRIEF = 'RUS'
UKRAINE_LP_BRIEF = 'UA'
PERU_LP_BRIEF = 'PERU'
EUROPE_LP_BRIEF = 'EU'
GERMAN_LP_BRIEF = 'D'
LP_REGIONS_CHOICES = (
        ('Russia', RUSSIA_LP_BRIEF),
        ('Ukraine', UKRAINE_LP_BRIEF),
        ('Peru', PERU_LP_BRIEF),
        ('Europe', EUROPE_LP_BRIEF),
        ('Germany', GERMAN_LP_BRIEF),
)

#Algorythms:
BASE_ALGO_DESCRIPTION = 'No description'
OTHER_ALGORYTM = 'other'
TESSERACT_SIMPLE_ALGORYTHM = 'tessimple'
ALGO_CHOICES = (
        (OTHER_ALGORYTM, 'Algorythm in developing'),
        (TESSERACT_SIMPLE_ALGORYTHM, 'Tesseract - no preprocessing'),
)

#tests:
TESTFILE = 'test_data/12346.jpeg'

#other:
IMAGE_RESIZE_HEIGHT = 500
IMAGE_RESIZE_WIDTH = 100