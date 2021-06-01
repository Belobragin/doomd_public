""" imnet app views """


import os
import time
import requests
import base64
import json
import cv2
from base64 import b64encode

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
from django.contrib.auth.mixins import UserPassesTestMixin, AccessMixin
from django.contrib.messages import get_messages
from django.conf import settings

from django.views import View
from django.views.generic import TemplateView

from django.contrib.auth.models import User

from ddws.hardcode import ERR_REDIR,\
                          RECIT_URL, ATTIT_URL,\
                          get_error_essence, obtain_recimage, make_context_results,\
                          ResultDict,\
                          BASE_REQUEST_FILE_DICT,\
                          TEST_TEMPLATE, DASHBOARD

from imnet.hardcode import *
from imnet.forms import ImnetRecInputForm, ImnetAttInputForm


class ImageInitialView(TemplateView):
    """
    .../imnet/ page view: description and algotythms list
    """

    template_name = IMNET_INITIAL_TEMPLATE

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = IMNET_INITIAL_PAGE_TITLE
        context['algo_list'] = [ATT_ALGO_CHOICES[k][1]
            for k in range(len(ATT_ALGO_CHOICES))]
        context['has_spoof_perm'] = self.request.user.has_perm(SPOOF_PERMISSIONS)

        return context


class ImageRecView(View):
    """
    .../imnet/imrec/ page view: input license plate picture and recognise it
    """

    ffile = BASE_REQUEST_FILE_DICT
    # redirect_page = 'imrecres' #!ATTN: to redirect to redirect_page, input self.redirect_page; redirect to initial - input ' ', NOT ''

    def get(self, request):
        return render(
                    request, IMNET_REC_TEMPLATE,
                    {"form": ImnetRecInputForm,
                    'page_title': IMREC_PAGE_TITLE,
                    'initial_page_title': IMNET_INITIAL_PAGE_TITLE,
                    })

    def post(self, request):
        result = []
        form = ImnetRecInputForm(request.POST,
                                request.FILES,
                                )
        if form.is_valid():
            # data = form.cleaned_data['imagefile'].read() #this will obtain file content - DO NOT DELETE
            path_to_save = os.path.join(
                settings.TEMP_PATH_TO_FILEFOLDER, form.cleaned_data['imagefile'].name)
            file_path = default_storage.save(
                path_to_save, form.cleaned_data['imagefile'])
            request.session['file_path'] = file_path
            with open(file_path, 'rb') as ff:
                self.ffile['input_image'] = ContentFile(
                    ff.read(), name=form.cleaned_data['imagefile'].name)

            temp_var = form.cleaned_data['algorythm']
            url = f'{RECIT_URL}?algo_name={temp_var}'

            try:
                r = requests.post(url, files=self.ffile)
                p = r.json()
                for _, element in p.items():
                    result.append(element)
                request.session['results'] = result
            except Exception as ee:
                try:
                    request.session['file_path'] = None
                    os.remove(file_path)
                except Exception:
                    pass
                messages.error(request, ERROR_MESSAGE_IMREC_FORM %
                               form['imagefile'].value())
                request.session['essence_error'] = get_error_essence(str(ee))
                request.session['full_error'] = str(ee)
                return redirect(reverse(ERR_REDIR, args=(APP_PATH, APP_ERROR_REDIR,)))

        messages.success(request, SUCCESS_MESSAGE_IMREC_FORM %
                         form['imagefile'].value())

        # return redirect(reverse(IMNET_REDIR, args = (self.redirect_page,))) #DO NOT DELETE - This is a correct way to redirect
        return redirect(reverse(IMNET_RECRES))


class ImageRecResultView(TemplateView):
    """
    .../imnet/imrecres/ page view: input imagenet picture recognition result
    """
    template_name = IMNET_RECRES_TEMPLATE

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        obtain_recimage(context,
                        self.request.session['file_path'])
        context['results'] = make_context_results(
            self.request.session['results'])
        context['initial_page_title'] = IMNET_INITIAL_PAGE_TITLE
        context['page_title'] = IMRECRES_PAGE_TITLE
        self.request.session['file_path'] = None
        self.request.session['results'] = None

        return context


