from decimal import Decimal, InvalidOperation
from io import BytesIO

from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    HRFlowable,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import Payment
from .serializers import PaymentSerializer
from .forms import PaymentForm
from residents.models import Resident
from propietarios.models import Propietario
from structure.models import Apartment


PAGINATE_BY = 15


# @login_required
def app_index(request):
    pagos_qs = (
        Payment.objects.select_related(
            'apartment__building__garden', 'resident', 'registered_by'
        ).order_by('-period', '-created_at')
    )

    estado = request.GET.get('estado', '')
    concepto = request.GET.get('concepto', '')
    apartamento = request.GET.get('apartamento', '')

    if estado:
        pagos_qs = pagos_qs.filter(status=estado)
    if concepto:
        pagos_qs = pagos_qs.filter(concept=concepto)
    if apartamento:
        pagos_qs = pagos_qs.filter(apartment_id=apartamento)

    paginator = Paginator(pagos_qs, PAGINATE_BY)
    pagina = request.GET.get('page')
    try:
        pagos = paginator.page(pagina)
    except PageNotAnInteger:
        pagos = paginator.page(1)
    except EmptyPage:
        pagos = paginator.page(paginator.num_pages)

    query = request.GET.copy()
    query.pop('page', None)

    contexto = {
        'pagos': pagos,
        'apartamentos': Apartment.objects.filter(is_active=True).select_related('building__garden'),
        'estado_actual': estado,
        'concepto_actual': concepto,
        'apartamento_actual': apartamento,
        'paginacion_query': query.urlencode(),
        'module_name': 'Pagos',
    }
    return render(request, 'payments/index.html', contexto)


# @login_required
def agregar_pago(request):
    if request.method == 'POST':
        datos = request.POST.copy()
        residente_id, error = _resolver_residente_id(
            datos.get('resident'), datos.get('apartment')
        )
        if error:
            messages.error(request, error)
        if residente_id:
            datos['resident'] = residente_id
        form = PaymentForm(datos, request.FILES)
        if not error and form.is_valid():
            pago = form.save(commit=False)
            pago.registered_by = request.user
            pago.save()
            messages.success(request, 'Pago registrado correctamente.')
            return redirect('pagos_index')
        if not error:
            messages.error(request, 'No se pudo registrar el pago. Revisa los datos enviados.')
    else:
        form = PaymentForm()

    contexto = {
        'form_payment': form,
        'residentes': Resident.objects.select_related('apartment').all(),
        'propietarios': Propietario.objects.filter(is_active=True),
        'apartamentos': Apartment.objects.filter(is_active=True),
        'module_name': 'Pagos',
        'titulo_modulo': 'Agregar pago',
        'url_form': 'agregar_pago',
        'url_form_args': [],
        'texto_boton': 'Agregar',
    }
    return render(request, 'payments/agregar.html', contexto)


def _resolver_residente_id(resident_id, apartment_id):
    """Devuelve (resident_id, error).

    El desplegable mezcla Propietarios y Residentes, pero Payment.resident
    apunta a Resident. Si el id elegido es un Propietario, se ubica o se crea
    su ficha de Resident en el departamento y se devuelve ese id para que el
    formulario valide y guarde sin cambios. Si ya es un Resident (o no hay
    nada que resolver), se devuelve (None, None).
    """
    if not resident_id or not apartment_id:
        return None, None
    try:
        if Resident.objects.filter(pk=resident_id).exists():
            return None, None
        propietario = Propietario.objects.filter(pk=resident_id).first()
        apartment = Apartment.objects.filter(pk=apartment_id).first()
    except (ValueError, ValidationError):
        return None, None
    if not propietario or not apartment:
        return None, None
    residente = Resident.objects.filter(
        cedula=propietario.cedula, apartment=apartment
    ).first()
    if residente:
        return str(residente.id), None
    if Resident.objects.filter(cedula=propietario.cedula).exists():
        return None, 'El propietario ya está registrado como residente en otro departamento.'
    residente = Resident.objects.create(
        apartment=apartment,
        full_name=propietario.full_name,
        cedula=propietario.cedula,
        phone=propietario.phone,
        email=propietario.email,
        tipo_relacion='propietario',
    )
    return str(residente.id), None


# @login_required
def eliminar_pago(request, pk):
    pago = Payment.objects.filter(pk=pk).first()
    if not pago:
        messages.error(request, 'Pago no encontrado.')
        return redirect('pagos_index')

    if request.method == 'POST':
        pago.delete()
        messages.success(request, 'Pago eliminado correctamente.')
        return redirect('pagos_index')

    return redirect('pagos_index')


