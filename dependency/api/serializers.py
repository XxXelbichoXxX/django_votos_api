from rest_framework.serializers import ModelSerializer
from dependency.models import Dependency


class DependencySerializer(ModelSerializer):
    class Meta:
        model = Dependency
        fields = ['dependencyId', 'dependencyName', 'owner', 'address', 'phone', 'logo']