from django.contrib import admin
from range.models import Range

@admin.register(Range)
class RangeAdmin(admin.ModelAdmin):
    pass