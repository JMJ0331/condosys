from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CommunicationViewSet, app_index

router = DefaultRouter()
router.register(r'', CommunicationViewSet, basename='communication')

urlpatterns = [
    path('', app_index, name='communications_index'),
    path('', include(router.urls)),
]
