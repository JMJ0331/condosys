from django.db import models
from django.db.models import CASCADE, PROTECT, SET_NULL
from structure.models import Apartment
from accounts.models import User
import uuid

# ==================================================
# PAGOS Y FACTURAS
# ==================================================

class ChargeType(models.Model):
    """
    Tipos de cargos (mantenimiento, mora, parqueo, basura, seguridad, etc)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Payment(models.Model):
    """
    Registro de pagos/facturas
    """
    STATUS_CHOICES = (
        ('pending', 'Pendiente'),
        ('at_risk', 'En riesgo'),
        ('overdue', 'Vencido'),
        ('paid', 'Pagado'),
        ('cancelled', 'Anulado'),
    )
    
    PAYMENT_METHOD_CHOICES = (
        ('cash', 'Efectivo'),
        ('transfer', 'Transferencia'),
        ('card', 'Tarjeta'),
        ('check', 'Cheque'),
        ('online', 'Pago en línea'),
        ('other', 'Otro'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    apartment = models.ForeignKey(Apartment, on_delete=CASCADE, related_name='payments')
    charge_type = models.ForeignKey(ChargeType, on_delete=PROTECT, related_name='payments')
    
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255, blank=True, null=True)
    
    invoice_date = models.DateField()
    due_date = models.DateField()
    payment_date = models.DateField(blank=True, null=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES, blank=True, null=True)
    reference_number = models.CharField(max_length=100, blank=True, null=True)
    
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-invoice_date']
        verbose_name_plural = 'Payments'
        indexes = [
            models.Index(fields=['apartment', 'status']),
            models.Index(fields=['status']),
            models.Index(fields=['due_date']),
        ]
    
    def __str__(self):
        return f"{self.apartment.number} - {self.charge_type.name} - {self.invoice_date}"
    
    @property
    def is_overdue(self):
        """Verifica si el pago está vencido"""
        from django.utils import timezone
        from datetime import timedelta
        today = timezone.now().date()
        return today > self.due_date and self.status != 'paid'
    
    @property
    def days_until_due(self):
        """Días hasta vencimiento"""
        from django.utils import timezone
        today = timezone.now().date()
        return (self.due_date - today).days

