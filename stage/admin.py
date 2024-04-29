from django.contrib import admin
from stage.models import Etapa

@admin.register(Etapa)
class EtapaAdmin(admin.ModelAdmin):
    pass