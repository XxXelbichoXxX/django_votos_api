import random
from django.db import models
import os


from django.contrib.auth.models import AbstractUser

def setRandId():
    return random.randint(100000, 999999)
class User(AbstractUser):
    id = models.CharField(max_length=30, primary_key=False, auto_created=True, null=True, blank=True)
    username = models.CharField(max_length=30, unique=True, primary_key=True)
    dependencyIdFK = models.ForeignKey('dependency.Dependency', on_delete=models.SET_NULL, null=True, blank=True)
    workstation = models.CharField(max_length=100, null=True, blank=True)
    rangeIdFK = models.ForeignKey('range.Range', on_delete=models.SET_NULL, null=True, blank=True)
    antiquity = models.IntegerField(null=True, blank=True)
    isAdmin = models.BooleanField(default=False, null=True, blank=True)
    image = models.ImageField(upload_to='user', null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = self.username+str(setRandId())
        elif self.id:
            if self.image:
                old_image = User.objects.get(pk=self.pk)
                if old_image.image and os.path.isfile(old_image.image.path):
                    os.remove(old_image.image.path)
        super().save(*args, **kwargs)


    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []