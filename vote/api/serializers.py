from rest_framework.serializers import ListSerializer
from rest_framework.serializers import ModelSerializer
from vote.models import Vote

class VoteSerializer(ModelSerializer):
    class Meta:
        model = Vote
        fields = ['voteId', 'empVoterIdFK', 'empCandidateIdFK', 'rangeIdFK', 'stageIdFK', 'voteDate', 'period', 'revocationStatus']


class VoteListSerializer(ListSerializer):
    def create(self, validated_data):
        votes = [Vote(**item) for item in validated_data]
        return Vote.objects.bulk_create(votes)