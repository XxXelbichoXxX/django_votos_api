from django.db import models
import os

class Dependency(models.Model):
    dependencyId = models.AutoField(primary_key=True)
    dependencyName = models.CharField(max_length=128, unique=True)
    owner = models.CharField(max_length=128, unique=False)
    address = models.CharField(max_length=128, unique=False)
    phone = models.CharField(max_length=20, unique=False)
    page = models.CharField(max_length=128, unique=False)
    logo = models.ImageField(upload_to='dependency', null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.dependencyId:
            if self.logo:
                old_logo = Dependency.objects.get(pk=self.pk)
                if old_logo.logo and os.path.isfile(old_logo.logo.path):
                    os.remove(old_logo.logo.path)
        super().save(*args, **kwargs)