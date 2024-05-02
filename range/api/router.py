from rest_framework.routers import DefaultRouter
from range.api.views import RangeApiViewSet

rangeRouter = DefaultRouter()

rangeRouter.register(
    prefix='range',
    basename='range',
    viewset=RangeApiViewSet
)