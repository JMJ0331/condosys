from django.db import models
from django.db.models import CASCADE, PROTECT, SET_NULL
from structure.models import Apartment
from incidents.models import Incident
from accounts.models import User
import uuid

# ==================================================
# ÓRDENES DE MANTENIMIENTO
# ==================================================

class MaintenanceOrder(models.Model):
    """
    Orden de mantenimiento
    Puede originarse de una incidencia o ser preventiva
    """
    TYPE_CHOICES = (
        ('preventive', 'Preventivo'),
        ('corrective', 'Correctivo'),
        ('emergency', 'Emergencia'),
    )
    
    STATUS_CHOICES = (
        ('scheduled', 'Programado'),
        ('in_progress', 'En proceso'),
        ('completed', 'Completado'),
        ('cancelled', 'Cancelado'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    incident = models.ForeignKey(
        Incident,
        on_delete=SET_NULL,
        null=True,
        blank=True,
        related_name='maintenance_orders'
    )
    apartment = models.ForeignKey(
        Apartment,
        on_delete=CASCADE,
        related_name='maintenance_orders',
        null=True,
        blank=True
    )
    assigned_to = models.ForeignKey(User, on_delete=PROTECT, related_name='maintenance_orders')
    
    type = models.CharField(max_length=30, choices=TYPE_CHOICES)
    description = models.TextField()
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='scheduled')
    
    scheduled_date = models.DateField(blank=True, null=True)
    completion_date = models.DateField(blank=True, null=True)
    
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    actual_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-scheduled_date']
        verbose_name_plural = 'Maintenance Orders'
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['assigned_to']),
        ]
    
    def __str__(self):
        apartment_str = f" - {self.apartment.number}" if self.apartment else ""
        return f"#{self.id.hex[:8]} {apartment_str} - {self.get_type_display()}"

