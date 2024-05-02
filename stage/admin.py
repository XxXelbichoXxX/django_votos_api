from django.contrib import admin
from stage.models import Stage

@admin.register(Stage)
class StageAdmin(admin.ModelAdmin):
    pass