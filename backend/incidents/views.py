from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import Incident, IncidentHistory
from .serializers import (
    IncidentListSerializer, IncidentDetailSerializer,
    IncidentHistorySerializer
)


class IncidentViewSet(viewsets.ModelViewSet):
    """ViewSet para Incident"""
    queryset = Incident.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'apartment__number', 'reported_by__email']
    ordering_fields = ['created_at', 'priority', 'status']
    ordering = ['-created_at']
    filterset_fields = ['apartment', 'status', 'priority', 'category', 'assigned_to']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return IncidentDetailSerializer
        return IncidentListSerializer


class IncidentHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet solo lectura para IncidentHistory"""
    queryset = IncidentHistory.objects.all()
    serializer_class = IncidentHistorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    filterset_fields = ['incident']

