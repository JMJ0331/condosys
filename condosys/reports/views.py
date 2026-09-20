import csv
from datetime import datetime
from decimal import Decimal

from django.db.models import Count, Q, Sum
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import AuditLog
from .serializers import AuditLogSerializer
from residencial.models import Residencial
from structure.models import Apartment, Building
from residents.models import Resident
from payments.models import Payment
from incidents.models import Incident
from visitors.models import Visitor
from reservations.models import Reservation
from .forms import AuditLogForm, AuditLogDetailForm


TIPOS_REPORTE = [
    ('apartamentos', 'Apartamentos ocupados / disponibles'),
    ('residentes', 'Residentes activos'),
    ('pagos_realizados', 'Pagos realizados'),
    ('pagos_pendientes', 'Pagos pendientes'),
    ('morosidad', 'Morosidad'),
    ('incidencias', 'Incidencias por estado'),
    ('visitas', 'Visitas registradas'),
    ('reservas', 'Reservas de áreas comunes'),
    ('ingresos', 'Ingresos mensuales'),
]

MESES_CORTO = {
    1: 'Ene', 2: 'Feb', 3: 'Mar', 4: 'Abr',
    5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Ago',
    9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dic',
}

MESES_NOMBRE = {
    1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril',
    5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto',
    9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre',
}

ESTADOS_MOROSIDAD = ['overdue', 'at_risk']
ESTADOS_INCIDENCIA_ABIERTA = ['new', 'assigned', 'in_progress']
LIMITE_FILAS = 200


def _parse_fecha(valor):
    """Convierte 'YYYY-MM-DD' a date; devuelve None si es vacío o inválido."""
    if not valor:
        return None
    try:
        return datetime.strptime(valor, '%Y-%m-%d').date()
    except ValueError:
        return None


def _etiquetas_edificio():
    """Etiquetas singular/plural según la distribución del residencial."""
    residencial = Residencial.obtener_unico()
    distribucion = getattr(residencial, 'distribucion', '') or ''
    if distribucion == 'edificios':
        return 'Edificio', 'edificios', 'Todos los edificios'
    return 'Torre', 'torres', 'Todas las torres'


def _filtrar_por_edificio(queryset, edificio_id, ruta='apartment__building_id'):
    if edificio_id:
        return queryset.filter(**{ruta: edificio_id})
    return queryset


def _aplicar_rango(queryset, campo, desde, hasta):
    if desde:
        queryset = queryset.filter(**{f'{campo}__gte': desde})
    if hasta:
        queryset = queryset.filter(**{f'{campo}__lte': hasta})
    return queryset


def _formatear_monto(valor):
    try:
        total = float(valor or 0)
    except (TypeError, ValueError):
        total = 0
    return f'RD$ {total:,.0f}'.replace(',', '.')


def _meses_entre(desde, hasta, maximo=12):
    """Meses (anio, mes) entre dos fechas, capado a `maximo`."""
    meses = []
    anio, mes = desde.year, desde.month
    while (anio, mes) <= (hasta.year, hasta.month) and len(meses) < maximo:
        meses.append((anio, mes))
        mes += 1
        if mes > 12:
            mes = 1
            anio += 1
    return meses or [(hasta.year, hasta.month)]


def _ultimos_meses(cantidad=7):
    hoy = timezone.localdate()
    meses = []
    anio, mes = hoy.year, hoy.month
    for _ in range(cantidad):
        meses.append((anio, mes))
        mes -= 1
        if mes < 1:
            mes = 12
            anio -= 1
    return list(reversed(meses))


