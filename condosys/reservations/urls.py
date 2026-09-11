from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CommonAreaViewSet, ReservationViewSet, app_index,
    crear_area_comun, crear_reserva,
)

router = DefaultRouter()
router.register(r'common-areas', CommonAreaViewSet, basename='commonarea')
router.register(r'', ReservationViewSet, basename='reservation')

urlpatterns = [
    path('crear/area-comun/', crear_area_comun, name='crear_area_comun'),
    path('crear/', crear_reserva, name='crear_reserva'),
    path('', app_index, name='reservations_index'),
    path('', include(router.urls)),
]