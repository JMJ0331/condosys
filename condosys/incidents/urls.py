from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import IncidentViewSet, IncidentHistoryViewSet, app_index

router = DefaultRouter()
router.register(r'incidents', IncidentViewSet, basename='incident')
router.register(r'history', IncidentHistoryViewSet, basename='incidenthistory')

urlpatterns = [
    path('', app_index, name='incidents_index'),
    path('', include(router.urls)),
]
