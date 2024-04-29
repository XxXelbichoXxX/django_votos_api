from django.db import models

class Rango(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128, unique=True)
