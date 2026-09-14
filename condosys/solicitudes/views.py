from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from residents.models import Resident
from .models import Solicitud
from .serializers import SolicitudSerializer
from .forms import SolicitudForm


# @login_required
def app_index(request):
    contexto = {
        'form_solicitud': SolicitudForm(),
        'residentes': Resident.objects.select_related('apartment').all(),
        'module_name': 'Solicitudes'
    }
    return render(request, 'solicitudes/index.html', contexto)


# @login_required
@require_POST
def crear_solicitud(request):
    form = SolicitudForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()
        messages.success(request, 'Solicitud creada correctamente.')
    else:
        messages.error(request, 'No se pudo crear la solicitud. Revisa los datos enviados.')
    return redirect('solicitudes_index')


class SolicitudViewSet(viewsets.ModelViewSet):
    """ViewSet para Solicitud"""
    queryset = Solicitud.objects.all()
    serializer_class = SolicitudSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['description', 'apartment__name', 'resident__full_name']
    ordering_fields = ['created_at', 'request_date', 'status', 'request_type']
    ordering = ['-created_at']
    filterset_fields = ['apartment', 'status', 'request_type', 'resident']