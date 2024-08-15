from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.core.mail import send_mail

class EmailsApiView(APIView):
    permission_classes = [AllowAny]  # Permitir acceso a cualquier usuario

    def post(self, request):
        try:
            to_email = request.data.get("to_email")
            subject = request.data.get("subject")
            message = request.data.get("message")

            send_mail(subject, message, None, [to_email])
            return Response({"message": "Email enviado correctamente"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
