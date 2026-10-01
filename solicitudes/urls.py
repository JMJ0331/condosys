from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SolicitudViewSet, app_index,
    agregar_solicitud, actualizar_solicitud, eliminar_solicitud,
)

router = DefaultRouter()
router.register(r'', SolicitudViewSet, basename='solicitud')

urlpatterns = [
    path('agregar/', agregar_solicitud, name='agregar_solicitud'),
    path('actualizar/<uuid:pk>/', actualizar_solicitud, name='actualizar_solicitud'),
    path('eliminar/<uuid:pk>/', eliminar_solicitud, name='eliminar_solicitud'),
    path('', app_index, name='solicitudes_index'),
    path('', include(router.urls)),
]
