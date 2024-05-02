from rest_framework import serializers
from user.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 
                  'last_name', 'password', 'email', 'rankIdFk', 'dependencyId', 'is_active', 'is_staff', 'workstation', 'antiquity', 'isAdmin' ,'image']