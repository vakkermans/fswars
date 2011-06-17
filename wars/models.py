from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
import json

#class FSWUser(models.Model):
#    nickname            = models.CharField(max_length=32, db_index=True, unique=True)
#    sounds              = models.CharField(max_length=1024, db_index=False)
#    player_number       = models.IntegerField(default=0)
#    modified            = models.DateTimeField(auto_now=True)

class Battle(models.Model):
    player1             = models.CharField(max_length=32)
    player2             = models.CharField(max_length=32, null=True)
    player1_sounds      = models.CharField(max_length=512, null=True) # json dumped list of ints
    player2_sounds      = models.CharField(max_length=512, null=True)
    turn_owner          = models.IntegerField(default=1)
    history             = models.CharField(max_length=2048) # json dumped history
    finished            = models.BooleanField()

    def status_players(self):
        return self.player1 and self.player2

    def status_sounds(self):
        return self.player1_sounds and self.player2_sounds

    def status(self):
        return json.dumps(self)
    
    def do_json(self):
        data = {}
        data['player1'] = self.player1
        data['player2'] = self.player2
        data['player1_sounds'] = self.player1_sounds
        data['player2_sounds'] = self.player2_sounds
        data['turn_owner'] = self.turn_owner
        data['history'] = self.history
        data['finished'] = self.finished
        
        return json.dumps(data)
