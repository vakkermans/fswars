# -*- coding: utf-8 -*-
from django.contrib import admin
from models import Battle

class BattleAdmin(admin.ModelAdmin):
    list_display = ("player1", "player2", "player1_sounds", "player2_sounds", "finished")
admin.site.register(Battle, BattleAdmin)
