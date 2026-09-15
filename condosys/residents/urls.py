from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ResidentViewSet, app_index, crear_residente, actualizar_residente, eliminar_residente

router = DefaultRouter()
router.register(r'', ResidentViewSet, basename='residente')

urlpatterns = [
    path('agregar/', crear_residente, name='crear_residente'),
    path('actualizar/<uuid:pk>/', actualizar_residente, name='actualizar_residente'),
    path('eliminar/<uuid:pk>/', eliminar_residente, name='eliminar_residente'),
    path('', app_index, name='residentes_index'),
    path('', include(router.urls)),
]
