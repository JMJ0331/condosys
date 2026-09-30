from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ResidencialViewSet, app_index

router = DefaultRouter()
router.register(r'residencial', ResidencialViewSet, basename='residencial')

urlpatterns = [
    path('', app_index, name='residencial_index'),
    path('', include(router.urls)),
]
