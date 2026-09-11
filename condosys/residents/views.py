from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from rest_framework import filters, viewsets
from accounts.permissions import IsManager
from .forms import ResidentForm
from .models import Resident
from .serializers import ResidentSerializer


@login_required
def app_index(request):
    contexto = {
        'form_resident': ResidentForm(),
        'module_name': 'Residentes',
    }
    return render(request, 'residents/index.html', contexto)


@login_required
@require_POST
def crear_residente(request):
    form = ResidentForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()
        messages.success(request, 'Residente registrado correctamente.')
    else:
        messages.error(request, 'No se pudo registrar el residente. Revisa los datos enviados.')
    return redirect('inicio')


class ResidentViewSet(viewsets.ModelViewSet):
    """ViewSet para Resident"""
    queryset = Resident.objects.all()
    serializer_class = ResidentSerializer
    permission_classes = [IsManager]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['full_name', 'email', 'cedula', 'apartment__number']
    ordering_fields = ['created_at', 'full_name']
    ordering = ['apartment', 'full_name']
    filterset_fields = ['apartment', 'is_active']

    def get_queryset(self):
        user = self.request.user
        if user.role in ['admin', 'manager']:
            return Resident.objects.all()
        return Resident.objects.filter(user=user)