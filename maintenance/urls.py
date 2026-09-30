from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MaintenanceChargeViewSet, app_index,
    agregar_mantenimiento, actualizar_mantenimiento, eliminar_mantenimiento,
)

router = DefaultRouter()
router.register(r'', MaintenanceChargeViewSet, basename='cargomantenimiento')

urlpatterns = [
    path('agregar/', agregar_mantenimiento, name='agregar_mantenimiento'),
    path('actualizar/<uuid:pk>/', actualizar_mantenimiento, name='actualizar_mantenimiento'),
    path('eliminar/<uuid:pk>/', eliminar_mantenimiento, name='eliminar_mantenimiento'),
    path('', app_index, name='mantenimientos_index'),
    path('', include(router.urls)),
]
