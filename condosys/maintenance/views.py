from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import MaintenanceOrder
from .serializers import (
    MaintenanceOrderListSerializer,
    MaintenanceOrderDetailSerializer
)
from .forms import MaintenanceOrderForm


def app_index(request):
    contexto = {
        'form_maintenance_order': MaintenanceOrderForm(),
        'module_name': 'Mantenimientos'
    }
    return render(request, 'maintenance/index.html', contexto)


class MaintenanceOrderViewSet(viewsets.ModelViewSet):
    """ViewSet para MaintenanceOrder"""
    queryset = MaintenanceOrder.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['apartment__number', 'assigned_to__email', 'description']
    ordering_fields = ['scheduled_date', 'status']
    ordering = ['-scheduled_date']
    filterset_fields = ['status', 'type', 'assigned_to', 'apartment']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return MaintenanceOrderDetailSerializer
        return MaintenanceOrderListSerializer

