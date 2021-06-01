import os, time

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404, render, redirect
#from django.http import Http404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic.edit import CreateView
from django.forms.models import inlineformset_factory
from django.conf import settings
from django.core.exceptions import PermissionDenied

from django.contrib.auth.models import User

from ddws.hardcode import *

from doomday.forms import UpdateForm

from ddgui.models import Ddevent
from ddgui.forms import DoomDayEventForm
from ddgui.hardcode import *


@login_required
@user_passes_test(lambda uu: uu.is_superuser)
def ddgui_initial(request):
    """
    Right now it's a superuser page: .../ddgui/
    """
    userlist_ids = []    
    temp_var = list(User.objects.all().values_list('username'))
    for ii in temp_var:
        userlist_ids.append(str(ii[0]))
    context = {'page_title': 'Superuser page',
               'all_users': userlist_ids,}
    return render(request, 'ddgui/initial.html', context)

@login_required
def ddgui_user(request): 
    """
    Displays user information: .../ddgui/user/
    """   
    user_id = request.user.id
    if request.user.is_authenticated:
        try:
            ws_user=get_object_or_404(User, pk=user_id)
            temp_user = ws_user.first_name 
        except:
            temp_user = ''
        context={
            'page_title': DDGUI_USER_PAGE_TITLE,
            'username':temp_user,
        }
        return render(request, 'ddgui/user.html', context)
    else:
        raise PermissionDenied

@login_required
def ddgui_new_doom_event_form(request):
    """
    Displays the DoomDay form for new event: .../ddgui/user/doom_event_form/new/ 
    """
    user_id = request.user.id
    user = User.objects.get(pk=user_id)
    user_form = UpdateForm(instance=user)
    DdguiDoomEventFormset = inlineformset_factory(User, Ddevent, 
                                                    form=DoomDayEventForm, 
                                                    can_delete=False, 
                                                    extra=1)
    formset = DdguiDoomEventFormset(instance=None)
    if request.method == "GET": 
        return render(
            request, "ddgui/doom_event_form.html",
            {"form": user_form,
            "formset": formset,
            }
        )
    elif request.method == "POST":
        user_form = UpdateForm(request.POST, request.FILES, instance=user)       
        if user_form.is_valid():
            author = user_form.save(commit=False)
            formset = DdguiDoomEventFormset(request.POST, request.FILES, instance=author)
            if formset.is_valid():
                    formset.save()
                    return HttpResponseRedirect('/ddredirect/success/')
            return redirect(reverse('ddgui:ddgui_user'))

@login_required
def ddgui_edit_doom_events_form(request):
    """
    Displays the DoomDay form for all events: .../ddgui/user/doom_event_form/edit/ 
    """
    user_id = request.user.id
    user = User.objects.get(pk=user_id)
    user_form = UpdateForm(instance=user)
    DdguiDoomEventFormset = inlineformset_factory(User, Ddevent, 
                                                    form=DoomDayEventForm, 
                                                    can_delete=True, 
                                                    extra=0)
    formset = DdguiDoomEventFormset(instance=user)   
    
    if request.method == "GET": 
        return render(
            request, "ddgui/doom_event_form.html",
            {"form": user_form,
            "formset": formset,
            }
        )
    elif request.method == "POST":
        user_form = UpdateForm(request.POST, request.FILES, instance=user)       
        if user_form.is_valid():
            author = user_form.save(commit=False)
            formset = DdguiDoomEventFormset(request.POST, request.FILES, instance=author)                
            if formset.is_valid():
                
                #remove previously uploaded files: 
                if request.FILES:                        
                    try:
                        for temp_var in Ddevent.objects.filter(author_id=user_id).values('doomfile'):
                            print(temp_var)
                            for k, v in temp_var.items():
                                if v!='': os.remove(os.path.join(settings.MEDIA_ROOT, v))
                    except:
                        pass
                
                formset.save()
                return HttpResponseRedirect('/ddredirect/success/')
            return redirect(reverse('ddgui:ddgui_user'))
