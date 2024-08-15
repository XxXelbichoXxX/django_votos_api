from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.contrib.auth.hashers import make_password
from django.db.models import Count

#importaciones necesarias para hacer solicitudes http personalizadas
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.db import transaction
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db.models.functions import Concat
from django.db.models import Value, CharField

#importaciones personales de nuestro proyecto
from user.models import User
from utils.utils import check_code_exists
from user.api.serializers import UserSerializer

import logging

logger = logging.getLogger(__name__)




class UserApiViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer
    queryset = User.objects.all()

    #SOBRE-ESCRIBIMOS EL METODO CREATE DE LA SUPERCLASE DE LA QUE HEREDAMOS PARA QUE ENCRIPTE EL PASSWORD ANTES DE INSERTARLO EN LA BD
    def create(self, request, *args, **kwargs):
        request.data['password'] = make_password(request.data['password'])
        return super().create(request, *args, **kwargs)
    
    #SOBRE- ESCRIBIMOS EL METODO DEL PATCH DE LA SUPERCLASE PARA QUE DETECTE CUANDO SE MODIFICO LA CONTRASEÑA Y LA ENCRIPTE DE NUEVO
    def partial_update(self, request, *args, **kwargs):
        password = request.data.get('password')
        if password is not None:
            request.data['password'] = make_password(password)
        return super().partial_update(request, *args, **kwargs)
    

    @action(detail=False, methods=['POST'], permission_classes=[AllowAny])
    def reset_password(self, request):
        username = request.data.get('username')
        code = request.data.get('code')
        password = request.data.get('password')

        if not username or not code or not password:
            return Response({"error": "Faltan datos obligatorios"}, status=status.HTTP_400_BAD_REQUEST)

        if not check_code_exists(code):
            return Response({"error": "Código incorrecto"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(username=username)
            user.set_password(password)  # Usar el método set_password para encriptar la nueva contraseña
            user.save()
            return Response({"success": "Contraseña cambiada exitosamente."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "Usuario no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error inesperado: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Peticion para obtener todos los usuarios depende su dependencia
    @swagger_auto_schema(
    manual_parameters=[
        openapi.Parameter('dependencyIdFK', openapi.IN_QUERY, description="Id de la dependencia a la que pertenencen", type=openapi.TYPE_INTEGER),
    ],
    responses={200: UserSerializer(many=True)},
    )
    @action(detail=False, methods=['GET'])
    def getUsersByDependency(self, request):
        """
        Obtiene todos los usuarios que pertenecen a una dependencia.

        ---
        # Parámetros:
        - dependencyIdFK: Id de la dependencia.
        
        # Retorna:
        - una lista de todos los usuarios que pertenecen a la dependencia.
        """
        base_url = request.build_absolute_uri('/uploads/')
        dependencyIdFK = request.query_params.get('dependencyIdFK')

        filters = {}

        if dependencyIdFK:
            filters['dependencyIdFK'] = dependencyIdFK

            
        users = (
            User.objects
            .filter(**filters)
            .values(
                "id",
                "username",
                "first_name",
                "last_name",
                "password",
                "email",
                "rangeIdFK",
                "dependencyIdFK",
                "is_active",
                "is_staff",
                "workstation",
                "antiquity",
                "isAdmin",
                "image"
            ).annotate(
                 logo=Concat(Value(base_url), 'dependencyIdFK__logo', output_field=CharField()),
            )
        )
        
        return Response(users, status=status.HTTP_200_OK)
        
    @swagger_auto_schema(
    manual_parameters=[
        openapi.Parameter('dependencyIdFK', openapi.IN_QUERY, description="Id de la dependencia a la que pertenencen", type=openapi.TYPE_INTEGER),
    ],
    responses={200: UserSerializer(many=True)},
    )
    @action(detail=False, methods=['GET'])
    def countUsersByDependency(self, request):
        """
        Obtiene todos los usuarios que pertenecen a una dependencia.

        ---
        # Parámetros:
        - dependencyIdFK: Id de la dependencia.

        # Retorna:
        - una lista de todos los usuarios que pertenecen a la dependencia.
        """
        dependencyIdFK = request.query_params.get('dependencyIdFK')

        filters = {}

        if dependencyIdFK:
            filters['dependencyIdFK'] = dependencyIdFK
            
        total_users = (
        User.objects
        .filter(**filters)
        .count()
        )
        
        return Response(total_users, status=status.HTTP_200_OK)
        
    
    @swagger_auto_schema(
    manual_parameters=[
        openapi.Parameter('dependencyIdFK', openapi.IN_QUERY, description="Id de la dependencia a la que pertenencen", type=openapi.TYPE_INTEGER),
        openapi.Parameter('rangeIdFK', openapi.IN_QUERY, description="Rango  del usuario", type=openapi.TYPE_STRING),
    ],
    responses={200: UserSerializer(many=True)},
    )
    @action(detail=False, methods=['GET'])
    def countUsersByDependencyAndRange(self, request):
        """
        Obtiene todos los usuarios que pertenecen a una dependencia.

        ---
        # Parámetros:
        - dependencyIdFK: Id de la dependencia.
        - rangeIdFK: Rango del usuario.
        # Retorna:
        - una lista de todos los usuarios que pertenecen a la dependencia.
        """
        dependencyIdFK = request.query_params.get('dependencyIdFK')
        rangeIdFK = request.query_params.get('rangeIdFK')

        filters = {}

        if dependencyIdFK:
            filters['dependencyIdFK'] = dependencyIdFK

        if rangeIdFK:
            filters['rangeIdFK'] = rangeIdFK

            
        total_users = (
        User.objects
        .filter(**filters)
        .count()
        )
        
        return Response(total_users, status=status.HTTP_200_OK)
        
    

    #INSERTAMOS UN METODO PARA CREAR VARIOS REGISTROS A LA VEZ 
    @action(detail=False, methods=['POST'])
    def createMassiveUsers(self, request, *args, **kwargs):
        """
        Crea Usuarios de forma masiva.

        Permite crear usuarios en grandes cantidades proporcionando una lista de datos de votos.
        ---
        # Parámetros
        - Se espera una solicitud POST con una lista de objetos JSON  de los nuevos usuarios.
        - Cada dato de usuario debe tener el formato requerido por el serializador UserSerializer.
        """
        # Utiliza el serializador VotoSerializer en lugar de VotoListSerializer
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    # Itera sobre los datos y crea un objeto User para cada conjunto de datos
                    for data in serializer.validated_data:
                        data['password'] = make_password(data['password']) # Encripta la contraseña
                        User.objects.create(**data)
            except Exception as e:
                # Si ocurre un error, puedes manejarlo aquí, por ejemplo, devolviendo un error 500
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('username', openapi.IN_QUERY, description="Número de empleado solicitante", type=openapi.TYPE_STRING),
            openapi.Parameter('email', openapi.IN_QUERY, description="email del empleado", type=openapi.TYPE_STRING),
        ],
        responses={200: openapi.TYPE_BOOLEAN},  # Cambiado a openapi.TYPE_BOOLEAN
    )
    @action(detail=False, methods=['GET'], permission_classes=[AllowAny])
    def checkCredentials(self, request):
        """
        Verifica la existencia del usuario y el email proporcionados.

        # Parámetros:
        - username  : Número de empleado solicitante.
        - email: email del empleado.

        # Retorna:
        - True si existe un voto con las condiciones dadas, False de lo contrario.
        """
        username = request.query_params.get('username')
        email = request.query_params.get('email')

        filters = {'username': username, 'email': email}

        exists = User.objects.filter(**filters).exists()

        return Response(exists, status=status.HTTP_200_OK)

#creamos otra vista para obtener los datos del usuario que se autentica
class UserView(APIView):
    permission_classes = [IsAuthenticated]  
    
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)