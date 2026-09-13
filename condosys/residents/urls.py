from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ResidentViewSet, app_index, crear_residente

router = DefaultRouter()
router.register(r'', ResidentViewSet, basename='residente')

urlpatterns = [
    path('crear/', crear_residente, name='crear_residente'),
    path('', app_index, name='residentes_index'),
    path('', include(router.urls)),
]
