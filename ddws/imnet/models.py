""" view module for image recognition app imnet"""

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings 
from django.utils import timezone

from imnet.hardcode import *

import datetime, time, os
from PIL import Image

   

