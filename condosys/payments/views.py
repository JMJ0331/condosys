from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import Payment
from .serializers import PaymentSerializer
from .forms import PaymentForm
from residents.models import Resident
from structure.models import Apartment


@login_required
def app_index(request):
    contexto = {
        'form_payment': PaymentForm(),
        'residentes': Resident.objects.select_related('apartment').all(),
        'apartamentos': Apartment.objects.filter(is_active=True),
        'module_name': 'Pagos'
    }
    return render(request, 'payments/index.html', contexto)


@login_required
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