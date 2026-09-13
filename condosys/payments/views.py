from decimal import Decimal, InvalidOperation
from io import BytesIO

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST
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
from structure.models import Apartment


# @login_required
def app_index(request):
    contexto = {
        'form_payment': PaymentForm(),
        'residentes': Resident.objects.select_related('apartment').all(),
        'apartamentos': Apartment.objects.filter(is_active=True),
        'module_name': 'Pagos'
    }
    return render(request, 'payments/index.html', contexto)


# @login_required
@require_POST
def crear_pago(request):
    form = PaymentForm(request.POST, request.FILES)
    if form.is_valid():
        pago = form.save(commit=False)
        pago.registered_by = request.user
        pago.save()
        messages.success(request, 'Pago registrado correctamente.')
    else:
        messages.error(request, 'No se pudo registrar el pago. Revisa los datos enviados.')
    return redirect('inicio')


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