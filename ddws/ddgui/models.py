from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings 
from django.utils import timezone

from ddgui.hardcode import DDGUI_FILEFOLDER

import datetime, time

class Dduser(models.Model):
    """
    This model extends User class for those users, who commit to doom event 
    This class also adds id of a bucket, which stores doom docs
    """
    dduser = models.OneToOneField(User, 
                                  on_delete=models.CASCADE, 
                                  primary_key=True,)
    birthdate = models.DateField(blank=True, null=True)
    scheduled_dd_event = models.BooleanField(default=False, blank=False)
        
    #def __str__(self):
    #    return "%s the DoomDay service user." % self.dduser.id
    
    class Meta:
        db_table = 'dduser'

@receiver(post_save, sender=User)    
def update_profile_signal(sender, instance, created, **kwargs):
    """
    This signal updated Dduser model on User update
    """
    if created:     
        fruit = Dduser.objects.create(dduser=instance)
        fruit.save()

class Ddevent(models.Model):
    """
    This class describes doom event
    """
    #multichoice:
    standard_choice="SNCh"
    custom_choice="CNCh"
    doom_day_notification_choices=[(standard_choice, "standard_notification_choice"),
                                   (custom_choice, "custom_notification_choice"),
                                  ]
    doom_source_showup_monitor_choices=[(standard_choice, "standard_showup_monitoring_choice"),
                                   (custom_choice, "custom_showup_monitoring_choice")]                              
    #model:
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    fillFormGT=models.DateTimeField('global time doom request created', 
                                    default= timezone.now, 
                                    blank=False)
    #fillFormLT=models.DateTimeField('local time doom request created')
    doomCountStart=models.DateTimeField('moment doom count down start - LocalT, days-hours', 
                                        default= timezone.now, 
                                        blank=False)
    doomEventDate=models.DateField('moment of doom event, days since doomCountStart', 
                                    default=timezone.now, #+datetime.timedelta(days=settings.DEFAULT_DOOM_INTERVAL),
                                    blank=True)
    doomEventInterval=models.IntegerField('days since last show up', 
                                          default=settings.DEFAULT_DOOM_INTERVAL, 
                                          blank=False)
    #we use this to set the channel automatically monitor user activity:
    doomEventCollectSource=models.CharField("source to monitor user show up, otherwise initiate count down doom event interval",
                                        max_length=4, 
                                        choices=doom_source_showup_monitor_choices,
                                        default=standard_choice, 
                                        blank=False)
    #we use this to set the channel to send user notifications:
    doomNotifications=models.CharField("type of notifications send to user about doom event",
                                        max_length=4, 
                                        choices=doom_source_showup_monitor_choices,
                                        default=standard_choice, 
                                        blank=False)
    doomfile=models.FileField(upload_to=DDGUI_FILEFOLDER, 
                              #widget=forms.ClearableFileInput(attrs={'multiple': True}), several files - ???
                              null=True, 
                              blank=True)
    
    class Meta:
        db_table = 'ddevent'

@receiver(post_save, sender=Ddevent)    
def update_duser_scheduled_dd_event_signal(sender, instance, created, **kwargs):
    """
    This signal updates Duser model on Ddevent update.
    i.e. when user get (any) doom event, Dduser instance get scheduled_dd_event=True 
    """
    if created: 
        fruit = Dduser.objects.filter(dduser=instance.author_id).update(scheduled_dd_event=True)

class DoomEventDocsBucket(models.Model):
    """
    Docs storage
    """
    event=models.OneToOneField(Ddevent, 
                                on_delete=models.CASCADE, 
                                primary_key=True,)
    doomDayEventBucket=models.CharField("AWS or another bucket with documents to uncover if DoomDay event",
                                        max_length=80, blank=False, default='')
    doomDayMessage=models.CharField("Short message to inform on doom day come",
                                        max_length=40, blank=False, default='I am a short default doom message!')                                    

    class Meta:
        db_table = 'ddbucket'


#     def __str__(self):
#         pass