def _ingresos_por_mes(meses, edificio_id=None):
    """Total pagado y conteo por mes usando fecha de pago (o periodo)."""
    pagados = Payment.objects.filter(status='paid').select_related('apartment__building')
    if edificio_id:
        pagados = pagados.filter(apartment__building_id=edificio_id)
    movimientos = pagados.values_list('payment_date', 'period', 'amount')
    acumulados = {(anio, mes): [0, Decimal('0')] for anio, mes in meses}
    for fecha_pago, periodo, monto in movimientos:
        efectiva = fecha_pago or periodo
        if efectiva is None:
            continue
        clave = (efectiva.year, efectiva.month)
        if clave in acumulados:
            acumulados[clave][0] += 1
            acumulados[clave][1] += monto or Decimal('0')
    barras = []
    maximo = max((float(total) for _, total in acumulados.values()), default=0)
    for anio, mes in meses:
        conteo, total = acumulados[(anio, mes)]
        total_f = float(total)
        altura = round(total_f / maximo * 100) if maximo > 0 else 0
        if total_f > 0 and altura < 4:
            altura = 4
        barras.append({
            'etiqueta': MESES_CORTO[mes],
            'nombre': f'{MESES_NOMBRE[mes]} {anio}',
            'total': total_f,
            'total_texto': _formatear_monto(total_f),
            'total_corto': f'RD$ {total_f / 1000:,.0f}k'.replace(',', '.'),
            'pagos': conteo,
            'altura': altura,
        })
    return barras


def _construir_vista(tipo, desde, hasta, edificio_id, etiqueta_singular):
    """Devuelve columnas, filas y datos de gráfico según el tipo de reporte."""
    columnas, filas, grafico, resumen = [], [], None, None

    if tipo == 'apartamentos':
        qs = Apartment.objects.select_related('building__garden', 'owner').order_by('building__name', 'name')
        qs = _filtrar_por_edificio(qs, edificio_id, ruta='building_id')
        qs = _aplicar_rango(qs, 'created_at__date', desde, hasta)
        columnas = ['Departamento', etiqueta_singular, 'Piso', 'Estado']
        for apto in qs[:LIMITE_FILAS]:
            filas.append([
                apto.name,
                apto.building.name,
                str(apto.floor) if apto.floor is not None else '—',
                apto.get_status_display(),
            ])

    elif tipo == 'residentes':
        qs = Resident.objects.select_related('apartment__building').filter(is_active=True).order_by('full_name')
        qs = _filtrar_por_edificio(qs, edificio_id)
        qs = _aplicar_rango(qs, 'created_at__date', desde, hasta)
        columnas = ['Residente', 'Departamento', etiqueta_singular, 'Relación', 'Teléfono']
        for residente in qs[:LIMITE_FILAS]:
            filas.append([
                residente.full_name,
                residente.apartment.name,
                residente.apartment.building.name,
                residente.get_tipo_relacion_display(),
                residente.phone or '—',
            ])

    elif tipo in ('pagos_realizados', 'pagos_pendientes', 'morosidad'):
        qs = Payment.objects.select_related('apartment__building', 'resident').order_by('-payment_date', '-period')
        qs = _filtrar_por_edificio(qs, edificio_id)
        if tipo == 'pagos_realizados':
            qs = _aplicar_rango(qs.filter(status='paid'), 'payment_date', desde, hasta)
            columnas = ['Departamento', 'Residente', 'Concepto', 'Monto', 'Fecha de pago', 'Periodo']
        elif tipo == 'pagos_pendientes':
            qs = _aplicar_rango(qs.filter(status='pending'), 'period', desde, hasta)
            columnas = ['Departamento', 'Residente', 'Concepto', 'Monto', 'Periodo', 'Estado']
        else:
            qs = _aplicar_rango(qs.filter(status__in=ESTADOS_MOROSIDAD), 'period', desde, hasta)
            columnas = ['Departamento', 'Residente', 'Concepto', 'Monto', 'Periodo', 'Estado']
        for pago in qs[:LIMITE_FILAS]:
            filas.append([
                pago.apartment.name,
                pago.resident.full_name,
                pago.get_concept_display(),
                _formatear_monto(pago.amount),
                pago.payment_date.strftime('%d/%m/%Y') if pago.payment_date else '—',
                pago.period.strftime('%d/%m/%Y') if pago.period else '—',
            ] if tipo == 'pagos_realizados' else [
                pago.apartment.name,
                pago.resident.full_name,
                pago.get_concept_display(),
                _formatear_monto(pago.amount),
                pago.period.strftime('%d/%m/%Y') if pago.period else '—',
                pago.get_status_display(),
            ])

    elif tipo == 'incidencias':
        qs = Incident.objects.select_related('apartment__building').order_by('-reported_date', '-created_at')
        qs = _filtrar_por_edificio(qs, edificio_id)
        qs = _aplicar_rango(qs, 'reported_date', desde, hasta)
        columnas = ['Título', 'Departamento', 'Categoría', 'Prioridad', 'Estado', 'Reportada']
        for incidencia in qs[:LIMITE_FILAS]:
            filas.append([
                incidencia.title,
                incidencia.apartment.name,
                incidencia.get_category_display(),
                incidencia.get_priority_display(),
                incidencia.get_status_display(),
                incidencia.reported_date.strftime('%d/%m/%Y') if incidencia.reported_date else '—',
            ])

    elif tipo == 'visitas':
        qs = Visitor.objects.select_related('apartment__building').order_by('-scheduled_entry')
        qs = _filtrar_por_edificio(qs, edificio_id)
        qs = _aplicar_rango(qs, 'scheduled_entry__date', desde, hasta)
        columnas = ['Visitante', 'Departamento', 'Tipo', 'Entrada', 'Salida', 'Estado']
        for visita in qs[:LIMITE_FILAS]:
            filas.append([
                visita.name,
                visita.apartment.name,
                visita.get_type_display(),
                visita.scheduled_entry.strftime('%d/%m/%Y %H:%M'),
                visita.scheduled_exit.strftime('%d/%m/%Y %H:%M') if visita.scheduled_exit else '—',
                visita.get_status_display(),
            ])

    elif tipo == 'reservas':
        qs = Reservation.objects.select_related('common_area', 'apartment__building').order_by('-start_time')
        qs = _filtrar_por_edificio(qs, edificio_id)
        qs = _aplicar_rango(qs, 'start_time__date', desde, hasta)
        columnas = ['Área común', 'Departamento', 'Inicio', 'Fin', 'Estado']
        for reserva in qs[:LIMITE_FILAS]:
            filas.append([
                reserva.common_area.name,
                reserva.apartment.name if reserva.apartment else '—',
                reserva.start_time.strftime('%d/%m/%Y %H:%M'),
                reserva.end_time.strftime('%d/%m/%Y %H:%M'),
                reserva.get_status_display(),
            ])

    else:
        if desde and hasta and desde <= hasta:
            meses = _meses_entre(desde, hasta)
            subtitulo = 'Rango seleccionado · RD$'
        else:
            meses = _ultimos_meses(7)
            subtitulo = 'Últimos 7 meses · RD$'
        barras = _ingresos_por_mes(meses, edificio_id)
        grafico = {'barras': barras, 'subtitulo': subtitulo}
        columnas = ['Mes', 'Pagos recibidos', 'Total']
        for barra in barras:
            filas.append([barra['nombre'], str(barra['pagos']), barra['total_texto']])
        ultima = barras[-1] if barras else None
        if ultima:
            resumen = {
                'mes': ultima['nombre'],
                'pagos': ultima['pagos'],
                'total': ultima['total_texto'],
            }

    return columnas, filas, grafico, resumen


