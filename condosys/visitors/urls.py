from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VisitorViewSet, app_index, crear_visitante

router = DefaultRouter()
router.register(r'records', VisitorViewSet, basename='visitor')

urlpatterns = [
    path('crear/', crear_visitante, name='crear_visitante'),
    path('', app_index, name='visitors_index'),
    path('', include(router.urls)),
]