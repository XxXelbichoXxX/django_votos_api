from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from forgetPasswordRequest.models import ForgetPasswordRequest
from forgetPasswordRequest.api.serializers import ForgetPasswordRequestSerializer
from django.db import transaction
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema

from cryptography.fernet import Fernet, InvalidToken
import binascii
import logging

from drf_yasg import openapi

logger = logging.getLogger(__name__)


class ForgetPasswordRequestApiViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = ForgetPasswordRequest.objects.all()
    serializer_class = ForgetPasswordRequestSerializer

    def load_code(self):
        try:
            with open("aassswascsxzas.key", "rb") as key_file:
                return key_file.read()
        except Exception as e:
            logger.error(f"Error loading key: {str(e)}")
            raise e


    @swagger_auto_schema(
        responses={200: openapi.TYPE_BOOLEAN},  # Cambiado a openapi.TYPE_BOOLEAN
    )
    @action(detail=False, methods=['POST'], permission_classes=[AllowAny])
    def sendInfo(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                key = self.load_code()
                f = Fernet(key)

                code = serializer.validated_data['code']
                encrypted_code = f.encrypt(code.encode())
                serializer.validated_data['code'] = encrypted_code.decode()

                ForgetPasswordRequest.objects.create(**serializer.validated_data)
                return Response({"success": True}, status=status.HTTP_200_OK)  # Retorna True en caso de éxito

            except InvalidToken as e:
                logger.error(f"Invalid token: {str(e)}")
                return Response({"success": False, "error": "Invalid token: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                logger.error(f"Error: {str(e)}")
                return Response({"success": False, "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"success": False, "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    
    
    @swagger_auto_schema(responses={200: ForgetPasswordRequestSerializer(many=True)})
    @action(detail=False, methods=['GET'], permission_classes=[AllowAny])
    def getInfo(self, request, *args, **kwargs):
        """
        Obtiene todos los registros con el campo 'code' desencriptado.

        # Retorna:
        - una lista de todos los registros con el campo 'code' desencriptado.
        """
        key = self.load_code()
        f = Fernet(key)
        
        queryset = self.get_queryset()
        desencrypted_data = []
        for obj in queryset:
            try:
                encrypted_code = obj.code.encode() 
                decrypted_code = f.decrypt(encrypted_code).decode()
                obj.code = decrypted_code
                desencrypted_data.append(obj)
            except (InvalidToken, binascii.Error) as e:
                # Añadir logging para depurar el problema
                logger.error(f"Error al desencriptar el código: {obj.code}. Error: {str(e)}")
                return Response({"error": "Invalid token: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                logger.error(f"Error inesperado: {str(e)}")
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        serializer = self.get_serializer(desencrypted_data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
        # Acción para verificar la existencia de registros con la fk, la etapa y el año proporcionados
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('code', openapi.IN_QUERY, description="Codigo", type=openapi.TYPE_STRING),
        ],
        responses={200: openapi.TYPE_BOOLEAN},  # Cambiado a openapi.TYPE_BOOLEAN
    )
    @action(detail=False, methods=['GET'], permission_classes=[AllowAny])
    def checkExistingCode(self, request):
        """

        # Retorna:
        - True si existe un voto con las condiciones dadas, False de lo contrario.
        """
        code = request.query_params.get('code')
        
        key = self.load_code()
        f = Fernet(key)

        try:
            # Obtener todos los registros y verificar si alguno coincide
            queryset = self.get_queryset()
            for obj in queryset:
                try:
                    # Desencriptar el código almacenado en la base de datos
                    encrypted_code = obj.code.encode()
                    decrypted_code = f.decrypt(encrypted_code).decode()

                    if decrypted_code == code:
                        return Response({"requestId": obj.requestId, "exists": True, "useCode" : obj.useCode}, status=status.HTTP_200_OK)
                except (InvalidToken, binascii.Error) as e:
                    # Manejo de error si el token no es válido
                    logger.error(f"Error al desencriptar el código en la base de datos. Error: {str(e)}")
                    continue  # Continuar con el siguiente registro

            return Response(False, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error inesperado: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    @action(detail=False, methods=['PUT'], permission_classes=[AllowAny])
    def updateStatusCode(self, request):
        """
        Actualiza el campo 'useCode' de un objeto basado en el ID proporcionado.
        """
        requestId = request.data.get('requestId')
        useCode = request.data.get('useCode')

        if requestId is None or useCode is None:
            return Response({"error": "ID y campo 'useCode' son obligatorios."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            obj = ForgetPasswordRequest.objects.get(pk=requestId)
            obj.useCode = useCode
            obj.save()

            serializer = self.get_serializer(obj)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ForgetPasswordRequest.DoesNotExist:
            return Response({"error": "Objeto no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



    """     def genera_clave():
        clave = Fernet.generate_key()
        with open("aassswascsxzas.key", "wb") as key_file:
            key_file.write(clave) """