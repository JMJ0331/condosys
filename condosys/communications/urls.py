from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CommunicationViewSet, app_index, crear_comunicacion

router = DefaultRouter()
router.register(r'', CommunicationViewSet, basename='comunicacion')

urlpatterns = [
    path('crear/', crear_comunicacion, name='crear_comunicacion'),
    path('', app_index, name='comunicados_index'),
    path('', include(router.urls)),
]
