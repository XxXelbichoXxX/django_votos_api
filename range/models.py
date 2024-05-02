from django.db import models

class Range(models.Model):
    rangeId = models.AutoField(primary_key=True)
    rangeName = models.CharField(max_length=128, unique=True)
