from django.db import models

class Stage(models.Model):
    stageId = models.AutoField(primary_key=True)
    dependencyIdFK = models.ForeignKey('dependency.Dependency', on_delete=models.CASCADE , null=True, blank=True)
    stageName = models.CharField(max_length=100, null=True, blank=True)
    startDate = models.DateField(null=True, blank=True)
    endDate = models.DateField(null=True, blank=True)
