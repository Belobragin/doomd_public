from django import forms
from django.forms import ModelForm, Textarea
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import User
from .models import Ddevent


class DoomDayEventForm(ModelForm):
    """
    In this form we collect info about doom day moment, what to send and how to
    """
    
    class Meta:
        model = Ddevent
        fields = ('doomCountStart', 'doomEventInterval', 'doomNotifications', 'doomfile')
        labels = {
            'doomCountStart': _("Start monitor activity at:"),
            'doomEventInterval': _("No show-up time(days):"),
            'doomNotifications': _("Way to inform you about doom day:"),
        }
        help_texts = {
            'doomCountStart': _("Format YYYY/MM/DD HH:mm"),
            'doomEventInterval': _("Days"),
            'doomNotifications': _("Choose from alternatives"),
        }
        #error_messages = {
        #    'doomCountStart': _("Start monitor activity at:"),
        #    'doomEventInterval': _("No show-up time(days):"),
        #    'doomNotifications': _("Way to inform you about doom day:"),
        #    },