from django.contrib import messages
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import CommonArea, Reservation
from residents.models import Resident
from structure.models import Apartment
from areas_comunes.models import AreaComun
from .serializers import (
    CommonAreaSerializer, ReservationListSerializer,
    ReservationDetailSerializer
)
from .forms import CommonAreaForm, ReservationForm

PAGINATE_BY = 15


@login_required
def app_index(request):
    reservas_qs = (
        Reservation.objects
        .select_related('common_area', 'apartment__building', 'resident')
        .order_by('-start_time')
    )

    estado = request.GET.get('estado', '')
    apartamento = request.GET.get('apartamento', '')

    if estado:
        reservas_qs = reservas_qs.filter(status=estado)
    if apartamento:
        reservas_qs = reservas_qs.filter(apartment_id=apartamento)

    paginator = Paginator(reservas_qs, PAGINATE_BY)
    pagina = request.GET.get('page')
    try:
        reservas = paginator.page(pagina)
    except PageNotAnInteger:
        reservas = paginator.page(1)
    except EmptyPage:
        reservas = paginator.page(paginator.num_pages)

    query = request.GET.copy()
    query.pop('page', None)

    contexto = {
        'reservas': reservas,
        'apartamentos': Apartment.objects.filter(is_active=True).order_by('name'),
        'estados_reserva': Reservation.STATUS_CHOICES,
        'estado_actual': estado,
        'apartamento_actual': apartamento,
        'paginacion_query': query.urlencode(),
        'module_name': 'Reservas',
    }
    return render(request, 'reservations/index.html', contexto)


def _contexto_formulario():
    return {
        'areas': AreaComun.objects.filter(status='activo'),
        'residentes': Resident.objects.select_related('apartment').all(),
        'module_name': 'Reservas',
    }


@login_required
def agregar_reserva(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Reserva creada correctamente.')
            return redirect('reservas_index')
        messages.error(request, 'No se pudo crear la reserva. Revisa los datos enviados.')
    else:
        form = ReservationForm()

    contexto = _contexto_formulario() | {
        'form_reservation': form,
        'titulo_modulo': 'Agregar reserva',
        'url_form': 'agregar_reserva',
        'url_form_args': [],
        'texto_boton': 'Agregar',
    }
    return render(request, 'reservations/agregar.html', contexto)


@login_required
def actualizar_reserva(request, pk):
    reserva = Reservation.objects.filter(pk=pk).first()
    if not reserva:
        messages.error(request, 'Reserva no encontrada.')
        return redirect('reservas_index')

    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=reserva)
        if form.is_valid():
            form.save()
            messages.success(request, 'Reserva actualizada correctamente.')
            return redirect('reservas_index')
        messages.error(request, 'No se pudo actualizar la reserva. Revisa los datos enviados.')
    else:
        form = ReservationForm(instance=reserva)

    contexto = _contexto_formulario() | {
        'form_reservation': form,
        'titulo_modulo': 'Actualizar reserva',
        'url_form': 'actualizar_reserva',
        'url_form_args': [str(reserva.id)],
        'texto_boton': 'Actualizar',
    }
    return render(request, 'reservations/agregar.html', contexto)


@login_required
@require_POST
def eliminar_reserva(request, pk):
    reserva = Reservation.objects.filter(pk=pk).first()
    if not reserva:
        messages.error(request, 'Reserva no encontrada.')
        return redirect('reservas_index')

    detalle = f'{reserva.common_area.name} - {reserva.start_time:%d/%m/%Y %H:%M}'
    reserva.delete()
    messages.success(request, f'Reserva {detalle} eliminada correctamente.')
    return redirect('reservas_index')


@login_required
@require_POST
def crear_area_comun(request):
    form = CommonAreaForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, 'Área común creada correctamente.')
    else:
        messages.error(request, 'No se pudo crear el área común. Revisa los datos enviados.')
    return redirect('inicio')


class CommonAreaViewSet(viewsets.ModelViewSet):
    """ViewSet para CommonArea"""
    queryset = CommonArea.objects.filter(is_active=True)
    serializer_class = CommonAreaSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    filterset_fields = ['garden']


class ReservationViewSet(viewsets.ModelViewSet):
    """ViewSet para Reservation"""
    queryset = Reservation.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['reserved_by__email', 'common_area__name']
    ordering_fields = ['start_time', 'status']
    ordering = ['-start_time']
    filterset_fields = ['common_area', 'status', 'reserved_by']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ReservationDetailSerializer
        return ReservationListSerializer
