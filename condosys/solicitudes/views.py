from django.contrib import messages
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from residents.models import Resident
from structure.models import Apartment
from .models import Solicitud
from .serializers import SolicitudSerializer
from .forms import SolicitudForm

PAGINATE_BY = 15


# @login_required
def app_index(request):
    solicitudes_qs = (
        Solicitud.objects
        .select_related('apartment__building', 'resident')
        .order_by('-created_at')
    )

    estado = request.GET.get('estado', '')
    apartamento = request.GET.get('apartamento', '')
    residente = request.GET.get('residente', '')

    if estado:
        solicitudes_qs = solicitudes_qs.filter(status=estado)
    if apartamento:
        solicitudes_qs = solicitudes_qs.filter(apartment_id=apartamento)
    if residente:
        solicitudes_qs = solicitudes_qs.filter(resident_id=residente)

    paginator = Paginator(solicitudes_qs, PAGINATE_BY)
    pagina = request.GET.get('page')
    try:
        solicitudes = paginator.page(pagina)
    except PageNotAnInteger:
        solicitudes = paginator.page(1)
    except EmptyPage:
        solicitudes = paginator.page(paginator.num_pages)

    query = request.GET.copy()
    query.pop('page', None)

    contexto = {
        'solicitudes': solicitudes,
        'apartamentos': Apartment.objects.filter(is_active=True),
        'residentes': Resident.objects.select_related('apartment').all(),
        'estado_actual': estado,
        'apartamento_actual': apartamento,
        'residente_actual': residente,
        'paginacion_query': query.urlencode(),
        'module_name': 'Solicitudes',
    }
    return render(request, 'solicitudes/index.html', contexto)


# @login_required
def agregar_solicitud(request):
    if request.method == 'POST':
        form = SolicitudForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Solicitud creada correctamente.')
            return redirect('solicitudes_index')
        messages.error(request, 'No se pudo crear la solicitud. Revisa los datos enviados.')
    else:
        form = SolicitudForm()

    contexto = {
        'form_solicitud': form,
        'residentes': Resident.objects.select_related('apartment').all(),
        'module_name': 'Solicitudes',
        'titulo_modulo': 'Agregar solicitud',
        'url_form': 'agregar_solicitud',
        'url_form_args': [],
        'texto_boton': 'Agregar',
    }
    return render(request, 'solicitudes/agregar.html', contexto)


# @login_required
def actualizar_solicitud(request, pk):
    solicitud = Solicitud.objects.filter(pk=pk).first()
    if not solicitud:
        messages.error(request, 'Solicitud no encontrada.')
        return redirect('solicitudes_index')

    if request.method == 'POST':
        form = SolicitudForm(request.POST, request.FILES, instance=solicitud)
        if form.is_valid():
            form.save()
            messages.success(request, 'Solicitud actualizada correctamente.')
            return redirect('solicitudes_index')
        messages.error(request, 'No se pudo actualizar la solicitud. Revisa los datos enviados.')
    else:
        form = SolicitudForm(instance=solicitud)

    contexto = {
        'form_solicitud': form,
        'solicitud': solicitud,
        'residentes': Resident.objects.select_related('apartment').all(),
        'module_name': 'Solicitudes',
        'titulo_modulo': 'Actualizar solicitud',
        'url_form': 'actualizar_solicitud',
        'url_form_args': [str(solicitud.id)],
        'texto_boton': 'Actualizar',
    }
    return render(request, 'solicitudes/agregar.html', contexto)


# @login_required
@require_POST
def eliminar_solicitud(request, pk):
    solicitud = Solicitud.objects.filter(pk=pk).first()
    if not solicitud:
        messages.error(request, 'Solicitud no encontrada.')
        return redirect('solicitudes_index')

    detalle = f'{solicitud.get_request_type_display()} - {solicitud.apartment.name}'
    solicitud.delete()
    messages.success(request, f'Solicitud {detalle} eliminada correctamente.')
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
