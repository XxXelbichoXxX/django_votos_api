from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from range.models import Range
from range.api.serializers import RangeSerializer


class RangeApiViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Range.objects.all()
    serializer_class = RangeSerializer