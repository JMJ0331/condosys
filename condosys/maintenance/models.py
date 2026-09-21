from django.db import models
from django.utils import timezone
import uuid

# ==================================================
# CARGOS / CUOTAS DE MANTENIMIENTO
# ==================================================

class MaintenanceCharge(models.Model):
    """
    Cargo recurrente de mantenimiento con sus métodos de pago permitidos
    (concepto, periodicidad, monto, vigencia y evidencia fotográfica).
    """
    CONCEPT_CHOICES = (
        ('maintenance', 'Mantenimiento'),
        ('security', 'Seguridad'),
        ('cleaning', 'Limpieza'),
        ('administration', 'Administración'),
        ('reserve_fund', 'Fondo de reserva'),
        ('water', 'Agua'),
        ('electricity', 'Electricidad'),
        ('other', 'Otro'),
    )

    PERIODICITY_CHOICES = (
        ('monthly', 'Mensual'),
        ('quarterly', 'Trimestral'),
        ('semiannual', 'Semestral'),
        ('annual', 'Anual'),
    )

    # Mismos métodos que define Payment (payments.models): efectivo,
    # transferencia, tarjeta, cheque, en línea y otro.
    PAYMENT_METHOD_CHOICES = (
        ('cash', 'Efectivo'),
        ('transfer', 'Transferencia'),
        ('card', 'Tarjeta'),
        ('check', 'Cheque'),
        ('online', 'Pago en línea'),
        ('other', 'Otro'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    concept = models.CharField(max_length=30, choices=CONCEPT_CHOICES)
    periodicity = models.CharField(max_length=20, choices=PERIODICITY_CHOICES, default='monthly')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    apartment = models.ForeignKey(
        'structure.Apartment',
        on_delete=models.SET_NULL,
        related_name='maintenance_charges',
        null=True,
        blank=True,
        verbose_name='Departamento (si es aplicable)',
        help_text='Vacío = aplica a todos los departamentos.',
    )

    payment_methods = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        blank=True,
        null=True,
    )

    effective_date = models.DateField(default=timezone.localdate)
    photo = models.FileField(upload_to='mantenimiento/', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-effective_date']
        verbose_name_plural = 'Cargos de mantenimiento'

    def __str__(self):
        return f"{self.get_concept_display()} - {self.amount} ({self.get_periodicity_display()})"