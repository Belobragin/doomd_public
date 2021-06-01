from django import forms
from django.forms import ModelForm
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User
from ddgui.models import Dduser

from captcha.fields import ReCaptchaField, ReCaptchaV3


class SignUpForm(UserCreationForm):
    """
    Sign-up form. Only selected fields are displayed
    """  
    
    promocode = forms.CharField(max_length = 8, 
                                min_length = 4, 
                                required=False)
    read_news = forms.BooleanField(label='Check, if you want to recieve site news', 
                                   widget=forms.CheckboxInput(attrs={'id' : 'read_news_checked',}),
                                   required=False)

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', "email",)

    #we put additional field to the form and must exclude it on save:
    def save(self, commit=True):
        """
        avoid save 'promocode' field
        """
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")
        
        temp_user = User.objects.create_user(username = self.cleaned_data.get('username'),
                                             email = self.cleaned_data.get('email'),
                                             password = self.cleaned_data.get('password1'),
        )
        temp_user.first_name = self.cleaned_data.get('first_name')
        temp_user.last_name = self.cleaned_data.get('last_name')
        if commit:
            temp_user.save()        
        return temp_user 

class UpdateForm(forms.ModelForm):
    """
    Update form. Only selected fields are displayed
    """
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email',]

class DoomDayForm(UserCreationForm):
    pass
