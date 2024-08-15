from django.contrib import admin
from forgetPasswordRequest.models import ForgetPasswordRequest

@admin.register(ForgetPasswordRequest)
class ForgetPasswordRequestAdmin(admin.ModelAdmin):
    pass