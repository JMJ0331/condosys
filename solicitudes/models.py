from django.db import models
from django.db.models import CASCADE, SET_NULL
from django.utils import timezone
from structure.models import Apartment
from residents.models import Resident
import uuid

# ==================================================
# SOLICITUDES
# ==================================================

class Solicitud(models.Model):
    """
    Solicitud de los residentes (certificados, permisos, servicios, etc.)
    """
    REQUEST_TYPE_CHOICES = (
        ('certificado', 'Certificado'),
        ('permiso', 'Permiso'),
        ('mantenimiento', 'Mantenimiento'),
        ('instalacion', 'Instalación'),
        ('reparacion', 'Reparación'),
        ('documentacion', 'Documentación'),
        ('otro', 'Otro'),
    )

    STATUS_CHOICES = (
        ('pendiente', 'Pendiente'),
        ('en_proceso', 'En proceso'),
        ('aprobada', 'Aprobada'),
        ('rechazada', 'Rechazada'),
        ('completada', 'Completada'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    apartment = models.ForeignKey(Apartment, on_delete=CASCADE, related_name='solicitudes')
    resident = models.ForeignKey(
        Resident,
        on_delete=SET_NULL,
        null=True,
        blank=True,
        related_name='solicitudes'
    )

    request_type = models.CharField(max_length=30, choices=REQUEST_TYPE_CHOICES)
    description = models.TextField()
    request_date = models.DateField(default=timezone.localdate)
    attachment = models.FileField(upload_to='solicitudes/', null=True, blank=True)

    tracking_response = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendiente')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Solicitudes'
        indexes = [
            models.Index(fields=['apartment', 'status']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"#{self.id.hex[:8]} - {self.get_request_type_display()} ({self.get_status_display()})"