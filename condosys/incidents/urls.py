from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    IncidentViewSet, IncidentHistoryViewSet, app_index,
    crear_incidencia, crear_imagen_incidencia, crear_historial_incidencia,
)

router = DefaultRouter()
router.register(r'incidencias', IncidentViewSet, basename='incidencia')
router.register(r'historial', IncidentHistoryViewSet, basename='historialincidencia')

urlpatterns = [
    path('crear/imagen/', crear_imagen_incidencia, name='crear_imagen_incidencia'),
    path('crear/historial/', crear_historial_incidencia, name='crear_historial_incidencia'),
    path('crear/', crear_incidencia, name='crear_incidencia'),
    path('', app_index, name='incidencias_index'),
    path('', include(router.urls)),
]