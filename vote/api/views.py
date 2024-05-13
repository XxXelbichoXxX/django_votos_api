from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from vote.models import Vote
from vote.api.serializers import VoteSerializer

#Otras importaciones para las consultas
from rest_framework.decorators import action
from django.db import models
from django.db.models import Count, F, Value, CharField, Func
from django.db.models.functions import Concat, TruncYear, TruncDate
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class VoteApiViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer

#-------------------------------------------------------------------------------------------------------------------
    #Peticion para crear votos de forma masiva
    @action(detail=False, methods=['POST'])
    def createMassiveVotes(self, request, *args, **kwargs):
        """
        Crea votos de forma masiva.

        Permite crear votos en grandes cantidades proporcionando una lista de datos de votos.
        ---
        # Parámetros
        - Se espera una solicitud POST con una lista de datos de votos.
        - Cada dato de voto debe tener el formato requerido por el serializador VoteSerializer.

        # Retorna
        - En caso de éxito, retorna una respuesta con los datos de los votos creados y el código de estado 201 (Created).
        - En caso de error, retorna los errores de validación con el código de estado 400 (Bad Request).
        """
        # Utiliza el serializador VoteSerializer en lugar de VoteListSerializer
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        if serializer.is_valid():
            # Itera sobre los datos y crea un objeto Vote para cada conjunto de datos
            for data in serializer.validated_data:
                Vote.objects.create(**data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#-------------------------------------------------------------------------------------------------------------------
    #Peticion para obtener el total de votos por rango , etapa y fecha (fecha es el año)
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('stageIdFK', openapi.IN_QUERY, description="Número de etapa", type=openapi.TYPE_STRING),
            openapi.Parameter('rangeIdFK', openapi.IN_QUERY, description="Número de rango", type=openapi.TYPE_STRING),
            openapi.Parameter('voteDate', openapi.IN_QUERY, description="Año voto", type=openapi.TYPE_STRING, format='date'),
        ],
        responses={200: VoteSerializer(many=True)},
    )
    @action(detail=False, methods=['GET'])
    def countVotes(self, request):
        """
        Obtiene el total de votos por rango, etapa y fecha.

        ---
        # Parámetros:
        - stageIdFK: Número de etapa.
        - rangeIdFK: Número de rango.
        - voteDate: Fecha de voto en formato de año.
    
        # Retorna:
        - una lista de la cantidad de votos por electo con información detallada de mayor a menor.
        """
        # Obtener la URL base para concatenarlo con la url de la imagen
        base_url = request.build_absolute_uri('/uploads/')

        stageIdFK = request.query_params.get('stageIdFK')
        rangeIdFK = request.query_params.get('rangeIdFK')
        voteDate_str = request.query_params.get('voteDate')

        filters = {'revocationStatus': False}

        if stageIdFK:
            filters['stageIdFK'] = stageIdFK

        if rangeIdFK:
            filters['rangeIdFK'] = rangeIdFK

        if voteDate_str:
            filters['voteDate__year'] = voteDate_str

        counts = (
            Vote.objects
            .filter(**filters)
            .values(
                    'stageIdFK',
                    'rangeIdFK', 
                    'empCandidateIdFK', 
                    workstation=F('empCandidateIdFK__workstation'),
                    dependency=F('empCandidateIdFK__dependencyId'),
                    username=F('empCandidateIdFK__username') 
                 ) 
            .annotate( 
                    image=Concat( Value(base_url),'empCandidateIdFK__image',output_field=CharField() ), 
                    full_name=Concat('empCandidateIdFK__first_name', Value(' '), 'empCandidateIdFK__last_name'),                 
                    year=TruncYear('voteDate'), 
                    total=Count('voteId')
                )   
            .order_by('-total')
        )

        return Response(counts, status=status.HTTP_200_OK)
        