class ImageAttView(View):
    """
    .../imnet/imatt/ page view: input imagenet picture and attack it
    """

    ffile = BASE_REQUEST_FILE_DICT

    def get(self, request):
        return render(
        request, IMNET_ATT_TEMPLATE,
        {"form": ImnetAttInputForm,
        'page_title': IMATT_PAGE_TITLE,
        'initial_page_title': IMNET_INITIAL_PAGE_TITLE,
        })

    def post(self, request):
        result = []
        temp_dict = {}
        form = ImnetAttInputForm(request.POST,
                                request.FILES,
                                )
        if form.is_valid():
            path_to_save = os.path.join(
                IMNET_ATT_FILES_PATH_TO_FILEFOLDER, form.cleaned_data['imagefile'].name)
            file_path = default_storage.save(
                path_to_save, form.cleaned_data['imagefile'])
            request.session['file_path'] = file_path

            with open(file_path, 'rb') as ff:
                self.ffile['input_image'] = ContentFile(
                    ff.read(), name=form.cleaned_data['imagefile'].name)
            temp_dict['steps'] = form.cleaned_data['number_of_steps']
            temp_dict["targeted"] = form.cleaned_data['targeted']
            temp_dict['target_goal'] = form.cleaned_data['target_goal']
            self.ffile['alter_parameters'] = json.dumps(temp_dict)

            temp_var = form.cleaned_data['algorythm']
            url = f'{ATTIT_URL}?algo_name={temp_var}'

            try:
                # this will fail if FataApi is turned off
                r = requests.post(url, files=self.ffile)

                try:
                    # this will fail, if we get structure with images, i.e. most convinient way
                    p = r.json()
                    for _, element in p.items():
                        result.append((element,))
                    request.session['results'] = result
                except:
                    # new format:
                    request.session['results'] = None
                    att_file_path = from_zip_stream_to_disk(r)
                    request.session['att_file_path'] = att_file_path

                messages.success(request, SUCCESS_MESSAGE_IMATT_FORM %
                                 form['imagefile'].value())

            except Exception as ee:
                try:
                    request.session['file_path'] = None
                    os.remove(file_path)
                except:
                    pass
                try:
                    request.session['att_file_path'] = None
                    os.remove(att_file_path)
                except:
                    pass
                messages.error(request, ERROR_MESSAGE_IMATT_FORM %
                               form['imagefile'].value())
                request.session['essence_error'] = get_error_essence(str(ee))
                request.session['full_error'] = str(ee)
                return redirect(reverse(ERR_REDIR, args=(APP_PATH, APP_ERROR_REDIR,)))

        return redirect(reverse(IMNET_ATTRES))


class ImageAttResultView(TemplateView):
    """
    .../imnet/imattres/ page view: input imagenet picture attack result
    """

    template_name = IMNET_ATTRES_TEMPLATE

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        result = []
        obtain_recimage(context,
                        self.request.session['file_path'])

        if not(self.request.session['results']):
            try:
                # read processed attack data from file to memoru:
                temp_data,\
                context['deltaNp'],\
                context['adverImage'],\
                context['delta_image'] = from_zip_file_to_att_data(
                    self.request.session['att_file_path'])
                # process attck data rec dict:
                for i, element in temp_data.items():
                    result.append(element)
                context['results'] = [ResultDict(
                    str(i+1), *res) for i, res in enumerate(result)]
                # process byte images:
                for context_parameter in ['adverImage', 'delta_image']:
                    content = cv2.imencode(
                        '.png', context[context_parameter])[1]
                    encoded = b64encode(content).decode()
                    context[context_parameter] = "data:%sbase64,%s" % (
                        'image/png;', encoded)
            except Exception as ee:
                context['deltaNp'] = None
                context['adverImage'] = ''
                context['delta_image'] = ''
                context['results'] = None
            finally:
                try:
                    os.remove(self.request.session['att_file_path'])
                except:
                    pass
        else:
            context['results'] = make_context_results(
                self.request.session['results'])

        self.request.session['file_path'] = None
        self.request.session['att_file_path'] = None
        context['initial_page_title'] = IMNET_INITIAL_PAGE_TITLE
        context['page_title'] = IMATTRES_PAGE_TITLE

        return context


class SpoofAttResultView(AccessMixin, TemplateView):
    """
    This class allows to spoof image based on the other image
    """

    ALLOWED_PERMISSIONS = SPOOF_PERMISSIONS 
    raise_exception = False
    template_name = IMNET_SPOOF_TEMPLATE

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            return self.handle_no_permission()
        if not self.request.user.has_perm(self.ALLOWED_PERMISSIONS):
            # Redirect the user to somewhere else - add your URL here
            return redirect(reverse(DASHBOARD))

        # Checks pass, let http method handlers process the request
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = IMNET_SPOOF_PAGE_TITLE
        return context
    
