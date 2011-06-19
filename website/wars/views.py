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
import json, uuid
from algorithms import algorithms
from django.core import serializers
from utils.comet import send_message
from django.views.decorators.http import require_GET, require_POST

SESSION_NICKNAME = 'session_nickname'
SESSION_UUID = 'session_uuid'

from algorithms import algorithms
algorithms.init()

class auth():

    def __init__(self, check_nickname=True):
        self.check_nickname = check_nickname

    def __call__(self, f):
        """
        If there are decorator arguments, __call__() is only called
        once, as part of the decoration process! You can only give
        it a single argument, which is the function object.
        """
        def authed_func(request, *args, **kargs):

            nickname = request.session.get(SESSION_NICKNAME, False)
            pl_uuid = request.session.get(SESSION_UUID, str(uuid.uuid4()))

            request.session[SESSION_UUID] = pl_uuid

            if self.check_nickname and not nickname:
                return HttpResponseRedirect(rurl('wars:frontpage'))

            request.user = nickname
            request.uuid = pl_uuid
            return f(request, *args, **kargs)

        return authed_func


@auth(check_nickname=False)
def frontpage(request):
    form = PickNameForm()
    if request.method == 'POST':
        form = PickNameForm(request.POST)
        if form.is_valid():
            nickname = form.cleaned_data['nickname']
            request.session[SESSION_NICKNAME] = nickname
            battle = Battle()
            battle.player1_uuid = request.uuid
            battle.player1 = nickname
            battle.save()
            return HttpResponseRedirect(rurl('wars:wait-on-player', battle.id))
    return rtr('wars/frontpage.html')


@auth(check_nickname=False)
def wait_on_player(request, battle_id):
    battle = get_object_or_404(Battle, id=battle_id)
    player_is_creator = battle.player1_uuid == request.uuid
    form = PickNameForm()
    if request.method == 'POST':
        form = PickNameForm(request.POST)
        if form.is_valid():
            # N.B. TODO: prevent people from stealing the game by checking if player2 is already set.
            nickname = form.cleaned_data['nickname']
            request.session[SESSION_NICKNAME] = nickname
            battle.player2_uuid = request.uuid
            battle.player2 = nickname
            battle.save()
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
    battle_json = battle.to_json()
    my_nickname = request.session[SESSION_NICKNAME];
    presets = algorithms.ALGORITHM_CLASSES.keys()

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
def battle_status(request, battle_id):
    battle = get_object_or_404(Battle, id=battle_id)
    return HttpResponse(battle.do_json())


@auth()
def battle_result(request, battle_id):
    battle = get_object_or_404(Battle, id=battle_id)
    history = json.loads(battle.history) if battle.history and battle.history != '' else []
    scores = calculate_final_scores(history)
    return rtr('wars/battle_result.html')



@require_POST
def update_battle(request, battle_id):
    form = UpdateBattleForm(request.POST)
    if form.is_valid():
        send_message(battle_id, form.cleaned_data['update'])
        return HttpResponse('updating through comet..')
    else:
        return HttpResponse('update form was not valid..')
