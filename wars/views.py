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
            try:
                battle = Battle.objects.get(player2__isnull=True)
                nickname = nickname+'2' if battle.player1 == nickname else nickname
                battle.player2 = nickname
                battle.save()
            except Battle.DoesNotExist:
                battle = Battle(player1=nickname)
                battle.save()
            request.session[SESSION_NICKNAME] = nickname
            return HttpResponseRedirect(rurl('wars:wait-on-player', battle.id))
    return rtr('wars/frontpage.html')


@auth()
def wait_on_player(request, battle_id):
    battle = get_object_or_404(Battle, id=battle_id)
    if battle.status_players():
        return HttpResponseRedirect(rurl('wars:pick-sounds', battle.id))
    return rtr('wars/wait_on_player.html')


@auth()
@csrf_exempt
def pick_sounds(request, battle_id):
    battle = get_object_or_404(Battle, id=battle_id)
    form = PickSoundsForm()
    if request.method == 'POST':
        form = PickSoundsForm(request.POST)
        if form.is_valid():
            sound_ids = form.cleaned_data.get('sound_ids',[])
            if battle.player1 == request.user:
                battle.player1_sounds = json.dumps(sound_ids)
            else:
                battle.player2_sounds = json.dumps(sound_ids)
            battle.save()
            return HttpResponseRedirect(rurl('wars:wait-on-sounds', battle.id))
    return rtr('wars/pick_sounds.html')


@auth()
def battle(request, battle_id):
    return rtr('wars/battle.html')


@auth()
def wait_on_sounds(request, battle_id):
    battle = get_object_or_404(Battle, id=battle_id)
    if battle.status_sounds():
        return HttpResponseRedirect(rurl('wars:battle', battle.id))
    return rtr('wars/wait_on_sounds.html')


def compute(request, id1, id2, preset):
    ps = preset.upper()
    if ps not in algorithms.ALGORITHM_CLASSES:
        print 'ARG, not a valid preset'
    return HttpResponse(json.dumps(algorithms.computeBattle(int(id1),
                                                            int(id2),
                                                            algorithms.ALGORITHM_CLASSES[ps])))


#@auth()
#def battle(request):
#    algorithms.init()
#    user = FSWUser.objects.get(nickname = request.session[SESSION_NICKNAME])
#    player1 = FSWUser.objects.get(player_number=1)
#    player2 = FSWUser.objects.get(player_number=2)
#    p1_sound = json.loads(player1.sounds)[0]
#    p2_sound = json.loads(player2.sounds)[0]
#
#    return rtr('wars/battle.html')


#def players_present():
#    player1 = True if FSWUser.objects.filter(player_number=1).count() > 0 else False
#    player2 = True if FSWUser.objects.filter(player_number=2).count() > 0 else False
#    return player1, player2



