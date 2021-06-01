""" forms for dscv app"""


from django import forms
from django.forms import Form, ModelForm, Textarea
from django.utils.translation import gettext_lazy as _

from dscv.models import DscvLp
from dscv.hardcode import *


class DscvLpInputForm(ModelForm):
    """
    In this form we collect info about license plates for recognizing
    """
    algorythm = forms.ChoiceField(widget=forms.Select(),
                                    choices=ALGO_CHOICES)
    lpfile = forms.FileField(label='License plate image:', 
                            widget=forms.ClearableFileInput(attrs={'type' : 'file',
                                                                    'accept': 'image/*',    
                                                                    'onchange':"loadFile(event);"}))
    class Meta:
        model = DscvLp
        fields = ('dscv_lp_hint', 'dscv_lp_country', ) #'dscv_lp_file' - exclude this after add widget, 
                                                       #  https://stackoverflow.com/questions/54748183/django-modelform-widgets-and-labels
    
    def save(self, ffile):
        compound_instance = super(DscvLpInputForm, self).save(commit=False)
        temp_dscv_lp_hint =  compound_instance.dscv_lp_hint        
        temp_dscv_lp_country =  compound_instance.dscv_lp_country        
        temp_dscv_lp_file = ffile #compound_instance.dscv_lp_file
        dscv_input_lp_instance = DscvLp(dscv_lp_hint=temp_dscv_lp_hint,
                                                dscv_lp_country=temp_dscv_lp_country,
                                                dscv_lp_file=  temp_dscv_lp_file)
        dscv_input_lp_instance.save()
        
        return dscv_input_lp_instance

    
