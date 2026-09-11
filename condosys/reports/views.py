from django.db.models import Count, Q, Sum
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import AuditLog
from .serializers import AuditLogSerializer
from structure.models import Apartment
from residents.models import Resident
from payments.models import Payment
from incidents.models import Incident
from visitors.models import Visitor
from reservations.models import Reservation
from .forms import AuditLogForm, AuditLogDetailForm


@login_required
def app_index(request):
    contexto = {
        'form_audit_log': AuditLogForm(),
        'form_audit_log_detail': AuditLogDetailForm(),
        'module_name': 'Reportes'
    }
    return render(request, 'reports/index.html', contexto)


@login_required
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


@login_required
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
            queryset = queryset.filter(invoice_date__month=month)
        if year:
            queryset = queryset.filter(invoice_date__year=year)

        data = queryset.values('status').annotate(count=Count('id'), total=Sum('amount')).order_by('status')
        return Response(data)

    @action(detail=False, methods=['get'])
    def occupancy(self, request):
        data = Apartment.objects.values('status').annotate(count=Count('id')).order_by('status')
        return Response(data)
