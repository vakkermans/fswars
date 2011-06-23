from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from utils.comet import send_message
#from django.core import serializers
import json


class Battle(models.Model):
    player1             = models.CharField(max_length=32)
    player1_uuid        = models.CharField(max_length=64)
    player2             = models.CharField(max_length=32, null=True)
    player2_uuid        = models.CharField(max_length=64, null=True)
    player1_sounds      = models.CharField(max_length=512, null=True) # json dumped list of ints
    player2_sounds      = models.CharField(max_length=512, null=True)
    num_rounds          = models.IntegerField(default=5)
    turn_owner          = models.IntegerField(default=1)
    finished            = models.BooleanField()

    def status_players(self):
        return self.player1 and self.player2

    def status_sounds(self):
        return self.player1_sounds and self.player2_sounds

#    def to_json(self):
#        return serializers.serialize('json', [self])

    def json_safe(self):
        data = {'id': self.id}
        for field in ['player1', 'player1_uuid', 'player2', 'player2_uuid',
                      'num_rounds', 'turn_owner', 'finished']:
            data[field] = getattr(self, field)
        data['player1_sounds'] = json.loads(self.player1_sounds) if self.player1_sounds else []
        data['player2_sounds'] = json.loads(self.player2_sounds) if self.player2_sounds else []
        data['rounds'] = [round.json_safe() for round in self.rounds.order_by('id')]
#        data['rounds'] = [round.json_safe() for round in \
#                          BattleRound.objects.filter(battle=self).order_by('-id')]
        return data

    def to_json(self):
        return json.dumps(self.json_safe())

    def send_update_battle_status(self):
        send_message(self.id, '{"command": "updateBattleStatus", "battle": %s }' % self.to_json(), True)


class BattleRound(models.Model):
    attacker            = models.IntegerField()
    player1_sound       = models.IntegerField()
    player2_sound       = models.IntegerField()
    winner              = models.IntegerField()
    # Just in case we change the scoring model.
    player1_points      = models.IntegerField(default=0)
    player2_points      = models.IntegerField(default=0)
    preset              = models.CharField(max_length=128)
    battle              = models.ForeignKey(Battle, related_name='rounds')

    def json_safe(self):
        data = {}
        for field in ['attacker', 'player1_sound', 'player2_sound', 'winner',
                      'player1_points', 'player2_points']:
            data[field] = getattr(self, field)
        return data


@receiver(post_save, sender=Battle)
def send_update(**kwargs):
    battle = kwargs['instance']
    battle.send_update_battle_status()
