from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CommunicationViewSet,
    app_index,
    agregar_comunicado,
    eliminar_comunicado,
)

router = DefaultRouter()
router.register(r'', CommunicationViewSet, basename='comunicacion')

urlpatterns = [
    path('agregar/', agregar_comunicado, name='crear_comunicado'),
    path('eliminar/<uuid:pk>/', eliminar_comunicado, name='eliminar_comunicado'),
    path('', app_index, name='comunicados_index'),
    path('', include(router.urls)),
]
