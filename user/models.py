from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(max_length=30, unique=True, primary_key=True)
    dependencyId = models.ForeignKey('dependency.Dependency', on_delete=models.SET_NULL, null=True, blank=True)
    workstation = models.CharField(max_length=100, null=True, blank=True)
    rankIdFk = models.ForeignKey('range.Range', on_delete=models.SET_NULL, null=True, blank=True)
    antiquity = models.IntegerField(null=True, blank=True)
    isAdmin = models.BooleanField(default=False, null=True, blank=True)
    image = models.ImageField(upload_to='user', null=True, blank=True)


    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []