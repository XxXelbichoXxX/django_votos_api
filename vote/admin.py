from django.contrib import admin
from vote.models import Voto

@admin.register(Voto)
class VoteAdmin(admin.ModelAdmin):
    pass