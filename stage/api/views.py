from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from stage.models import Stage
from stage.api.serializers import StageSerializer


class StageApiViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Stage.objects.all()
    serializer_class = StageSerializer