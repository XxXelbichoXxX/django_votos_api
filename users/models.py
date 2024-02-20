from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(max_length=30, unique=True)
    #nombre = models.CharField(max_length=50, null=True, blank=True)
    workstation = models.CharField(max_length=100, null=True, blank=True)
    dependency = models.CharField(max_length=100, null=True, blank=True)
    rank = models.IntegerField(null=True, blank=True)
    #edad = models.IntegerField( null=True, blank=True)
    antiquity = models.IntegerField(null=True, blank=True)
    image = models.CharField(max_length=100, null=True, blank=True)


    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []