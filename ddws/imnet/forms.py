""" forms for imnet app"""


from django import forms
from django.forms import Form, ModelForm, Textarea
from django.utils.translation import gettext_lazy as _

#from imnet.models import *
from imnet.hardcode import *


class ImnetRecInputForm(Form):
    """
    By this form we get image to recognize
    """

    algorythm = forms.ChoiceField(widget=forms.Select(),
                                    choices=REC_ALGO_CHOICES)
    imagefile = forms.ImageField(label='Image to recognize:', 
                            widget=forms.ClearableFileInput(attrs={'type' : 'file',
                                                                    'accept': 'image/*',    
                                                                    'onchange':"loadFile(event);"}))
    
    # def save(self, ffile):
    #     compound_instance = super(ImnetInputForm, self).save()
        # temp_dscv_lp_hint =  compound_instance.dscv_lp_hint        
        # temp_dscv_lp_country =  compound_instance.dscv_lp_country        
        # temp_dscv_lp_file = ffile #compound_instance.dscv_lp_file
        # dscv_input_lp_instance = DscvLp(dscv_lp_hint=temp_dscv_lp_hint,
        #                                         dscv_lp_country=temp_dscv_lp_country,
        #                                         dscv_lp_file=  temp_dscv_lp_file)
        # dscv_input_lp_instance.save()
        
        #return compound_instance #dscv_input_lp_instance

class ImnetAttInputForm(Form):
    """
    This form for image/data to attack
    """

    algorythm   = forms.ChoiceField(widget=forms.Select(),
                                    choices=ATT_ALGO_CHOICES)    
    targeted    = forms.BooleanField(widget=forms.CheckboxInput(attrs={'id' : 'boxchecked',}),
                                    required=False)
    target_goal = forms.IntegerField(widget=forms.TextInput(attrs={'id' : 'hidden',}),                                     
                                    required=False,
                                    label = 'Target goal - ImageNet class idx')                                     
    number_of_steps = forms.ChoiceField(widget=forms.Select(),
                                        initial = '2',
                                        required=False,
                                        choices=NUM_STEPS_CHOICES)
    imagefile = forms.ImageField(label='Image to attack:', 
                                 widget=forms.ClearableFileInput(attrs={'type' : 'file',
                                                                        'accept': 'image/*',    
                                                                        'onchange':"loadFile(event);"}))
    
