from django.db import models
from django.utils import timezone
class Vote(models.Model):
    voteId = models.AutoField(primary_key=True)        
    empVoterIdFK = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='Voter')
    empCandidateIdFK = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='Candidate')
    rangeIdFK = models.ForeignKey('range.Range', on_delete=models.SET_NULL, null=True, blank=True)
    stageIdFK = models.ForeignKey('stage.Stage', on_delete=models.SET_NULL, null=True, blank=True)
    voteDate = models.DateTimeField(auto_now=True)
    period = models.CharField(max_length=4, blank=True)
    revocationStatus = models.BooleanField(default=False, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Extraer el año de la fecha actual
        current_year = timezone.now().year
        # Convertir el año a una cadena de texto
        self.period = str(current_year)
        # Llamar al método save() del modelo base para guardar el objeto
        super().save(*args, **kwargs)