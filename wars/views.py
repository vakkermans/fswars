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
from django.core import serializers

SESSION_NICKNAME = 'session_nickname'

from algorithms import algorithms
algorithms.init()

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
            sound_ids = [int(x) for x in form.cleaned_data.get('sound_ids').split(',')]
            if battle.player1 == request.user:
                battle.player1_sounds = json.dumps(sound_ids)
            else:
                battle.player2_sounds = json.dumps(sound_ids)
            battle.save()
            return HttpResponseRedirect(rurl('wars:wait-on-sounds', battle.id))
    return rtr('wars/pick_sounds.html')


@auth()
def battle(request, battle_id):
    battle = get_object_or_404(Battle, id=battle_id)
    battle_json = battle.do_json()
    return rtr('wars/battle.html')


@auth()
def wait_on_sounds(request, battle_id):
    battle = get_object_or_404(Battle, id=battle_id)
    if battle.status_sounds():
        return HttpResponseRedirect(rurl('wars:battle', battle.id))
    return rtr('wars/wait_on_sounds.html')


#def compute(request, id1, id2, preset):
#    ps = preset.upper()
#    if ps not in algorithms.ALGORITHM_CLASSES:
#        print 'ARG, not a valid preset'
#    return HttpResponse(json.dumps(algorithms.computeBattle(int(id1),
#                                                            int(id2),
#                                                            algorithms.ALGORITHM_CLASSES[ps])))


@auth()
def fight(request, battle_id, id1, id2, preset):
    battle = get_object_or_404(Battle, id=battle_id)
    ps = preset.upper()
    battle_result = algorithms.computeBattle(int(id1), int(id2), algorithms.ALGORITHM_CLASSES[ps])
    history = json.loads(battle.history) if battle.history else []
    history.append([int(id1), int(id2), ps, battle_result['winner'], battle_result['points']])
    battle.history = json.dumps(history)
    # N.B. player1 always starts! 1-indexed, so 1 or 2
    battle.turn_owner = 2 if len(history) % 2 == 1 else 1
    if len(history) >= len(json.loads(battle.player1_sounds)) or \
       len(history) >= len(json.loads(battle.player2_sounds)):
        battle.finished = True
    battle.save()
    return HttpResponse(battle.do_json())


def calculate_final_scores(history):
    player1 = 0
    player2 = 0
    for i in range(len(history)):
        if history[i][3] == 1:
            player1 += history[i][4]
        else:
            player2 += history[i][4]
    return player1, player2



@auth()
def battle_result(request, battle_id):
    battle = get_object_or_404(Battle, id=battle_id)
    history = json.loads(battle.history) if battle.history and battle.history != '' else []
    scores = calculate_final_scores(history)
    return rtr('wars/battle_result.html')

