from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MaintenanceOrderViewSet

router = DefaultRouter()
router.register(r'', MaintenanceOrderViewSet, basename='maintenanceorder')

urlpatterns = [
    path('', include(router.urls)),
]
