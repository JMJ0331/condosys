from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import IncidentViewSet, IncidentHistoryViewSet

router = DefaultRouter()
router.register(r'incidents', IncidentViewSet, basename='incident')
router.register(r'history', IncidentHistoryViewSet, basename='incidenthistory')

urlpatterns = [
    path('', include(router.urls)),
]
