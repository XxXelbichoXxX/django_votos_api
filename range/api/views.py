from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from range.models import Rango
from range.api.serializers import RangoSerializer


class RangoApiViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Rango.objects.all()
    serializer_class = RangoSerializer