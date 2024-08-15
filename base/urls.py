from django.contrib import admin
from django.urls import path, include, re_path
#importaciones necesarias para el manejo de imagenes
from django.conf import settings
from django.conf.urls.static import static

#importaciones de rest_framework
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

#importaciones de rutas creadas en nuestro proyecto
from user.api.router import userRouter
from range.api.router import rangeRouter
from stage.api.router import stageRouter
from vote.api.router import voteRouter
from dependency.api.router import dependencyRouter
from forgetPasswordRequest.api.router import forgetPasswordRequestRouter
from emails.api.views import EmailsApiView

schema_view = get_schema_view(
   openapi.Info(
      title="Base_ComiteEtica_ApiDoc",
      default_version='v2',
      description="documentacion base de la api de cómite ética",
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    #rutas globales de django
    path('admin/', admin.site.urls),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    #rutas de nuestras api
    path('api/', include(userRouter.urls)),
    path('api/', include('user.api.router')),#esta ruta es diferente porque es para saber los datos del usuario que se autentica
    path('api/', include(rangeRouter.urls)),
    path('api/', include(stageRouter.urls)),
    path('api/', include(voteRouter.urls)),
    path('api/', include(dependencyRouter.urls)),
    path('api/', include(forgetPasswordRequestRouter.urls)),
    path('api/emails/', EmailsApiView.as_view(), name='emails'),

]

#rutas para imagenes
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)