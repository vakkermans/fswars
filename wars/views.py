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

class auth():

    def __call__(self, f):
        """
        If there are decorator arguments, __call__() is only called
        once, as part of the decoration process! You can only give
        it a single argument, which is the function object.
        """
        def authed_func(request, *args, **kargs):
            nickname = request.session.get(SESSION_NICKNAME, False)

            if not nickname:
                return HttpResponseRedirect(rurl('wars:pick-name'))

            try:
                request.user = FSWUser.objects.get(nickname=nickname)
                return f(request, *args, **kargs)
            except FSWUser.DoesNotExist:
                del request.session[SESSION_NICKNAME]
                messages.add_message(request, messages.INFO, 'Please pick a username')
                return HttpResponseRedirect(rurl('wars:pick-name'))

        return authed_func




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

def delete_users(request):
    FSWUser.objects.all().delete()
    return HttpResponseRedirect(rurl('frontpage'))

@auth()
def battle(request):
    return HttpResponse(str(request))


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
                user.player_number = 0
                user.save()
            player1, player2 = players_present()
            if player1 and player2:
                messages.add_message(request, messages.INFO, 'There are already 2 players.')
                return rtr('wars/pick_name.html')
            user.player_number = (1 if player2 else 2)
            user.save()
            return HttpResponseRedirect(rurl('wars:pick-sounds'))
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

@auth()
@csrf_exempt
def pick_sounds(request):
    nickname = request.session[SESSION_NICKNAME]
    form = PickSoundsForm()
    if request.method == 'POST':
        form = PickSoundsForm(request.POST)
        if form.is_valid():
            sound_id = int(form.cleaned_data['sound_ids'])
            user = FSWUser.objects.get(nickname=nickname)
            user.sounds = json.dumps([sound_id])
            user.save()
            return HttpResponseRedirect(rurl('wars:battle'))
    return rtr('wars/pick_sounds.html')
