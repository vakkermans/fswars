from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

class FSWUser(models.Model):
    nickname            = models.CharField(max_length=32, db_index=True, unique=True)
    sounds              = models.CharField(max_length=1024, db_index=False)
    player_number       = models.IntegerField(default=0)
    modified            = models.DateTimeField(auto_now=True)

