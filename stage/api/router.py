from rest_framework.routers import DefaultRouter
from stage.api.views import StageApiViewSet

stageRouter = DefaultRouter()

stageRouter.register(
    prefix='stage',
    basename='stage',
    viewset=StageApiViewSet
)