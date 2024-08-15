from rest_framework.serializers import ModelSerializer
from forgetPasswordRequest.models import ForgetPasswordRequest


class ForgetPasswordRequestSerializer(ModelSerializer):
    class Meta:
        model = ForgetPasswordRequest
        fields = ['requestId', 'username', 'email', 'code', 'useCode']