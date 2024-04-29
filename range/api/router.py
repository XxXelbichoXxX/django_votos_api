from rest_framework.routers import DefaultRouter
from range.api.views import RangoApiViewSet

router_rango = DefaultRouter()

router_rango.register(
    prefix='rango',
    basename='rango',
    viewset=RangoApiViewSet
)