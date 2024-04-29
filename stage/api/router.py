from rest_framework.routers import DefaultRouter
from stage.api.views import EtapaApiViewSet

router_Etapa = DefaultRouter()

router_Etapa.register(
    prefix='etapa',
    basename='etapa',
    viewset=EtapaApiViewSet
)