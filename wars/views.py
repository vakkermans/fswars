from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponse, \
    HttpResponseNotAllowed, HttpResponseRedirect
from utils.web import rtr, rurl
from forms import *
from django.views.decorators.csrf import csrf_exempt
from models import *
from django.contrib import messages
import json, datetime
#import cachedb

SESSION_NICKNAME = 'session_nickname'

#def pick_name(request):
#    if SESSION_NICKNAME in request.session and cachedb.user_exists_p(request.session[SESSION_NICKNAME]):
#        if cachedb.player_present(1) and cachedb.player_present(2):
#            messages.add_message(request, messages.INFO, 'Already 2 players playing.')
#            return rtr('wars/pick_name.html')
#        else:
#            return HttpResponseRedirect(rurl('wars:pick-sounds'))
#    form = PickNameForm()
#    if request.method == 'POST':
#        form = PickNameForm(request.POST)
#        if form.is_valid():
#            nickname = form.cleaned_data['nickname']
#            if cachedb.user_exists_p(nickname):
#                messages.add_message(request, messages.INFO, 'Pick another nickname, this one is already taken.')
#                return rtr('wars/pick_name.html')
#            request.session[SESSION_NICKNAME] = form.cleaned_data['nickname']
#            cachedb.add_user(nickname)
#            if cachedb.player_present(1):
#                cachedb.set_player(1, nickname)
#            else:
#                cachedb.set_player(2, nickname)
#            return HttpResponseRedirect(rurl('wars:pick-sounds'))
#    return rtr('wars/pick_name.html')

def players_present():
    player1 = True if FSWUser.objects.filter(player_number=1).count() > 0 else False
    player2 = True if FSWUser.objects.filter(player_number=2).count() > 0 else False
    return player1, player2


def pick_name(request):
    if SESSION_NICKNAME in request.session:
        # check if user is playing
        try:
            user = FSWUser.objects.get(nickname = request.session[SESSION_NICKNAME])
            if user.player_number != 0:
                return HttpResponseRedirect(rurl('wars:pick-sounds'))
            else:
                player1, player2 = players_present()
                if player1 and player2:
                    messages.add_message(request, messages.INFO, 'There are already 2 players.')
                    return rtr('wars/pick_name.html')
                user.player_number = (1 if player2 else 2)
                user.save()
        except FSWUser.DoesNotExist:
            del request.session[SESSION_NICKNAME]

    # user doens't have session
    form = PickNameForm()
    if request.method == 'POST':
        form = PickNameForm(request.POST)
        if form.is_valid():
            nickname = form.cleaned_data['nickname']
            # if user already exists
            user, created = FSWUser.objects.get_or_create(nickname=nickname)
            #nickname = request.session[SESSION_NICKNAME]
            if not created:
                if datetime.datetime.now() - user.modified > datetime.timedelta(days=1):
                    pass
                else:
                    messages.add_message(request, messages.INFO, 'Pick another nickname, this one is already taken.')
                    return rtr('wars/pick_name.html')
            request.session[SESSION_NICKNAME] = nickname
            # N.B.! copied from above, DRY it out
            player1, player2 = players_present()
            if player1 and player2:
                messages.add_message(request, messages.INFO, 'There are already 2 players.')
                return rtr('wars/pick_name.html')
            user.player_number = (1 if player2 else 2)
            user.save()
            return HttpResponseRedirect(rurl('wars:pick-sounds'))
    return rtr('wars/pick_name.html')

@csrf_exempt
def pick_sounds(request):
    # username = request.SESSION['username']
    if request.method == 'POST':
        print "post"
        
        return rtr('wars/pick_sounds.html')
    else:
        return rtr('wars/pick_sounds.html')
