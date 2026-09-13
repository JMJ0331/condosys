from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MaintenanceOrderViewSet, app_index, crear_orden_mantenimiento

router = DefaultRouter()
router.register(r'', MaintenanceOrderViewSet, basename='ordenmantenimiento')

urlpatterns = [
    path('crear/', crear_orden_mantenimiento, name='crear_orden_mantenimiento'),
    path('', app_index, name='mantenimientos_index'),
    path('', include(router.urls)),
]