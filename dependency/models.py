from django.db import models

class Dependency(models.Model):
    dependencyId = models.AutoField(primary_key=True)
    dependencyName = models.CharField(max_length=128, unique=True)
    owner = models.CharField(max_length=128, unique=False)
    address = models.CharField(max_length=128, unique=False)
    phone = models.CharField(max_length=20, unique=False)
    page = models.CharField(max_length=128, unique=False)
    logo = models.ImageField(upload_to='dependency', null=True, blank=True)