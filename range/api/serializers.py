from rest_framework.serializers import ModelSerializer
from range.models import Range


class RangeSerializer(ModelSerializer):
    class Meta:
        model = Range
        fields = ['rangeId', 'rangeName']