#-------------------------------------------------------------------------------------------------------------------
     # Peticion para obtener el total de votos por rango, etapa y fecha (fecha es el año)
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('stageIdFK', openapi.IN_QUERY, description="Número de etapa", type=openapi.TYPE_STRING),
            openapi.Parameter('rangeIdFK', openapi.IN_QUERY, description="Número de rango", type=openapi.TYPE_STRING),
            openapi.Parameter('voteDate', openapi.IN_QUERY, description="Año voto", type=openapi.TYPE_STRING, format='date'),
            openapi.Parameter('top', openapi.IN_QUERY, description="Número de registros a retornar", type=openapi.TYPE_INTEGER),
        ],
        responses={200: VoteSerializer(many=True)},
    )
    @action(detail=False, methods=['GET'])
    def countTopVotes(self, request):
        """
        Obtiene el total de votos por rango, etapa y año, limitado por un Tope de registros.

        # Parámetros:
        - stageIdFK: Número de etapa.
        - rangeIdFK: Número de rango.
        - voteDate: Año de voto.
        - top: Número de registros a retornar (opcional).

        # Retorna:
        - Lista de votos con información detallada, ordenada por el total de votos de mayor a menor.
        """
        # Obtener la URL base para concatenarlo con la url de la imagen
        base_url = request.build_absolute_uri('/uploads/')

        stageIdFK = request.query_params.get('stageIdFK')
        rangeIdFK = request.query_params.get('rangeIdFK')
        voteDate_str = request.query_params.get('voteDate')
        top_count = request.query_params.get('top')  # Obtener el parámetro "top"

        filters = {'revocationStatus': False}

        if stageIdFK:
            filters['stageIdFK'] = stageIdFK

        if rangeIdFK:
            filters['rangeIdFK'] = rangeIdFK

        if voteDate_str:
            filters['voteDate__year'] = voteDate_str

        counts = (
            Vote.objects
            .filter(**filters)
            .values(
                    'stageIdFK',
                    'rangeIdFK', 
                    'empCandidateIdFK', 
                    workstation=F('empCandidateIdFK__workstation'),
                    dependency=F('empCandidateIdFK__dependencyId'),
                    username=F('empCandidateIdFK__username') 
                 ) 
            .annotate( 
                    image=Concat( Value(base_url),'empCandidateIdFK__image',output_field=CharField() ), 
                    full_name=Concat('empCandidateIdFK__first_name', Value(' '), 'empCandidateIdFK__last_name'),                 
                    year=TruncYear('voteDate'), 
                    total=Count('voteId')
                )   
            .order_by('-total')[:int(top_count)] if top_count else None  # Aplicar el recuento superior si se proporciona
        )

        return Response(counts, status=status.HTTP_200_OK)


    
#-------------------------------------------------------------------------------------------------------------------
# Peticion para obtener todos los votos sin contabilizar por rango, etapa y fecha
    @swagger_auto_schema(
    manual_parameters=[
        openapi.Parameter('stageIdFK', openapi.IN_QUERY, description="Número de etapa", type=openapi.TYPE_STRING),
        openapi.Parameter('rangeIdFK', openapi.IN_QUERY, description="Número de rango", type=openapi.TYPE_STRING),
        openapi.Parameter('voteDate', openapi.IN_QUERY, description="Año voto", type=openapi.TYPE_STRING, format='date'),
    ],
    responses={200: VoteSerializer(many=True)},
    )
    @action(detail=False, methods=['GET'])
    def getAllVotes(self, request):
        """
        Obtiene todos los registros de la tabla votos filtrandolos por rango, etapa y fecha, (sin contabilizar) .

        ---
        # Parámetros:
        - stageIdFK: Número de etapa.
        - rangeIdFK: Número de rango.
        - voteDate: Fecha de voto en formato de año.
        
        # Retorna:
        - una lista de todos los registros de votos sin contabilizar.
        """
        stageIdFK = request.query_params.get('stageIdFK')
        rangeIdFK = request.query_params.get('rangeIdFK')
        voteDate_str = request.query_params.get('voteDate')

        filters = {}

        if stageIdFK:
            filters['stageIdFK'] = stageIdFK

        if rangeIdFK:
            filters['rangeIdFK'] = rangeIdFK

        if voteDate_str:
            filters['voteDate__year'] = voteDate_str
            
        votes = (
            Vote.objects
            .filter(**filters)
            .values(
                'stageIdFK',
                'rangeIdFK',
                'empCandidateIdFK',
                nombre_candidato=Concat('empCandidateIdFK__first_name' , Value(' '), 'empCandidateIdFK__last_name'),
                voteDate_trunc=TruncDate('voteDate'),                                
            )
        )
        
        return Response(votes, status=status.HTTP_200_OK)


