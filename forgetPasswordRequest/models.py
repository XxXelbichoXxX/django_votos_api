from django.db import models
import os

class ForgetPasswordRequest(models.Model):
    requestId = models.AutoField(primary_key=True)
    username = models.CharField(max_length=128, unique=False)
    email = models.CharField(max_length=128, unique=False)
    code = models.CharField(max_length=128, unique=False)
    useCode = models.BooleanField(default=False)