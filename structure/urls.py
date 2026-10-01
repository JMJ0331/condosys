from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    GardenViewSet, BuildingViewSet, ApartmentViewSet, app_index,
    agregar_departamento, actualizar_departamento, eliminar_departamento,
)

router = DefaultRouter()
router.register(r'jardines', GardenViewSet, basename='jardin')
router.register(r'edificios', BuildingViewSet, basename='edificio')
router.register(r'departamentos', ApartmentViewSet, basename='departamento')

urlpatterns = [
    path('agregar/', agregar_departamento, name='agregar_departamento'),
    path('actualizar/<uuid:pk>/', actualizar_departamento, name='actualizar_departamento'),
    path('eliminar/<uuid:pk>/', eliminar_departamento, name='eliminar_departamento'),
    path('', app_index, name='departamentos_index'),
    path('', include(router.urls)),
]