from django.db.models import Q
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import Incident, IncidentHistory
from accounts.permissions import CanModifyIncident
from residents.models import Resident
from .serializers import (
    IncidentListSerializer, IncidentDetailSerializer,
    IncidentHistorySerializer
)
from .forms import IncidentForm, IncidentImageForm, IncidentHistoryForm


<<<<<<< HEAD
=======
# @login_required
>>>>>>> 92964151f67b4af53f5d5b1c0445adc7116e3df9
def app_index(request):
    contexto = {
        'form_incident': IncidentForm(),
        'form_incident_image': IncidentImageForm(),
        'form_incident_history': IncidentHistoryForm(),
        'residentes': Resident.objects.select_related('apartment').all(),
        'module_name': 'Incidencias'
    }
    return render(request, 'incidents/index.html', contexto)


<<<<<<< HEAD
=======
# @login_required
>>>>>>> 92964151f67b4af53f5d5b1c0445adc7116e3df9
@require_POST
def crear_incidencia(request):
    form = IncidentForm(request.POST, request.FILES)
    if form.is_valid():
        incidencia = form.save(commit=False)
        incidencia.reported_by = request.user
        # Título no se pide en el formulario: se genera a partir del tipo y
        # la descripción para que el registro nunca quede sin título.
        if not incidencia.title:
            base = f"{incidencia.get_category_display()}: {incidencia.description}"
            incidencia.title = base[:200]
        incidencia.save()
        # El comentario de "Seguimiento" queda guardado como primer registro
        # del historial de la incidencia.
        comentario = form.cleaned_data.get('comment')
        if comentario:
            IncidentHistory.objects.create(
                incident=incidencia,
                status_from=None,
                status_to=incidencia.status,
                changed_by=request.user,
                comment=comentario,
            )
        messages.success(request, 'Incidencia creada correctamente.')
    else:
        messages.error(request, 'No se pudo crear la incidencia. Revisa los datos enviados.')
    return redirect('inicio')


<<<<<<< HEAD
=======
# @login_required
>>>>>>> 92964151f67b4af53f5d5b1c0445adc7116e3df9
@require_POST
def crear_imagen_incidencia(request):
    form = IncidentImageForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, 'Imagen de incidencia agregada correctamente.')
    else:
        messages.error(request, 'No se pudo agregar la imagen. Revisa los datos enviados.')
    return redirect('inicio')


<<<<<<< HEAD
=======
# @login_required
>>>>>>> 92964151f67b4af53f5d5b1c0445adc7116e3df9
@require_POST
def crear_historial_incidencia(request):
    form = IncidentHistoryForm(request.POST)
    if form.is_valid():
        historial = form.save(commit=False)
        historial.changed_by = request.user
        historial.save()
        messages.success(request, 'Historial de incidencia creado correctamente.')
    else:
        messages.error(request, 'No se pudo crear el historial. Revisa los datos enviados.')
    return redirect('inicio')


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

