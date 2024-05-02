from django.contrib import admin
from dependency.models import Dependency

@admin.register(Dependency)
class DependencyAdmin(admin.ModelAdmin):
    pass