from django.db import models

class Etapa(models.Model):
    id = models.AutoField(primary_key=True)
    num_etapa = models.IntegerField(null=True, blank=True)
    nombre_etapa = models.CharField(max_length=100, null=True, blank=True)
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_fin = models.DateField(null=True, blank=True)
