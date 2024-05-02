from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from dependency.models import Dependency
from dependency.api.serializers import DependencySerializer


class DependencyApiViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Dependency.objects.all()
    serializer_class = DependencySerializer