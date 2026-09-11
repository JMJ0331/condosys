from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import Payment, ChargeType
from .serializers import PaymentSerializer, ChargeTypeSerializer
from .forms import ChargeTypeForm, PaymentForm


@login_required
def app_index(request):
    contexto = {
        'form_charge_type': ChargeTypeForm(),
        'form_payment': PaymentForm(),
        'module_name': 'Pagos'
    }
    return render(request, 'payments/index.html', contexto)


@login_required
@require_POST
def crear_pago(request):
    form = PaymentForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, 'Pago registrado correctamente.')
    else:
        messages.error(request, 'No se pudo registrar el pago. Revisa los datos enviados.')
    return redirect('inicio')


class ChargeTypeViewSet(viewsets.ModelViewSet):
    """ViewSet para ChargeType"""
    queryset = ChargeType.objects.filter(is_active=True)
    serializer_class = ChargeTypeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class PaymentViewSet(viewsets.ModelViewSet):
    """ViewSet para Payment"""
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['apartment__number', 'reference_number']
    ordering_fields = ['invoice_date', 'due_date', 'status']
    ordering = ['-invoice_date']
    filterset_fields = ['apartment', 'status', 'payment_method', 'charge_type']

    def get_queryset(self):
        queryset = super().get_queryset()
        request = self.request
        resident_id = request.query_params.get('resident')
        month = request.query_params.get('month')
        year = request.query_params.get('year')

        if resident_id:
            queryset = queryset.filter(apartment__residents__user_id=resident_id)
        if month:
            try:
                queryset = queryset.filter(invoice_date__month=int(month))
            except (ValueError, TypeError):
                pass
        if year:
            try:
                queryset = queryset.filter(invoice_date__year=int(year))
            except (ValueError, TypeError):
                pass

        return queryset.distinct()

