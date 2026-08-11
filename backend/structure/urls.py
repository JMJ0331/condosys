from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GardenViewSet, BuildingViewSet, ApartmentViewSet

router = DefaultRouter()
router.register(r'gardens', GardenViewSet, basename='garden')
router.register(r'buildings', BuildingViewSet, basename='building')
router.register(r'apartments', ApartmentViewSet, basename='apartment')

urlpatterns = [
    path('', include(router.urls)),
]
