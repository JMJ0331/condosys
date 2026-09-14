from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SolicitudViewSet, app_index, crear_solicitud

router = DefaultRouter()
router.register(r'', SolicitudViewSet, basename='solicitud')

urlpatterns = [
    path('crear/', crear_solicitud, name='crear_solicitud'),
    path('', app_index, name='solicitudes_index'),
    path('', include(router.urls)),
]