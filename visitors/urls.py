from django.urls import path, include
from django.views.generic import RedirectView
from rest_framework.routers import DefaultRouter
from .views import (
    VisitorViewSet, app_index,
    agregar_visitante, actualizar_visitante, eliminar_visitante,
)

router = DefaultRouter()
router.register(r'registros', VisitorViewSet, basename='visitante')

urlpatterns = [
    path('agregar/', agregar_visitante, name='agregar_visitante'),
    path('crear/', RedirectView.as_view(pattern_name='agregar_visitante'), name='crear_visitante'),
    path('actualizar/<uuid:pk>/', actualizar_visitante, name='actualizar_visitante'),
    path('eliminar/<uuid:pk>/', eliminar_visitante, name='eliminar_visitante'),
    path('', app_index, name='visitantes_index'),
    path('', include(router.urls)),
]
