from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponse, \
    HttpResponseNotAllowed, HttpResponseRedirect
from utils.web import rtr, rurl
from forms import *

def pick_name(request):
    form = PickNameForm()
    if request.method == 'POST':
        form = PickNameForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect(rurl('wars:pick-sounds'))
    return rtr('wars/pick_name.html')

def pick_sounds(request):
    return rtr('wars/pick_sounds.html')
