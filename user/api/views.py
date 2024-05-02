from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.contrib.auth.hashers import make_password

#importaciones necesarias para hacer solicitudes http personalizadas
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.db import transaction

#importaciones personales de nuestro proyecto
from user.models import User
from user.api.serializers import UserSerializer


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
        

#creamos otra vista para obtener los datos del usuario que se autentica
class UserView(APIView):
    permission_classes = [IsAuthenticated]  
    
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)