from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CommunicationViewSet, app_index,
    agregar_comunicado, actualizar_comunicado, eliminar_comunicado,
)

router = DefaultRouter()
router.register(r'', CommunicationViewSet, basename='comunicacion')

urlpatterns = [
    path('agregar/', agregar_comunicado, name='agregar_comunicado'),
    path('actualizar/<uuid:pk>/', actualizar_comunicado, name='actualizar_comunicado'),
    path('eliminar/<uuid:pk>/', eliminar_comunicado, name='eliminar_comunicado'),
    path('', app_index, name='comunicados_index'),
    path('', include(router.urls)),
]
