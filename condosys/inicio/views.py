<<<<<<< HEAD
from django.db.models import Q
from django.http import Http404
from django.shortcuts import redirect
from django.views.generic import ListView
=======
from django.shortcuts import render
>>>>>>> cec7002f1e7cce511dcba6ae432c0537b7500b19

from incidents.models import Incident
from payments.models import Payment
from reservations.models import Reservation
from structure.models import Apartment

ESTADOS_INCIDENCIA_ABIERTA = ['new', 'assigned', 'in_progress']
ESTADOS_PAGO_PENDIENTE = ['pending', 'at_risk', 'overdue']
LIMITE_PAGOS_POR_VENCER = 5
LIMITE_ACTIVIDAD = 5


<<<<<<< HEAD
class InicioView(ListView):
    template_name = 'inicio/index.html'
    context_object_name = 'residentes'
    model = Resident
    paginate_by = 10
=======
# @login_required
def app_index(request):
    """Panel de inicio: conteos, pagos pendientes por vencer y actividad reciente."""
    pagos_pendientes_qs = Payment.objects.filter(status__in=ESTADOS_PAGO_PENDIENTE)
>>>>>>> cec7002f1e7cce511dcba6ae432c0537b7500b19

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

<<<<<<< HEAD
        return qs

    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except Http404:
            query = request.GET.copy()
            query.pop('page', None)
            url = request.path
            if query:
                url += '?' + query.urlencode()
            return redirect(url)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['jardines'] = Garden.objects.filter(is_active=True)
        ctx['edificios'] = Building.objects.filter(is_active=True)
        ctx['departamentos'] = Apartment.objects.filter(is_active=True)
        ctx['search_actual'] = self.request.GET.get('search', '')
        ctx['garden_actual'] = self.request.GET.get('garden', '')
        ctx['building_actual'] = self.request.GET.get('building', '')
        ctx['apartment_actual'] = self.request.GET.get('apartment', '')
        query = self.request.GET.copy()
        query.pop('page', None)
        ctx['paginacion_query'] = query.urlencode()
        ctx['total_departamentos'] = Apartment.objects.filter(is_active=True).count()
        ctx['total_residentes'] = Resident.objects.filter(is_active=True).count()
        ctx['total_pagos'] = Payment.objects.count()
        ctx['total_visitantes'] = Visitor.objects.count()
        return ctx
=======
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
>>>>>>> cec7002f1e7cce511dcba6ae432c0537b7500b19
