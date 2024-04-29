from django.contrib import admin
from range.models import Rango

@admin.register(Rango)
class RangoAdmin(admin.ModelAdmin):
    pass