from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from stage.models import Etapa
from stage.api.serializers import EtapaSerializer


class EtapaApiViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Etapa.objects.all()
    serializer_class = EtapaSerializer