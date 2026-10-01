from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from accounts.permissions import ROLES_RESIDENTE
from accounts.decorators import role_required
from incidents.models import Incident
from payments.models import Payment
from reservations.models import Reservation
from structure.models import Apartment

ESTADOS_INCIDENCIA_ABIERTA = ['new', 'assigned', 'in_progress']
ESTADOS_PAGO_PENDIENTE = ['pending', 'at_risk', 'overdue']
LIMITE_PAGOS_POR_VENCER = 5
LIMITE_ACTIVIDAD = 5


@role_required(*ROLES_RESIDENTE)
def app_index(request):
    """Panel de inicio: conteos, pagos pendientes por vencer y actividad reciente."""
    pagos_pendientes_qs = Payment.objects.filter(status__in=ESTADOS_PAGO_PENDIENTE)

    contexto = {
        'total_departamentos': Apartment.objects.filter(is_active=True).count(),
        'incidencias_abiertas': Incident.objects.filter(status__in=ESTADOS_INCIDENCIA_ABIERTA).count(),
        'pagos_pendientes': pagos_pendientes_qs.count(),
        'reservas_pendientes': Reservation.objects.filter(status='requested').count(),
        'pagos_por_vencer': (
            pagos_pendientes_qs
            .select_related('apartment', 'resident')
            .order_by('period')[:LIMITE_PAGOS_POR_VENCER]
        ),
        'actividad_reciente': _actividad_reciente(),
    }
    return render(request, 'inicio/index.html', contexto)


def _actividad_reciente():
    """Últimos pagos e incidencias de todos los usuarios (incluye admin/manager)."""
    pagos = (
        Payment.objects.select_related('resident', 'apartment', 'registered_by')
        .order_by('-created_at')[:LIMITE_ACTIVIDAD]
    )
    incidencias = (
        Incident.objects.select_related('apartment__building', 'reported_by')
        .order_by('-created_at')[:LIMITE_ACTIVIDAD]
    )

    actividad = [
        {
            'tipo': 'pago',
            'texto': f'{pago.resident.full_name} registró un pago.',
            'fecha': pago.created_at,
        }
        for pago in pagos
    ]
    actividad += [
        {
            'tipo': 'incidencia',
            'texto': (
                'Nueva incidencia reportada en '
                f'{incidencia.apartment.building.tower or incidencia.apartment.building.name} '
                f'{incidencia.apartment.name}.'
            ),
            'fecha': incidencia.created_at,
        }
        for incidencia in incidencias
    ]
    actividad.sort(key=lambda item: item['fecha'], reverse=True)
    return actividad[:LIMITE_ACTIVIDAD]
