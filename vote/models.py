from django.db import models

class Vote(models.Model):
    voteId = models.AutoField(primary_key=True)        
    empVoterIdFK = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='Voter')
    empCandidateIdFK = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='Candidate')
    rangeIdFK = models.ForeignKey('range.Range', on_delete=models.SET_NULL, null=True, blank=True)
    stageIdFK = models.ForeignKey('stage.Stage', on_delete=models.SET_NULL, null=True, blank=True)
    voteDate = models.DateTimeField(auto_now=True)
    revocationStatus = models.BooleanField(default=False, null=True, blank=True)

