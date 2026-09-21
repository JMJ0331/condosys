from django.contrib import messages
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from structure.models import Apartment
from .models import MaintenanceCharge
from .serializers import (
    MaintenanceChargeListSerializer,
    MaintenanceChargeDetailSerializer
)
from .forms import MaintenanceChargeForm

PAGINATE_BY = 15


def _anios_con_cargos():
    """Años con cargos registrados (desc), incluyendo el año actual."""
    anios = {fecha.year for fecha in MaintenanceCharge.objects.dates('effective_date', 'year')}
    anios.add(timezone.localdate().year)
    return sorted(anios, reverse=True)


MESES_NOMBRE = {
    1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril',
    5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto',
    9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre',
}


# @login_required
def app_index(request):
    cargos_qs = (
        MaintenanceCharge.objects
        .select_related('apartment__building')
        .order_by('-effective_date', '-created_at')
    )

    estado = request.GET.get('estado', '')
    apartamento = request.GET.get('apartamento', '')
    mes = request.GET.get('mes', '')
    anio = request.GET.get('anio', '')

    if estado == 'activo':
        cargos_qs = cargos_qs.filter(is_active=True)
    elif estado == 'inactivo':
        cargos_qs = cargos_qs.filter(is_active=False)
    if apartamento:
        cargos_qs = cargos_qs.filter(apartment_id=apartamento)
    if mes.isdigit() and 1 <= int(mes) <= 12:
        cargos_qs = cargos_qs.filter(effective_date__month=int(mes))
    else:
        mes = ''
    if anio.isdigit():
        cargos_qs = cargos_qs.filter(effective_date__year=int(anio))
    else:
        anio = ''

    paginator = Paginator(cargos_qs, PAGINATE_BY)
    pagina = request.GET.get('page')
    try:
        cargos = paginator.page(pagina)
    except PageNotAnInteger:
        cargos = paginator.page(1)
    except EmptyPage:
        cargos = paginator.page(paginator.num_pages)

    query = request.GET.copy()
    query.pop('page', None)

    contexto = {
        'cargos': cargos,
        'apartamentos': Apartment.objects.filter(is_active=True),
        'estado_actual': estado,
        'apartamento_actual': apartamento,
        'mes_actual': mes,
        'anio_actual': anio,
        'mes_actual_nombre': MESES_NOMBRE.get(int(mes), 'Todos los meses') if mes else 'Todos los meses',
        'anios': _anios_con_cargos(),
        'paginacion_query': query.urlencode(),
        'module_name': 'Mantenimientos',
    }
    return render(request, 'maintenance/index.html', contexto)


# @login_required
def agregar_mantenimiento(request):
    if request.method == 'POST':
        form = MaintenanceChargeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cargo de mantenimiento creado correctamente.')
            return redirect('mantenimientos_index')
        messages.error(request, 'No se pudo crear el cargo. Revisa los datos enviados.')
    else:
        form = MaintenanceChargeForm()

    contexto = {
        'form_cargo': form,
        'module_name': 'Mantenimientos',
        'titulo_modulo': 'Agregar mantenimiento',
        'url_form': 'agregar_mantenimiento',
        'url_form_args': [],
        'texto_boton': 'Agregar',
    }
    return render(request, 'maintenance/agregar.html', contexto)


# @login_required
def actualizar_mantenimiento(request, pk):
    cargo = MaintenanceCharge.objects.filter(pk=pk).first()
    if not cargo:
        messages.error(request, 'Cargo de mantenimiento no encontrado.')
        return redirect('mantenimientos_index')

    if request.method == 'POST':
        form = MaintenanceChargeForm(request.POST, request.FILES, instance=cargo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cargo de mantenimiento actualizado correctamente.')
            return redirect('mantenimientos_index')
        messages.error(request, 'No se pudo actualizar el cargo. Revisa los datos enviados.')
    else:
        form = MaintenanceChargeForm(instance=cargo)

    contexto = {
        'form_cargo': form,
        'cargo': cargo,
        'module_name': 'Mantenimientos',
        'titulo_modulo': 'Actualizar mantenimiento',
        'url_form': 'actualizar_mantenimiento',
        'url_form_args': [str(cargo.id)],
        'texto_boton': 'Actualizar',
    }
    return render(request, 'maintenance/agregar.html', contexto)


# @login_required
@require_POST
def eliminar_mantenimiento(request, pk):
    cargo = MaintenanceCharge.objects.filter(pk=pk).first()
    if not cargo:
        messages.error(request, 'Cargo de mantenimiento no encontrado.')
        return redirect('mantenimientos_index')

    detalle = f'{cargo.get_concept_display()} - {cargo.amount}'
    cargo.delete()
    messages.success(request, f'Cargo {detalle} eliminado correctamente.')
    return redirect('mantenimientos_index')


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
