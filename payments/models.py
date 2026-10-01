from django.db import models
from django.db.models import CASCADE, PROTECT, SET_NULL
from django.core.exceptions import ValidationError
from structure.models import Apartment
from accounts.models import User
from residents.models import Resident
import uuid

# ==================================================
# PAGOS Y FACTURAS
# ==================================================

class Payment(models.Model):
    """
    Registro de pagos/facturas
    """
    CONCEPT_CHOICES = (
        ('maintenance', 'Mantenimiento'),
        ('extraordinary', 'Cuota extraordinaria'),
        ('reservation', 'Reserva'),
        ('parking', 'Parqueo'),
        ('services', 'Servicios'),
        ('other', 'Otro'),
    )

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
    apartment = models.ForeignKey(Apartment, on_delete=PROTECT, related_name='payments')
    resident = models.ForeignKey(Resident, on_delete=PROTECT, related_name='payments')

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    concept = models.CharField(max_length=50, choices=CONCEPT_CHOICES)

    # Periodo/Mes correspondiente (primer día del mes p.ej. 2026-09-01)
    period = models.DateField()
    payment_date = models.DateField(blank=True, null=True)

    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES, blank=True, null=True)

    # Comprobante
    receipt_image = models.ImageField(upload_to='payments/', blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    # Quién registró el pago
    registered_by = models.ForeignKey(User, on_delete=SET_NULL, null=True, blank=True, related_name='registered_payments')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-period']
        verbose_name_plural = 'Pagos'
        indexes = [
            models.Index(fields=['apartment', 'status']),
            models.Index(fields=['period']),
            models.Index(fields=['status']),
        ]

    def clean(self):
        super().clean()
        if self.resident_id and self.apartment_id and self.resident.apartment_id != self.apartment_id:
            raise ValidationError('El residente seleccionado no pertenece al apartamento elegido.')

    def __str__(self):
        return f"{self.resident.full_name} - {self.get_concept_display()} - {self.period}"