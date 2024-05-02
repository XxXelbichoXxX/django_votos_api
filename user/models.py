import random
from django.db import models


from django.contrib.auth.models import AbstractUser

def setRandId():
    return random.randint(100000, 999999)
class User(AbstractUser):
    id = models.CharField(max_length=30, primary_key=False, auto_created=True, null=True, blank=True)
    username = models.CharField(max_length=30, unique=True, primary_key=True)
    dependencyId = models.ForeignKey('dependency.Dependency', on_delete=models.SET_NULL, null=True, blank=True)
    workstation = models.CharField(max_length=100, null=True, blank=True)
    rankIdFk = models.ForeignKey('range.Range', on_delete=models.SET_NULL, null=True, blank=True)
    antiquity = models.IntegerField(null=True, blank=True)
    isAdmin = models.BooleanField(default=False, null=True, blank=True)
    image = models.ImageField(upload_to='user', null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = self.username+str(setRandId())
        super().save(*args, **kwargs)


    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []