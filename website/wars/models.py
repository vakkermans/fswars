from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from utils.comet import send_message
from django.core import serializers


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

    def to_json(self):
        return serializers.serialize('json', [self])

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
    battle              = models.ForeignKey(Battle, related_name='rounds')

@receiver(post_save, sender=Battle)
def send_update(**kwargs):
    battle = kwargs['instance']
    battle.send_update_battle_status()
    
