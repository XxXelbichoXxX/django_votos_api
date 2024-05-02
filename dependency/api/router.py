from rest_framework.routers import DefaultRouter
from dependency.api.views import DependencyApiViewSet

dependencyRouter = DefaultRouter()

dependencyRouter.register(
    prefix='dependency',
    basename='dependency',
    viewset=DependencyApiViewSet
)