#-------------------------------------------------------------------------------------------------------------------
    # Acción para verificar la existencia de registros con la fk, la etapa y el año proporcionados
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('empVoterIdFK', openapi.IN_QUERY, description="Número de empleado del votante", type=openapi.TYPE_STRING),
            openapi.Parameter('stageIdFK', openapi.IN_QUERY, description="Número de etapa", type=openapi.TYPE_STRING),
            openapi.Parameter('voteDate', openapi.IN_QUERY, description="Año voto", type=openapi.TYPE_STRING, format='date'),
        ],
        responses={200: openapi.TYPE_BOOLEAN},  # Cambiado a openapi.TYPE_BOOLEAN
    )
    @action(detail=False, methods=['GET'])
    def checkExistingVote(self, request):
        """
        Verifica la existencia de un voto basado en el número de empleado del votante, el número de etapa y el año de voto.

        # Parámetros:
        - empVoterIdFK  : Número de empleado del votante.
        - stageIdFK: Número de etapa.
        - voteDate: Año de voto.

        # Retorna:
        - True si existe un voto con las condiciones dadas, False de lo contrario.
        """
        empVoterIdFK = request.query_params.get('empVoterIdFK')
        stageIdFK = request.query_params.get('stageIdFK')
        voteDate_str = request.query_params.get('voteDate')

        filters = {'empVoterIdFK': empVoterIdFK, 'stageIdFK': stageIdFK, 'voteDate__year': voteDate_str}

        exists = Vote.objects.filter(**filters).exists()

        return Response(exists, status=status.HTTP_200_OK)
    


#-------------------------------------------------------------------------------------------------------------------
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('empCandidateIdFK', openapi.IN_QUERY, description="ID del candidato a actualizar", type=openapi.TYPE_INTEGER),
        ],
        responses={
            status.HTTP_200_OK: openapi.Response("Se actualizaron registros", example={'message': 'Se actualizaron registros.'}),
            status.HTTP_404_NOT_FOUND: openapi.Response("No se encontraron registros", example={'message': 'No se encontraron registros para actualizar.'}),
            status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response("Error interno del servidor", example={'error': 'Mensaje de error.'}),
        },
    )
    @action(detail=False, methods=['GET'])
    def updateRevocationStatus(self, request):
        """
        Actualiza el campo estatus_revocacion a True para los registros específicos de votos.

        Actualiza el campo estatus_revocacion a True para los registros específicos de un candidato para ya no contabilizarlos en caso de una revocatoría.
        
        # Parámetros:
        - empCandidateIdFK (int): ID del candidato a actualizar.

        # Retorna:
        - 200 OK: Se actualizaron registros. Ejemplo: {'message': 'Se actualizaron registros.'}
        - 404 Not Found: No se encontraron registros para actualizar. Ejemplo: {'message': 'No se encontraron registros para actualizar.'}
        - 500 Internal Server Error: Error interno del servidor. Ejemplo: {'error': 'Mensaje de error.'}
        """
        try:
            empCandidateIdFK = request.query_params.get('empCandidateIdFK')

            current_year = timezone.now().year
            print(empCandidateIdFK)
            print(current_year)
            # Actualizar el campo estatus_revocacion a True para los registros específicos
            filters = {'empCandidateIdFK': empCandidateIdFK}    

            updated_rows = (
                 Vote.objects
                 .filter(**filters)
                 .update(revocationStatus=True)
             )

            if updated_rows > 0:
                 return Response({'message': f'Se actualizaron {updated_rows} registros.'}, status=status.HTTP_200_OK)
            else:
                 return Response({'message': 'No se encontraron registros para actualizar.'}, status=status.HTTP_404_NOT_FOUND) 
        

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)