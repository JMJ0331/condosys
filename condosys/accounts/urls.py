from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, app_index, crear_usuario, crear_usuario_nuevo

router = DefaultRouter()
router.register(r'', UserViewSet, basename='user')

urlpatterns = [
    path('crear/usuario/', crear_usuario, name='crear_usuario'),
    path('crear/usuario-nuevo/', crear_usuario_nuevo, name='crear_usuario_nuevo'),
    path('', app_index, name='accounts_index'),
    path('', include(router.urls)),
]
