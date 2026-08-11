from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import Payment, ChargeType
from .serializers import PaymentSerializer, ChargeTypeSerializer


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
    filterset_fields = ['apartment', 'status', 'payment_method']

