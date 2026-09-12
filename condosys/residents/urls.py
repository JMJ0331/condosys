from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ResidentViewSet, app_index, crear_residente, nuevo_residente

router = DefaultRouter()
router.register(r'', ResidentViewSet, basename='resident')

urlpatterns = [
    path('nuevo/', nuevo_residente, name='nuevo_residente'),
    path('crear/', crear_residente, name='crear_residente'),
    path('', app_index, name='residents_index'),
    path('', include(router.urls)),
]