def _respuesta_csv(tipo_clave, tipo_etiqueta, columnas, filas):
    respuesta = HttpResponse(content_type='text/csv; charset=utf-8')
    respuesta['Content-Disposition'] = f'attachment; filename="reporte-{tipo_clave}.csv"'
    respuesta.write('﻿')
    escritor = csv.writer(respuesta)
    escritor.writerow([f'Reporte: {tipo_etiqueta}'])
    escritor.writerow(columnas)
    for fila in filas:
        escritor.writerow(fila)
    return respuesta


# @login_required
def app_index(request):
    tipos = dict(TIPOS_REPORTE)
    tipo = request.GET.get('tipo', 'ingresos')
    if tipo not in tipos:
        tipo = 'ingresos'
    desde = _parse_fecha(request.GET.get('desde', ''))
    hasta = _parse_fecha(request.GET.get('hasta', ''))
    edificio_id = request.GET.get('edificio', '')
    if desde and hasta and desde > hasta:
        desde, hasta = hasta, desde

    singular, plural, placeholder_todas = _etiquetas_edificio()
    edificios = Building.objects.filter(is_active=True).order_by('name')

    hoy = timezone.localdate()
    pagados_mes = Payment.objects.filter(status='paid').filter(
        Q(payment_date__year=hoy.year, payment_date__month=hoy.month)
        | Q(payment_date__isnull=True, period__year=hoy.year, period__month=hoy.month)
    )
    ingresos_mes = pagados_mes.aggregate(total=Sum('amount'))['total'] or 0
    morosidad = Payment.objects.filter(status__in=ESTADOS_MOROSIDAD).aggregate(total=Sum('amount'))['total'] or 0
    total_apartamentos = Apartment.objects.count()
    ocupados = Apartment.objects.filter(status='occupied').count()
    ocupacion = round(ocupados / total_apartamentos * 100) if total_apartamentos else 0
    incidencias_abiertas = Incident.objects.filter(status__in=ESTADOS_INCIDENCIA_ABIERTA).count()

    columnas, filas, grafico, resumen = _construir_vista(
        tipo,
        desde,
        hasta,
        edificio_id or None,
        singular,
    )

    if request.GET.get('formato') == 'csv':
        return _respuesta_csv(tipo, tipos[tipo], columnas, filas)

    contexto = {
        'module_name': 'Reportes',
        'tipos': TIPOS_REPORTE,
        'tipo_actual': tipo,
        'tipo_etiqueta': tipos[tipo],
        'desde_actual': desde.strftime('%Y-%m-%d') if desde else '',
        'hasta_actual': hasta.strftime('%Y-%m-%d') if hasta else '',
        'edificio_actual': edificio_id or '',
        'edificios': edificios,
        'etiqueta_singular': singular,
        'etiqueta_plural': plural,
        'placeholder_todas': placeholder_todas,
        'kpi_ingresos_mes': _formatear_monto(ingresos_mes),
        'kpi_morosidad': _formatear_monto(morosidad),
        'kpi_ocupacion': f'{ocupacion}%',
        'kpi_incidencias': incidencias_abiertas,
        'columnas': columnas,
        'filas': filas,
        'grafico': grafico,
        'resumen': resumen,
    }
    return render(request, 'reports/index.html', contexto)


