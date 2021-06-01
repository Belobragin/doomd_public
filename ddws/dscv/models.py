""" view module for LP rcognition app"""

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings 
from django.utils import timezone

from ddws.dscv.hardcode import *

import datetime, time, os
from PIL import Image


class DscvLp(models.Model):
    """
    This model describes LP database, input by users
    """

    # dscv_lp_input_user = models.ForeignKey(User, 
    #                                     on_delete=models.CASCADE,
    #                                     max_length=100, 
    #                                     default= 3,)
    dscv_lp_hint =  models.CharField("lp number as on the picture:",
                                        max_length=20,
                                        default = '', 
                                        blank = True)
    dscv_lp_input_date_time = models.DateTimeField('moment lp image was input', 
                                        default= timezone.now,
                                        null=False, 
                                        blank=False)
    dscv_lp_country =  models.CharField("lp number country",
                                        choices=LP_REGIONS_CHOICES,
                                        max_length=20,
                                        default=RUSSIA_LP_BRIEF,                                        
                                        null=False, #TODO: this must be chosen by script
                                        blank=False)
    dscv_lp_file = models.ImageField("File with LP image",
                                        upload_to=FILEFOLDER, 
                                        #widget=forms.ClearableFileInput(attrs={'multiple': True}), several files - ???
                                        null=False, 
                                        blank=False,
                                        #editable = True,
                                        )
    # def save(self, 
    #          resize = False, 
    #          new_size = (IMAGE_RESIZE_HEIGHT, IMAGE_RESIZE_WIDTH)):
    #     if not self.dscv_lp_file:
    #         return        
    #     super(DscvLp, self).save()
    #     image = Image.open(self.dscv_lp_file.name)
    #     if resize: image = image.resize(new_size, Image.ANTIALIAS)
    #     image.save(os.path.join(FILEFOLDER, self.dscv_lp_file.name))

    class Meta:        
        db_table = 'dscv_lp_image'
        verbose_name = 'lp_image'
    
    def __str__(self):
        return self.dscv_lp_image

@receiver(models.signals.post_delete, sender=DscvLp)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `DscvLp` object is deleted.
    """
    if instance.dscv_lp_file:
        if os.path.isfile(instance.dscv_lp_file.path):
            os.remove(instance.dscv_lp_file.path)

# @receiver(models.signals.pre_save, sender=MediaFile)
# def auto_delete_file_on_change(sender, instance, **kwargs):
#     """
#     Deletes old file from filesystem
#     when corresponding `MediaFile` object is updated
#     with new file.
#     """
#     if not instance.pk:
#         return False

#     try:
#         old_file = MediaFile.objects.get(pk=instance.pk).file
#     except MediaFile.DoesNotExist:
#         return False

#     new_file = instance.file
#     if not old_file == new_file:
#         if os.path.isfile(old_file.path):
#             os.remove(old_file.path)

# @receiver(post_save, sender=User)    
# def update_profile_signal(sender, instance, created, **kwargs):
#     """
#     This signal calls for lp recognition
#     """
#     if created:     
#         fruit = Dduser.objects.create(dduser=instance)
#         fruit.save()


class DscvLpResults(models.Model):
    """
    This model describes lp recognition results by tesseract algo
    """
    dscv_lpres_image = models.ForeignKey(DscvLp, 
                                        on_delete=models.CASCADE) #lp image - FK
    dscv_lpres_algo = models.CharField('Algorythm to recognize',
                                        max_length=20,  
                                        choices = ALGO_CHOICES,
                                        default= OTHER_ALGORYTM,
                                        ) #lp image - FK
    dscv_lpres_num = models.CharField("lp number as recognised",
                                        max_length=20,
                                        default = '',
                                        blank=True)
    dscv_lpres_date = models.DateTimeField('moment lp image was recognised', 
                                        default= timezone.now, 
                                        blank=False)
    dscv_lpres_pars = models.CharField("parameters on the moment of lp number recognition",
                                        max_length=200,
                                        default = DEFAULT_DSCV_PARS,
                                        blank=False)

    class Meta:        
        db_table = 'dscv_results'
        verbose_name = 'recognition results'

    def __str__(self):
        return self.dscv_lprec_algo + ' ' + self.dscv_lpres_image

    

