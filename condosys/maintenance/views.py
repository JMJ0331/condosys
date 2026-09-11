from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import MaintenanceOrder
from .serializers import (
    MaintenanceOrderListSerializer,
    MaintenanceOrderDetailSerializer
)
from .forms import MaintenanceOrderForm


@login_required
def app_index(request):
    contexto = {
        'form_maintenance_order': MaintenanceOrderForm(),
        'module_name': 'Mantenimientos'
    }
    return render(request, 'maintenance/index.html', contexto)


@login_required
@require_POST
def crear_orden_mantenimiento(request):
    form = MaintenanceOrderForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, 'Orden de mantenimiento creada correctamente.')
    else:
        messages.error(request, 'No se pudo crear la orden. Revisa los datos enviados.')
    return redirect('inicio')


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

