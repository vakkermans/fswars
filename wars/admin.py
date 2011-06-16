# -*- coding: utf-8 -*-
from django.contrib import admin
from models import FSWUser

class FSWUserAdmin(admin.ModelAdmin):
    list_display = ("nickname", "player_number", "sounds")

admin.site.register(FSWUser, FSWUserAdmin)
