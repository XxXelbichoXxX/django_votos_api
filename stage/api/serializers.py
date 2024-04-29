from rest_framework.serializers import ModelSerializer
from stage.models import Etapa


class EtapaSerializer(ModelSerializer):
    class Meta:
        model = Etapa
        fields = ['id', 'num_etapa', 'nombre_etapa', 'fecha_inicio', 'fecha_fin']