class PaymentViewSet(viewsets.ModelViewSet):
    """ViewSet para Payment"""
    queryset = Payment.objects.select_related('apartment', 'resident').all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['resident__full_name', 'apartment__number', 'resident__cedula']
    ordering_fields = ['period', 'payment_date', 'status']
    ordering = ['-period']
    filterset_fields = ['apartment', 'resident', 'status', 'payment_method', 'concept']

    def get_queryset(self):
        queryset = super().get_queryset()
        request = self.request
        resident_id = request.query_params.get('resident')
        month = request.query_params.get('month')
        year = request.query_params.get('year')

        if resident_id:
            queryset = queryset.filter(resident_id=resident_id)
        if month:
            try:
                queryset = queryset.filter(period__month=int(month))
            except (ValueError, TypeError):
                pass
        if year:
            try:
                queryset = queryset.filter(period__year=int(year))
            except (ValueError, TypeError):
                pass

        return queryset.distinct()


# @login_required
def generar_comprobante(request):
    """Genera un comprobante de pago en PDF con los datos del formulario."""
    apartment_id = request.GET.get('apartment', '')
    resident_id = request.GET.get('resident', '')
    amount_raw = request.GET.get('amount', '0')
    concept = request.GET.get('concept', '')
    period = request.GET.get('period', '')
    payment_date = request.GET.get('payment_date', '')
    payment_method = request.GET.get('payment_method', '')
    status = request.GET.get('status', '')

    apartment = Apartment.objects.select_related('building__garden').filter(pk=apartment_id).first()
    resident = Resident.objects.select_related('apartment').filter(pk=resident_id).first()

    try:
        amount = Decimal(amount_raw or '0')
    except (InvalidOperation, ValueError):
        amount = Decimal('0')

    concept_label = dict(Payment.CONCEPT_CHOICES).get(concept, concept)
    method_label = dict(Payment.PAYMENT_METHOD_CHOICES).get(payment_method, payment_method)
    status_label = dict(Payment.STATUS_CHOICES).get(status, status)

    resident_label = resident.full_name if resident else '—'
    cedula = resident.cedula if resident else '—'
    apartment_label = apartment.name if apartment else '—'
    building_label = (
        f"{apartment.building.garden.name} — {apartment.building.name}"
        if apartment else '—'
    )
    location_label = f"Depto {apartment_label} · {building_label}"

    today = timezone.localdate()

    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        leftMargin=2.2 * cm,
        rightMargin=2.2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
        title='Comprobante de pago',
    )

    styles = getSampleStyleSheet()
    style_title = ParagraphStyle(
        'Titulo', parent=styles['Title'], fontSize=20, leading=24,
        alignment=1, spaceAfter=2, textColor=colors.HexColor('#166534'),
    )
    style_subtitle = ParagraphStyle(
        'Subtitle', parent=styles['Normal'], fontSize=12, leading=16,
        alignment=1, spaceAfter=18, textColor=colors.HexColor('#4b5563'),
    )
    style_label = ParagraphStyle(
        'Label', parent=styles['Normal'], fontSize=9.5, leading=12,
        textColor=colors.HexColor('#6b7280'), spaceAfter=2,
    )
    style_value = ParagraphStyle(
        'Value', parent=styles['Normal'], fontSize=12.5, leading=16,
        textColor=colors.HexColor('#111827'),
    )

    def field(label, value):
        return [Paragraph(label, style_label), Paragraph(value, style_value)]

    data = [
        field('Residente', resident_label),
        field('Cédula', cedula),
        field('Apartamento', location_label),
        field('Concepto', concept_label or '—'),
        field('Monto', f"Bs {amount:,.2f}".replace(',', '.').replace('.', ',', 1)),
        field('Periodo', period or '—'),
        field('Fecha de pago', payment_date or '—'),
        field('Método de pago', method_label or '—'),
        field('Estado', status_label or '—'),
    ]

    table = Table(data, colWidths=[6 * cm, 9.6 * cm])
    table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('LINEBELOW', (0, -2), (-1, -2), 0.5, colors.HexColor('#d1d5db')),
    ]))

    story = [
        Paragraph('CONDOSYS', style_title),
        Paragraph('Comprobante de pago', style_subtitle),
        table,
        Spacer(1, 1.5 * cm),
        HRFlowable(width='100%', thickness=0.6, color=colors.HexColor('#d1d5db')),
        Spacer(1, 0.5 * cm),
        Paragraph(
            f"Documento generado el {today.strftime('%d/%m/%Y')} · CONDOSYS",
            ParagraphStyle(
                'Footer', parent=styles['Normal'], fontSize=9, alignment=1,
                textColor=colors.HexColor('#9ca3af'),
            ),
        ),
    ]

    doc.build(story)
    buffer.seek(0)

    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="comprobante_pago.pdf"'
    return response