from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import PropietarioViewSet, app_index, crear_propietario, actualizar_propietario, eliminar_propietario

router = DefaultRouter()
router.register(r'', PropietarioViewSet, basename='propietario')

urlpatterns = [
    path('agregar/', crear_propietario, name='crear_propietario'),
    path('actualizar/<uuid:pk>/', actualizar_propietario, name='actualizar_propietario'),
    path('eliminar/<uuid:pk>/', eliminar_propietario, name='eliminar_propietario'),
    path('', app_index, name='propietarios_index'),
    path('', include(router.urls)),
]