from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ResidentViewSet, app_index, crear_residente

router = DefaultRouter()
router.register(r'', ResidentViewSet, basename='resident')

urlpatterns = [
    path('crear/', crear_residente, name='crear_residente'),
    path('', app_index, name='residents_index'),
    path('', include(router.urls)),
]
