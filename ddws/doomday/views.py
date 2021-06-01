""" doomday app views """

import datetime, requests
import time
import json

from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.messages import get_messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.forms.models import inlineformset_factory
from django.core.exceptions import PermissionDenied
from django.conf import settings
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse

from django.views import View
from django.views.generic import TemplateView

from django.contrib.auth.models import User, Group

from django.contrib.auth.views import PasswordResetView

from ddws.hardcode import *

from doomday.forms import SignUpForm, UpdateForm

from ddgui.models import Dduser
from ddgui.forms import DoomDayEventForm


class TestView(TemplateView):
    """
    .../imnet/imattres/ page view: input imagenet picture attack result
    """
    template_name = TEST_TEMPLATE

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #context['page_title'] = IMNET_INITIAL_PAGE_TITLE
        #context['algo_list'] = [ATT_ALGO_CHOICES[k][1] for k in range(len(ATT_ALGO_CHOICES))]

        return context


class DashboardView(TemplateView):
    """
    Zero page
    """
    template_name = DASHBOARD_TEMPLATE

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['page_title'] = DOOMDAY_DASHBOARD_PAGE_TITLE
        # This is also correct:
        # context =   {
        #             'page_title': DOOMDAY_DASHBOARD_PAGE_TITLE,
        #             }
        return context


class AboutView(TemplateView):
    """
    View for about portal page
    """
    template_name = ABOUT_TEMPLATE

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = DOOMDAY_ABOUT_PAGE_TITLE

        return context


class ErrorRedirectView(TemplateView):
    """
    View for redirect on error case app page
    """
    template_name = ERR_REDIR_TEMPLATE

    def get_context_data(self, application_page, redirect_page, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'mydelay': settings.ERROR_REDIRECT_DELAY,
                        'application': application_page,
                        'page_title': ERROR_PAGE_TITLE,
                        'err_ess': self.request.session.get('essence_error', None),
                        'err_descr': self.request.session.get('full_error', None),
                        'redirect_path': redirect_page, }
                       )

        return context


class DdredirectView(TemplateView):
    """
    View for redirect portal page
    """
    template_name = REDIRECT_TEMPLATE

    def get_context_data(self, redirect_page="about/", **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'mydelay': settings.REDIRECT_DELAY,
            'goto_page': redirect_page,
            'redirect_path': redirect_page,
            'page_title': DOOMDAY_REDIRECT_MESSAGE,
        })

        return context


class RegisterView(View):
    """
    Registration form NEW (with 'birthday' field)
    """

    DduserInlineFormset = inlineformset_factory(User,
                                                Dduser,
                                                fields=('birthdate',),
                                                can_delete=False, )
    formset = DduserInlineFormset(instance=None)

    def get(self, request):

        if request.user.is_authenticated:
            messages.warning(request, WARNING_MESSAGE % request.user.username)
            return redirect(reverse(DASHBOARD))
        else:
            return render(
                request, REGISTER_TEMPLATE,
                {"form": SignUpForm,
                 "formset": self.formset,
                 'inform_key': settings.MY_CAPTCHA_SITE_KEY,
                 })

    def post(self, request):
               
        form = SignUpForm(request.POST)
        if form.is_valid():
            #print('1', form.cleaned_data)
            recaptcha_response = request.POST.get('g-recaptcha-response')
            #print('2',recaptcha_response)
            data = {
                'secret': settings.MY_CAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            r = requests.post(
                'https://www.google.com/recaptcha/api/siteverify', data=data)
            res_captcha = r.json()
            #print('3',res_captcha)
            if not res_captcha['success']:
                messages.error(request, ERROR_MESSAGE_ON_CAPTCHA)
                return redirect(reverse(LOGIN_P))
            else:
                user = form.save(commit=False)
                user_promocode = form.cleaned_data['promocode']
                self.formset = self.DduserInlineFormset(request.POST,
                                                        request.FILES,
                                                        instance=user)
                if self.formset.is_valid():
                    user.backend = "django.contrib.auth.backends.ModelBackend"
                    if check_promocode(user_promocode):
                        # include user to promocode group
                        group = Group.objects.get(name=PROMOCODE_GROUP)
                        user.groups.add(group)
                    if read_news:
                        group = Group.objects.get(name=WANT_RECIEVE_NEWS_GROUP)
                        user.groups.add(group)
                    user.save()
                    self.formset.save()
                    login(request, user)
                    #login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    # storage = get_messages(request)
                    # for message in storage:
                    messages.success(request, SUCCESS_MESSAGE % user.username)
                    # return redirect(reverse(REDIR))
                            
        return redirect(reverse(DASHBOARD))


@login_required()  # only logged in users should access this
def edit_user(request):
    """
    Update user data
    https://blog.khophi.co/extending-django-user-model-userprofile-like-a-pro/
    """

    upk = request.user.id
    user = User.objects.get(pk=upk)
    user_form = UpdateForm(instance=user)
    DduserInlineFormset = inlineformset_factory(
        User, Dduser, fields=('birthdate', 'read_news'))
    formset = DduserInlineFormset(instance=user)

    if request.user.is_authenticated:  # and request.user.id == upk
        if request.method == "POST":
            user_form = UpdateForm(request.POST, request.FILES, instance=user)
            formset = DduserInlineFormset(
                request.POST, request.FILES, instance=user)
            if user_form.is_valid():
                created_user = user_form.save(commit=False)
                formset = DduserInlineFormset(
                    request.POST, request.FILES, instance=created_user)
                if formset.is_valid():
                    created_user.save()
                    formset.save()
                    return redirect(reverse(DASHBOARD))
        return render(request, UPDATE_TEMPLATE,
                      {
                          "noodle_form": user_form,
                          "formset": formset,
                      })
    else:
        raise PermissionDenied


class MyPasswordResetView(PasswordResetView):
    """
    This class inherits from standard class, but allows ovewrite of fields in messages
    """    
    extra_email_context = {}
    extra_email_context['site_name'] = settings.MY_SITE
    extra_email_context['domain'] = settings.MY_DOMAIN

