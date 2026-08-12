from django.db import models
from django.db.models import CASCADE, PROTECT, SET_NULL
from structure.models import Garden
from accounts.models import User
import uuid

# ==================================================
# ÁREAS COMUNES Y RESERVAS
# ==================================================

class CommonArea(models.Model):
    """
    Área común (salón, piscina, cancha, etc)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    garden = models.ForeignKey(Garden, on_delete=CASCADE, related_name='common_areas')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    capacity = models.PositiveIntegerField(blank=True, null=True)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['garden', 'name']
        unique_together = ('garden', 'name')
        verbose_name_plural = 'Common Areas'
    
    def __str__(self):
        return f"{self.garden.name} - {self.name}"


class Reservation(models.Model):
    """
    Reserva de área común
    """
    STATUS_CHOICES = (
        ('requested', 'Solicitada'),
        ('approved', 'Aprobada'),
        ('rejected', 'Rechazada'),
        ('completed', 'Completada'),
        ('cancelled', 'Cancelada'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    common_area = models.ForeignKey(CommonArea, on_delete=CASCADE, related_name='reservations')
    reserved_by = models.ForeignKey(User, on_delete=CASCADE, related_name='reservations')
    
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    reason = models.CharField(max_length=200, blank=True, null=True)
    expected_guests = models.PositiveIntegerField(blank=True, null=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='requested')
    approved_by = models.ForeignKey(
        User,
        on_delete=SET_NULL,
        null=True,
        blank=True,
        related_name='reservations_approved'
    )
    
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-start_time']
        verbose_name_plural = 'Reservations'
        indexes = [
            models.Index(fields=['common_area', 'start_time']),
            models.Index(fields=['reserved_by']),
            models.Index(fields=['status']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['common_area', 'start_time', 'end_time'],
                name='unique_reservation_time'
            ),
        ]
    
    def __str__(self):
        return f"{self.common_area.name} - {self.start_time.date()}"

