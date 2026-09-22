from decimal import Decimal, InvalidOperation
from datetime import datetime
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


def _anios_con_pagos():
    """Años con pagos registrados (desc), incluyendo el año actual."""
    anios = {fecha.year for fecha in Payment.objects.dates('period', 'year')}
    anios.add(timezone.localdate().year)
    return sorted(anios, reverse=True)


MESES_NOMBRE = {
    1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril',
    5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto',
    9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre',
}


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
    mes = request.GET.get('mes', '')
    anio = request.GET.get('anio', '')

    if estado:
        pagos_qs = pagos_qs.filter(status=estado)
    if concepto:
        pagos_qs = pagos_qs.filter(concept=concepto)
    if apartamento:
        pagos_qs = pagos_qs.filter(apartment_id=apartamento)
    if mes.isdigit() and 1 <= int(mes) <= 12:
        pagos_qs = pagos_qs.filter(period__month=int(mes))
    else:
        mes = ''
    if anio.isdigit():
        pagos_qs = pagos_qs.filter(period__year=int(anio))
    else:
        anio = ''

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
        'mes_actual': mes,
        'anio_actual': anio,
        'mes_actual_nombre': MESES_NOMBRE.get(int(mes), 'Todos los meses') if mes else 'Todos los meses',
        'anios': _anios_con_pagos(),
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