# @login_required
@require_POST
def crear_audit_log(request):
    form = AuditLogForm(request.POST)
    if form.is_valid():
        log = form.save(commit=False)
        log.user = request.user
        log.save()
        messages.success(request, 'Registro de auditoría creado correctamente.')
    else:
        messages.error(request, 'No se pudo crear el registro. Revisa los datos enviados.')
    return redirect('inicio')


# @login_required
@require_POST
def crear_audit_log_detail(request):
    form = AuditLogDetailForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, 'Detalle de auditoría agregado correctamente.')
    else:
        messages.error(request, 'No se pudo agregar el detalle. Revisa los datos enviados.')
    return redirect('inicio')


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    permission_classes = [IsAuthenticated]


class ReportViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def summary(self, request):
        data = {
            'apartments_total': Apartment.objects.count(),
            'apartments_occupied': Apartment.objects.filter(status='occupied').count(),
            'apartments_available': Apartment.objects.filter(status='empty').count(),
            'active_residents': Resident.objects.filter(is_active=True).count(),
            'payments_total': Payment.objects.count(),
            'payments_pending': Payment.objects.filter(status='pending').count(),
            'payments_overdue': Payment.objects.filter(status='overdue').count(),
            'incidents_total': Incident.objects.count(),
            'incidents_open': Incident.objects.filter(status__in=['new', 'assigned', 'in_progress']).count(),
            'visitors_total': Visitor.objects.count(),
            'reservations_total': Reservation.objects.count(),
            'reservations_pending': Reservation.objects.filter(status='requested').count(),
            'monthly_income': Payment.objects.filter(status='paid').aggregate(total=Sum('amount'))['total'] or 0,
        }
        return Response(data)

    @action(detail=False, methods=['get'])
    def payments(self, request):
        queryset = Payment.objects.all()
        apartment = request.query_params.get('apartment')
        status_param = request.query_params.get('status')
        month = request.query_params.get('month')
        year = request.query_params.get('year')

        if apartment:
            queryset = queryset.filter(apartment_id=apartment)
        if status_param:
            queryset = queryset.filter(status=status_param)
        if month:
            queryset = queryset.filter(period__month=month)
        if year:
            queryset = queryset.filter(period__year=year)

        data = queryset.values('status').annotate(count=Count('id'), total=Sum('amount')).order_by('status')
        return Response(data)

    @action(detail=False, methods=['get'])
    def occupancy(self, request):
        data = Apartment.objects.values('status').annotate(count=Count('id')).order_by('status')
        return Response(data)
