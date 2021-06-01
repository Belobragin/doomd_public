"""
views.py module for dnews app
"""

import os
import time
import json

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView

from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin, AccessMixin
from django.contrib.messages import get_messages
from django.conf import settings

from django.views import View
from django.views.generic import TemplateView, ListView, DetailView

#from django.contrib.auth.models import User

from ddws.hardcode import ERR_REDIR,\
                          TEST_TEMPLATE, DASHBOARD

from dnews.hardcode import *
from dnews.models import Ddnews


class DnewsInitialView(ListView):
    """
    view for '' path - main news page
    """
    template_name = ALL_NEWS_LIST_TEMPLATE
    context_object_name = 'latest_news_list'

    def get_queryset(self):
        """Return the last five news."""
        return Ddnews.objects.order_by('-release_date')[:5]

class DnewsDetailsView(DetailView):
    """
    view the body of the news
    """
    model = Ddnews
    template_name = MY_NEWS_LIST_TEMPLATE

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['mynews'] = Ddnews.objects.filter(id = )
    #     return context