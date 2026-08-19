from django.db.models import Q
from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import Incident, IncidentHistory
from accounts.permissions import CanModifyIncident
from .serializers import (
    IncidentListSerializer, IncidentDetailSerializer,
    IncidentHistorySerializer
)


def app_index(request):
    return render(request, 'incidents/index.html', {'module_name': 'Incidencias'})


class IncidentViewSet(viewsets.ModelViewSet):
    """ViewSet para Incident"""
    queryset = Incident.objects.all()
    permission_classes = [IsAuthenticated, CanModifyIncident]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'apartment__number', 'reported_by__email']
    ordering_fields = ['created_at', 'priority', 'status']
    ordering = ['-created_at']
    filterset_fields = ['apartment', 'status', 'priority', 'category', 'assigned_to']

    def get_queryset(self):
        user = self.request.user
        if user.role in ['admin', 'manager']:
            return Incident.objects.all()
        if user.role in ['maintenance', 'security']:
            return Incident.objects.filter(Q(assigned_to=user) | Q(reported_by=user)).distinct()
        return Incident.objects.filter(reported_by=user)

    def perform_update(self, serializer):
        incident = self.get_object()
        previous_status = incident.status
        previous_assigned = incident.assigned_to
        updated_incident = serializer.save()

        status_changed = previous_status != updated_incident.status
        assigned_changed = previous_assigned != updated_incident.assigned_to
        if status_changed or assigned_changed:
            IncidentHistory.objects.create(
                incident=updated_incident,
                status_from=previous_status,
                status_to=updated_incident.status,
                changed_by=self.request.user,
                comment=self.request.data.get('history_comment', None)
            )

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

