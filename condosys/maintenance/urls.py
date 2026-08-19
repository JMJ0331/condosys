from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MaintenanceOrderViewSet, app_index

router = DefaultRouter()
router.register(r'', MaintenanceOrderViewSet, basename='maintenanceorder')

urlpatterns = [
    path('', app_index, name='maintenance_index'),
    path('', include(router.urls)),
]
