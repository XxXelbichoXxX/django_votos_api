from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from dependency.models import Dependency
from dependency.api.serializers import DependencySerializer
from django.db import transaction
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action


class DependencyApiViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Dependency.objects.all()
    serializer_class = DependencySerializer

    @action(detail=False, methods=['POST'])
    def createMassiveDependency(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    # Itera sobre los datos y crea un objeto User para cada conjunto de datos
                    for data in serializer.validated_data:
                        Dependency.objects.create(**data)
            except Exception as e:
                # Si ocurre un error, puedes manejarlo aquí, por ejemplo, devolviendo un error 500
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)