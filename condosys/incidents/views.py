from django.contrib import messages
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import OuterRef, Q, Subquery
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import Incident, IncidentHistory
from accounts.permissions import CanModifyIncident
from residents.models import Resident
from structure.models import Apartment
from .serializers import (
    IncidentListSerializer, IncidentDetailSerializer,
    IncidentHistorySerializer
)
from .forms import IncidentForm, IncidentImageForm, IncidentHistoryForm

PAGINATE_BY = 15


def _ultimo_comentario_subquery():
    return (
        IncidentHistory.objects.filter(incident=OuterRef('pk'))
        .order_by('-created_at')
        .values('comment')[:1]
    )


# @login_required
def app_index(request):
    incidencias_qs = (
        Incident.objects
        .select_related('apartment__building', 'resident')
        .annotate(ultimo_comentario=Subquery(_ultimo_comentario_subquery()))
        .order_by('-created_at')
    )

    estado = request.GET.get('estado', '')
    apartamento = request.GET.get('apartamento', '')
    residente = request.GET.get('residente', '')

    if estado:
        incidencias_qs = incidencias_qs.filter(status=estado)
    if apartamento:
        incidencias_qs = incidencias_qs.filter(apartment_id=apartamento)
    if residente:
        incidencias_qs = incidencias_qs.filter(resident_id=residente)

    paginator = Paginator(incidencias_qs, PAGINATE_BY)
    pagina = request.GET.get('page')
    try:
        incidencias = paginator.page(pagina)
    except PageNotAnInteger:
        incidencias = paginator.page(1)
    except EmptyPage:
        incidencias = paginator.page(paginator.num_pages)

    query = request.GET.copy()
    query.pop('page', None)

    contexto = {
        'incidencias': incidencias,
        'apartamentos': Apartment.objects.filter(is_active=True),
        'residentes': Resident.objects.select_related('apartment').all(),
        'estado_actual': estado,
        'apartamento_actual': apartamento,
        'residente_actual': residente,
        'paginacion_query': query.urlencode(),
        'module_name': 'Incidencias',
    }
    return render(request, 'incidents/index.html', contexto)


def _guardar_incidencia(request, form, incidencia=None):
    """Guarda la incidencia y registra el comentario como historial."""
    es_nueva = incidencia is None
    estado_previo = None if es_nueva else incidencia.status
    registro = form.save(commit=False)
    if es_nueva:
        registro.reported_by = request.user
        if not registro.title:
            base = f"{registro.get_category_display()}: {registro.description}"
            registro.title = base[:200]
    registro.save()
    comentario = form.cleaned_data.get('comment')
    if comentario and request.user.is_authenticated:
        IncidentHistory.objects.create(
            incident=registro,
            status_from=estado_previo,
            status_to=registro.status,
            changed_by=request.user,
            comment=comentario,
        )
    return registro


# @login_required
def agregar_incidencia(request):
    if request.method == 'POST':
        form = IncidentForm(request.POST, request.FILES)
        if form.is_valid():
            _guardar_incidencia(request, form)
            messages.success(request, 'Incidencia creada correctamente.')
            return redirect('incidencias_index')
        messages.error(request, 'No se pudo crear la incidencia. Revisa los datos enviados.')
    else:
        form = IncidentForm()

    contexto = {
        'form_incident': form,
        'residentes': Resident.objects.select_related('apartment').all(),
        'module_name': 'Incidencias',
        'titulo_modulo': 'Agregar incidencia',
        'url_form': 'agregar_incidencia',
        'url_form_args': [],
        'texto_boton': 'Agregar',
    }
    return render(request, 'incidents/agregar.html', contexto)


# @login_required
def actualizar_incidencia(request, pk):
    incidencia = Incident.objects.filter(pk=pk).first()
    if not incidencia:
        messages.error(request, 'Incidencia no encontrada.')
        return redirect('incidencias_index')

    if request.method == 'POST':
        form = IncidentForm(request.POST, request.FILES, instance=incidencia)
        if form.is_valid():
            _guardar_incidencia(request, form, incidencia)
            messages.success(request, 'Incidencia actualizada correctamente.')
            return redirect('incidencias_index')
        messages.error(request, 'No se pudo actualizar la incidencia. Revisa los datos enviados.')
    else:
        form = IncidentForm(instance=incidencia)

    contexto = {
        'form_incident': form,
        'incidencia': incidencia,
        'residentes': Resident.objects.select_related('apartment').all(),
        'module_name': 'Incidencias',
        'titulo_modulo': 'Actualizar incidencia',
        'url_form': 'actualizar_incidencia',
        'url_form_args': [str(incidencia.id)],
        'texto_boton': 'Actualizar',
    }
    return render(request, 'incidents/agregar.html', contexto)


# @login_required
@require_POST
def eliminar_incidencia(request, pk):
    incidencia = Incident.objects.filter(pk=pk).first()
    if not incidencia:
        messages.error(request, 'Incidencia no encontrada.')
        return redirect('incidencias_index')

    detalle = f'{incidencia.get_category_display()} - {incidencia.apartment.name}'
    incidencia.delete()
    messages.success(request, f'Incidencia {detalle} eliminada correctamente.')
    return redirect('incidencias_index')


# @login_required
@require_POST
def crear_imagen_incidencia(request):
    form = IncidentImageForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, 'Imagen de incidencia agregada correctamente.')
    else:
        messages.error(request, 'No se pudo agregar la imagen. Revisa los datos enviados.')
    return redirect('incidencias_index')


# @login_required
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
    return redirect('incidencias_index')


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
