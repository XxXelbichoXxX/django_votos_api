from rest_framework.serializers import ModelSerializer
from stage.models import Stage


class StageSerializer(ModelSerializer):
    class Meta:
        model = Stage
        fields = ['stageId','dependencyIdFK', 'stageName', 'startDate', 'endDate']