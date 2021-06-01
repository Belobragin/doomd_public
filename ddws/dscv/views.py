""" dscv app views """


import os, time, requests

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView
from django.forms.models import inlineformset_factory
from django.core.exceptions import PermissionDenied
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.contrib import messages
from django.contrib.messages import get_messages
from django.conf import settings

from django.views import View
from django.views.generic import TemplateView

from django.contrib.auth.models import User

from ddws.hardcode import ERR_REDIR, ERR_REDIR_TEMPLATE,\
                          RECIT_URL, ATTIT_URL,\
                          get_error_essence, obtain_recimage, make_context_results,\
                          ResultDict,\
                          BASE_REQUEST_FILE_DICT,\
                          TEST_TEMPLATE

from dscv.models import DscvLp, DscvLpResults
from dscv.forms import DscvLpInputForm
from dscv.hardcode import *


@method_decorator(login_required, name='dispatch')
class DscvInitialView(TemplateView):
    """
    .../dscv/ page view: discover algotythms list
    """

    template_name = DSCV_INITIAL_TEMPLATE

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = DSCV_INITIAL_PAGE_TITLE
        context['algo_list'] = [ALGO_CHOICES[k][1] for k in range(len(ALGO_CHOICES))]
        
        return context

@method_decorator(login_required, name='dispatch')
class DscvReclpView(View):
    """
    .../dscv/reclp/ page view: input license plate picture and recognise it
    """
    
    ffile = BASE_REQUEST_FILE_DICT

    def get(self, request):
        return render(
        request, DSCV_INPUT_LP_TEMPLATE,
        {"form": DscvLpInputForm,
        'page_title':DSCV_RECOGNITION_FORM_TITLE,
        'initial_page_title':DSCV_INITIAL_PAGE_TITLE,
        })

    def post(self, request):
        result = []
        form = DscvLpInputForm(request.POST, 
                                request.FILES,
                                )
        if form.is_valid():
            form.save(ffile = form['lpfile'].value())
            lp_country = form.cleaned_data['dscv_lp_country']
            user_recognize_lp = form.cleaned_data['dscv_lp_hint']
            path_to_save = os.path.join(settings.TEMP_PATH_TO_FILEFOLDER, form.cleaned_data['lpfile'].name)
            file_path = default_storage.save(path_to_save, form.cleaned_data['lpfile'])
            request.session['file_path'] = file_path
            with open(file_path, 'rb') as ff:
                self.ffile['input_image'] = ContentFile(ff.read(), name=form.cleaned_data['lpfile'].name)

            temp_var = form.cleaned_data['algorythm']
            url = f'{RECIT_URL}?algo_name={temp_var}'           
            
            try:
                r = requests.post(url, files = self.ffile)
                p = r.json()
                for _, element in p.items():
                    element_ = (element, user_recognize_lp, lp_country)
                    #element_ = (element,)
                    result.append(element_)              
                request.session['results'] = result
            except Exception as ee:
                try:
                    request.session['file_path'] = None
                    os.remove(file_path)
                except Exception:
                    pass
                messages.error(request, ERROR_MESSAGE_DSCVREC_FORM % form['lpfile'].value())
                request.session['essence_error'] = get_error_essence(str(ee))
                request.session['full_error'] = str(ee)
                return redirect(reverse(ERR_REDIR, args = (APP_PATH, APP_ERROR_REDIR,))) 

        messages.success(request, SUCCESS_MESSAGE_DSCV_LP_FORM % form['lpfile'].value())          
        
        #return redirect(reverse(IMNET_REDIR, args = (self.redirect_page,))) #DO NOT DELETE - This is a correct way to redirect
        return redirect(reverse(DSCV_LP_RES))


@method_decorator(login_required, name='dispatch')
class DscvReclpResView(TemplateView):

    template_name = DSCV_LP_RES_TEMPLATE    
    
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        obtain_recimage(context,
                        self.request.session['file_path'])         
        context['results'] = make_context_results(self.request.session['results'])            
        #DO NOT DELETE _ TODO: make redirection from template if results are None
        # except Exception as ee:
        #     #messages.error(self.request, ERROR_MESSAGE_DSCVREC_FORM % form['lpfile'].value())
        #     context['essence_error'] = get_error_essence(str(ee))
        #     context['full_error'] = str(ee) 
        #     context['application'] = APP_PATH
        #     context['redirect_path'] = APP_ERROR_REDIR 
        #finally:
        context['initial_page_title'] = DSCV_INITIAL_PAGE_TITLE      
        context['page_title'] = DSCV_LPRES_PAGE_TITLE       
        self.request.session['file_path'] = None
        self.request.session['results'] = None

        return context

