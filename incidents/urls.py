from django.urls import path, include
from django.views.generic import RedirectView
from rest_framework.routers import DefaultRouter
from .views import (
    IncidentViewSet, IncidentHistoryViewSet, app_index,
    crear_imagen_incidencia, crear_historial_incidencia,
    agregar_incidencia, actualizar_incidencia, eliminar_incidencia,
)

router = DefaultRouter()
router.register(r'incidencias', IncidentViewSet, basename='incidencia')
router.register(r'historial', IncidentHistoryViewSet, basename='historialincidencia')

urlpatterns = [
    path('crear/imagen/', crear_imagen_incidencia, name='crear_imagen_incidencia'),
    path('crear/historial/', crear_historial_incidencia, name='crear_historial_incidencia'),
    path('agregar/', agregar_incidencia, name='agregar_incidencia'),
    path('crear/', RedirectView.as_view(pattern_name='agregar_incidencia'), name='crear_incidencia'),
    path('actualizar/<uuid:pk>/', actualizar_incidencia, name='actualizar_incidencia'),
    path('eliminar/<uuid:pk>/', eliminar_incidencia, name='eliminar_incidencia'),
    path('', app_index, name='incidencias_index'),
    path('', include(router.urls)),
]