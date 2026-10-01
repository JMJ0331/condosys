from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CommonAreaViewSet, ReservationViewSet, app_index,
    crear_area_comun, agregar_reserva, actualizar_reserva, eliminar_reserva,
)

router = DefaultRouter()
router.register(r'areas-comunes', CommonAreaViewSet, basename='areacomun')
router.register(r'', ReservationViewSet, basename='reserva')

urlpatterns = [
    path('crear/area-comun/', crear_area_comun, name='crear_area_comun'),
    path('agregar/', agregar_reserva, name='agregar_reserva'),
    path('actualizar/<uuid:pk>/', actualizar_reserva, name='actualizar_reserva'),
    path('eliminar/<uuid:pk>/', eliminar_reserva, name='eliminar_reserva'),
    path('', app_index, name='reservas_index'),
    path('', include(router.urls)),
]
