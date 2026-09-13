from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import PropietarioViewSet, app_index

router = DefaultRouter()
router.register(r'', PropietarioViewSet, basename='propietario')

urlpatterns = [
    path('', app_index, name='propietarios_index'),
    path('', include(router.urls)),
]