from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MaintenanceChargeViewSet, app_index, crear_cargo_mantenimiento

router = DefaultRouter()
router.register(r'', MaintenanceChargeViewSet, basename='cargomantenimiento')

urlpatterns = [
    path('crear/', crear_cargo_mantenimiento, name='crear_cargo_mantenimiento'),
    path('', app_index, name='mantenimientos_index'),
    path('', include(router.urls)),
]