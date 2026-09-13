from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import MaintenanceCharge
from .serializers import (
    MaintenanceChargeListSerializer,
    MaintenanceChargeDetailSerializer
)
from .forms import MaintenanceChargeForm


# @login_required
def app_index(request):
    contexto = {
        'form_cargo_mantenimiento': MaintenanceChargeForm(),
        'module_name': 'Mantenimientos'
    }
    return render(request, 'maintenance/index.html', contexto)


# @login_required
@require_POST
def crear_cargo_mantenimiento(request):
    form = MaintenanceChargeForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()
        messages.success(request, 'Cargo de mantenimiento creado correctamente.')
    else:
        messages.error(request, 'No se pudo crear el cargo. Revisa los datos enviados.')
    return redirect('inicio')


class MaintenanceChargeViewSet(viewsets.ModelViewSet):
    """ViewSet para MaintenanceCharge"""
    queryset = MaintenanceCharge.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['concept']
    ordering_fields = ['effective_date', 'amount']
    ordering = ['-effective_date']
    filterset_fields = ['concept', 'periodicity', 'is_active']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return MaintenanceChargeDetailSerializer
        return MaintenanceChargeListSerializer