from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from stage.models import Stage
from stage.api.serializers import StageSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.db import transaction
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi



class StageApiViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Stage.objects.all()
    serializer_class = StageSerializer

        # Peticion para obtener las etapas acorde a una dependencia
    @swagger_auto_schema(
    manual_parameters=[
        openapi.Parameter('dependencyIdFK', openapi.IN_QUERY, description="Id de la dependencia a la que pertenencen", type=openapi.TYPE_INTEGER),
    ],
    responses={200: StageSerializer(many=True)},
    )
    @action(detail=False, methods=['GET'])
    def getStagesByDependency(self, request):
        """
        Obtiene todas las etapas correspondientes a una dependencia.

        ---
        # Parámetros:
        - dependencyIdFK: Id de la dependencia.
        
        # Retorna:
        - una lista de todas las etapas correspondientes a la dependencia.
        """
        dependencyIdFK = request.query_params.get('dependencyIdFK')

        filters = {}

        if dependencyIdFK:
            filters['dependencyIdFK'] = dependencyIdFK
            
        stages = (
            Stage.objects
            .filter(**filters)
            .values(
                "stageId",
                "dependencyIdFK",
                "stageName",
                "startDate",
                "endDate"          
            )
        )
        
        return Response(stages, status=status.HTTP_200_OK)
    
