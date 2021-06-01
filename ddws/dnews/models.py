from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.core.mail import BadHeaderError, send_mail
from django.dispatch import receiver
from django.conf import settings 
from django.utils import timezone

from dnews.hardcode import *

import datetime, time


class Ddnews(models.Model):
    """
    This model represents site news
    """
    header = models.CharField(max_length=200,
                              blank=False)
    news_text = models.CharField(max_length=800,
                              blank=False)
    release_date = models.DateTimeField('date published', 
                                        default = timezone.now,
                                        blank=False)
    
    def __str__(self):
       return self.header
    
    class Meta:
        db_table = 'doomd_news'


@receiver(post_save, sender = Ddnews)    
def make_email_deliver_signal(sender, instance, created, **kwargs):
    """
    This signal sends e-mails to users in the group 'news' after new element is added to Ddnews model
    """
    news_send_list = list(User.objects.filter(groups__name = 'news').values_list('email', flat = True))
    if created:     
        send_mail(
            instance.header,
            instance.news_text,
            settings.MAIL_NEWS_ADDRESS,
            news_send_list,
        )
    return