# @login_required
def actualizar_pago(request, pk):
    pago = Payment.objects.filter(pk=pk).first()
    if not pago:
        messages.error(request, 'Pago no encontrado.')
        return redirect('pagos_index')

    if request.method == 'POST':
        datos = request.POST.copy()
        residente_id, error = _resolver_residente_id(
            datos.get('resident'), datos.get('apartment')
        )
        if error:
            messages.error(request, error)
        if residente_id:
            datos['resident'] = residente_id
        form = PaymentForm(datos, request.FILES, instance=pago)
        if not error and form.is_valid():
            form.save()
            messages.success(request, 'Pago actualizado correctamente.')
            return redirect('pagos_index')
        if not error:
            messages.error(request, 'No se pudo actualizar el pago. Revisa los datos enviados.')
    else:
        tipo_relacion = getattr(pago.resident, 'tipo_relacion', '')
        form = PaymentForm(
            instance=pago,
            initial={'quien_paga': 'propietario' if tipo_relacion == 'propietario' else 'residente'},
        )

    contexto = {
        'form_payment': form,
        'residentes': Resident.objects.select_related('apartment').all(),
        'propietarios': Propietario.objects.filter(is_active=True),
        'apartamentos': Apartment.objects.filter(is_active=True),
        'module_name': 'Pagos',
        'titulo_modulo': 'Actualizar pago',
        'url_form': 'actualizar_pago',
        'url_form_args': [str(pago.id)],
        'texto_boton': 'Actualizar',
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
    """Genera el comprobante de pago en PDF (diseño de comprobante.png)."""
    from residencial.models import Residencial

    MESES = {
        1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril',
        5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto',
        9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre',
    }
    VERDE = colors.HexColor('#0F3D2E')
    FONDO_VERDE = colors.HexColor('#E9F5EC')
    GRIS = colors.HexColor('#6B7280')
    NEGRO = colors.HexColor('#111827')

    apartment_id = request.GET.get('apartment', '')
    resident_id = request.GET.get('resident', '')
    amount_raw = request.GET.get('amount', '0')
    concept = request.GET.get('concept', '')
    period_raw = request.GET.get('period', '')
    payment_date_raw = request.GET.get('payment_date', '')
    payment_method = request.GET.get('payment_method', '')
    status = request.GET.get('status', '')

    apartment = Apartment.objects.select_related('building__garden').filter(pk=apartment_id).first()
    resident = Resident.objects.select_related('apartment').filter(pk=resident_id).first()
    residencial = Residencial.obtener_unico()

    try:
        amount = Decimal(amount_raw or '0')
    except (InvalidOperation, ValueError):
        amount = Decimal('0')

    def monto(valor):
        return f'RD${valor:,.2f}'

    concept_label = dict(Payment.CONCEPT_CHOICES).get(concept, concept) or '—'
    method_label = dict(Payment.PAYMENT_METHOD_CHOICES).get(payment_method, payment_method) or '—'
    status_label = dict(Payment.STATUS_CHOICES).get(status, status) or '—'

    try:
        periodo = datetime.strptime(period_raw, '%Y-%m-%d').date() if period_raw else None
    except ValueError:
        periodo = None
    periodo_label = f'{MESES[periodo.month]} {periodo.year}' if periodo else '—'

    try:
        fecha_pago = datetime.strptime(payment_date_raw, '%Y-%m-%d').date() if payment_date_raw else None
    except ValueError:
        fecha_pago = None
    hoy = timezone.localdate()
    fecha_label = (fecha_pago or hoy).strftime('%d/%m/%Y')

    if apartment:
        bloque = apartment.building.tower or apartment.building.name
        departamento_label = f'{bloque} - {apartment.name}'
    else:
        departamento_label = '—'

    recibo = (request.GET.get('recibo') or '').strip().upper() or f'{Payment.objects.count() + 1:06d}'
    digitos = ''.join(c for c in recibo if c.isdigit()) or '0'
    ncf = f"A{digitos.rjust(11, '0')[-11:]}"
    rnc = (residencial.rnc if residencial and residencial.rnc else '0-00-00000-0')
    nombre_residencial = (residencial.nombre if residencial and residencial.nombre else 'condosys')
    ciudad = (residencial.municipio if residencial and residencial.municipio else 'Santiago de los caballeros')

    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        leftMargin=1.6 * cm,
        rightMargin=1.6 * cm,
        topMargin=2.2 * cm,
        bottomMargin=1.6 * cm,
        title='Comprobante de pago',
    )
    ancho = letter[0] - 3.2 * cm

    def barras(canvas, _doc):
        canvas.saveState()
        canvas.setFillColor(VERDE)
        canvas.rect(0, letter[1] - 30, letter[0], 30, stroke=0, fill=1)
        canvas.rect(0, 0, letter[0], 22, stroke=0, fill=1)
        canvas.restoreState()

    styles = getSampleStyleSheet()
    est_titulo = ParagraphStyle('Titulo', parent=styles['Title'], fontSize=19, leading=23, alignment=1, spaceAfter=2, textColor=VERDE, fontName='Helvetica-Bold')
    est_subtitulo = ParagraphStyle('Subtitulo', parent=styles['Normal'], fontSize=10.5, leading=14, alignment=1, spaceAfter=14, textColor=GRIS)
    est_etiqueta = ParagraphStyle('Etiqueta', parent=styles['Normal'], fontSize=8.5, leading=11, textColor=GRIS, spaceAfter=1)
    est_valor = ParagraphStyle('Valor', parent=styles['Normal'], fontSize=11, leading=14, textColor=NEGRO, fontName='Helvetica-Bold')
    est_marca = ParagraphStyle('Marca', parent=styles['Normal'], fontSize=17, leading=20, textColor=VERDE, fontName='Helvetica-Bold')
    est_ciudad = ParagraphStyle('Ciudad', parent=styles['Normal'], fontSize=9, leading=12, textColor=GRIS)
    est_fiscal = ParagraphStyle('Fiscal', parent=styles['Normal'], fontSize=10, leading=14, textColor=NEGRO)
    est_fiscal_titulo = ParagraphStyle('FiscalTitulo', parent=est_fiscal, fontName='Helvetica-Bold')
    est_pie = ParagraphStyle('Pie', parent=styles['Normal'], fontSize=8.5, leading=11, alignment=1, textColor=GRIS)
    est_celda = ParagraphStyle('Celda', parent=styles['Normal'], fontSize=10, leading=13, textColor=NEGRO)
    est_celda_der = ParagraphStyle('CeldaDer', parent=est_celda, alignment=2)
    est_celda_cen = ParagraphStyle('CeldaCen', parent=est_celda, alignment=1)
    est_cab = ParagraphStyle('Cab', parent=styles['Normal'], fontSize=10.5, leading=13, textColor=colors.white, fontName='Helvetica-Bold')
    est_cab_der = ParagraphStyle('CabDer', parent=est_cab, alignment=2)

    def campo(etiqueta, valor):
        return [Paragraph(etiqueta, est_etiqueta), Paragraph(valor, est_valor)]

    encabezado = Table([
        [
            [Paragraph(nombre_residencial, est_marca), Paragraph(f'{ciudad}, RD', est_ciudad)],
            [Paragraph('RNC', est_etiqueta), Paragraph(rnc, est_ciudad)],
            [Paragraph('NCF', est_etiqueta), Paragraph(ncf, est_ciudad)],
        ],
    ], colWidths=[ancho * 0.52, ancho * 0.24, ancho * 0.24])
    encabezado.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 1),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
        ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
    ]))

    info = Table([[
        campo('Fecha de pago', fecha_label),
        campo('Departamento', departamento_label),
        campo('Residente / Propietario', resident.full_name if resident else '—'),
    ], [
        campo('Cedula / RNC', resident.cedula if resident else '—'),
        campo('Metodo de pago', method_label),
        campo('Estado', status_label),
    ]], colWidths=[ancho / 3] * 3)
    info.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), FONDO_VERDE),
        ('ROUNDEDCORNERS', [8, 8, 8, 8]),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))

    tabla = Table([
        [Paragraph('Concepto', est_cab), Paragraph('Periodo', est_cab), Paragraph('Monto', est_cab_der)],
        [Paragraph(concept_label, est_celda), Paragraph(periodo_label, est_celda_cen), Paragraph(monto(amount), est_celda_der)],
    ], colWidths=[ancho * 0.5, ancho * 0.25, ancho * 0.25])
    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), VERDE),
        ('ROUNDEDCORNERS', [6, 6, 6, 6]),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
        ('LINEBELOW', (0, 1), (-1, 1), 0.6, colors.HexColor('#E5E7EB')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))

    totales = Table([
        [Paragraph('Subtotal', est_celda), Paragraph(monto(amount), est_celda_der)],
        [Paragraph('ITBS (18%)', est_celda), Paragraph(monto(Decimal('0')), est_celda_der)],
        [Paragraph('Total pagado', est_celda), Paragraph(monto(amount), est_celda_der)],
    ], colWidths=[ancho * 0.62, ancho * 0.38])
    totales.setStyle(TableStyle([
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LINEBELOW', (0, 1), (-1, 1), 0.6, colors.HexColor('#D1D5DB')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))

    nota = Table([[
        [Paragraph('Comprobante Fiscal', est_fiscal_titulo),
         Paragraph('Este documento es valido como comprobante fiscal (NCF) segun la normativa vigente de la DGII, Republica Dominicana.', est_fiscal)],
    ]], colWidths=[ancho])
    nota.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), FONDO_VERDE),
        ('ROUNDEDCORNERS', [8, 8, 8, 8]),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ]))

    est_pie_izq = ParagraphStyle('PieIzq', parent=est_pie, alignment=0)
    est_pie_der = ParagraphStyle('PieDer', parent=est_pie, alignment=2)
    linea_izq = HRFlowable(width='85%', thickness=0.6, color=colors.HexColor('#9CA3AF'), spaceAfter=4, spaceBefore=0, hAlign='LEFT')
    linea_der = HRFlowable(width='85%', thickness=0.6, color=colors.HexColor('#9CA3AF'), spaceAfter=4, spaceBefore=0, hAlign='RIGHT')
    firmas = Table([
        [linea_izq, linea_der],
        [Paragraph('Firma del administrador', est_pie_izq), Paragraph('Sello del residencial', est_pie_der)],
    ], colWidths=[ancho / 2] * 2)
    firmas.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 1),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
    ]))

    story = [
        encabezado,
        Spacer(1, 0.3 * cm),
        HRFlowable(width='100%', thickness=0.6, color=colors.HexColor('#E5E7EB')),
        Spacer(1, 0.4 * cm),
        Paragraph('Comprobante de Pago', est_titulo),
        Paragraph(f'No. de recibo: {recibo}', est_subtitulo),
        info,
        Spacer(1, 0.4 * cm),
        tabla,
        Spacer(1, 0.25 * cm),
        totales,
        Spacer(1, 0.45 * cm),
        nota,
        Spacer(1, 2.2 * cm),
        firmas,
        Spacer(1, 0.8 * cm),
        Paragraph('Condosys - Sistema de administracion de residenciales - www.condosys.do', est_pie),
        Paragraph('Este comprobante ha sido generado electronicamente y no requiere firma manuscrita para su validez interna.', est_pie),
    ]

    doc.build(story, onFirstPage=barras, onLaterPages=barras)
    buffer.seek(0)

    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="comprobante_pago.pdf"'
    return response
