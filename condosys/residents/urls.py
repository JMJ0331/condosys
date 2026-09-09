from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ResidentViewSet, app_index

router = DefaultRouter()
router.register(r'', ResidentViewSet, basename='resident')

urlpatterns = [
    path('', app_index, name='residents_index'),
    path('', include(router.urls)),
]
