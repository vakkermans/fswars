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
import json
from algorithms import algorithms

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
                return HttpResponseRedirect(rurl('wars:frontpage'))

            request.user = nickname
            return f(request, *args, **kargs)

        return authed_func


def frontpage(request):
    form = PickNameForm()
    if request.method == 'POST':
        form = PickNameForm(request.POST)
        if form.is_valid():
            nickname = form.cleaned_data['nickname']
            request.session[SESSION_NICKNAME] = nickname
            try:
                battle = Battle.objects.get(player2=None)
                battle.player2 = nickname
            except Battle.DoesNotExist:
                battle = Battle(player1=nickname)
                battle.save()
            return HttpResponseRedirect(rurl('wait-on-player', battle.id))
    return rtr('wars/frontpage.html')


@auth()
def wait_on_player(request, battle_id):
    battle = get_object_or_404(Battle, id=battle_id)
    if battle.status_players():
        return HttpResponseRedirect(rurl('pick-sounds', battle.id))
    return rtr('wars/wait_on_player.html')


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
def waiting_queue(request):
    player1, player2 = players_present()
    if player1 and player2:
        return HttpResponseRedirect(rurl('wars:battle'))
    else:
        return rtr('wars/queue.html')

@auth()
def compute(request, id1, id2, preset):
    ps = preset.upper()
    if ps not in algorithms.ALGORITHM_CLASSES:
        print 'ARG, not a valid preset'
    return HttpResponse(json.dumps(algorithms.computeBattle(int(id1),
                                                            int(id2),
                                                            algorithms.ALGORITHM_CLASSES[ps])))


@auth()
def battle(request):
    algorithms.init()
    user = FSWUser.objects.get(nickname = request.session[SESSION_NICKNAME])
    player1 = FSWUser.objects.get(player_number=1)
    player2 = FSWUser.objects.get(player_number=2)
    p1_sound = json.loads(player1.sounds)[0]
    p2_sound = json.loads(player2.sounds)[0]

    return rtr('wars/battle.html')


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
            return HttpResponseRedirect(rurl('wars:queue'))
    return rtr('wars/pick_sounds.html')
