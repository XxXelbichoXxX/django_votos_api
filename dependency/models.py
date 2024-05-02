from django.db import models

class Dependency(models.Model):
    dependencyId = models.AutoField(primary_key=True)
    dependencyName = models.CharField(max_length=128, unique=True)
    owner = models.CharField(max_length=128, unique=True)
    address = models.CharField(max_length=128, unique=True)
    phone = models.CharField(max_length=20, unique=True)
    logo = models.CharField(max_length=20, unique=True)
    image = models.ImageField(upload_to='dependency', null=True, blank=True)