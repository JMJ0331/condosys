from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    GardenViewSet, BuildingViewSet, ApartmentViewSet, app_index,
    crear_jardin, crear_edificio, crear_departamento,
)

router = DefaultRouter()
router.register(r'gardens', GardenViewSet, basename='garden')
router.register(r'buildings', BuildingViewSet, basename='building')
router.register(r'apartments', ApartmentViewSet, basename='apartment')

urlpatterns = [
    path('crear/jardin/', crear_jardin, name='crear_jardin'),
    path('crear/edificio/', crear_edificio, name='crear_edificio'),
    path('crear/departamento/', crear_departamento, name='crear_departamento'),
    path('', app_index, name='structure_index'),
    path('', include(router.urls)),
]