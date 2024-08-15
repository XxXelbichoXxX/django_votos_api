from rest_framework.routers import DefaultRouter
from forgetPasswordRequest.api.views import ForgetPasswordRequestApiViewSet

forgetPasswordRequestRouter = DefaultRouter()

forgetPasswordRequestRouter.register(
    prefix='forgetPasswordRequest',
    basename='forgetPasswordRequest',
    viewset=ForgetPasswordRequestApiViewSet
)