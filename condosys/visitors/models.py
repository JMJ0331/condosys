from django.db import models
from django.db.models import CASCADE, PROTECT, SET_NULL
from structure.models import Apartment
from accounts.models import User
import uuid

# ==================================================
# VISITANTES Y CONTROL DE ACCESO
# ==================================================

class Visitor(models.Model):
    """
    Registro de visitantes
    """
    TYPE_CHOICES = (
        ('family', 'Familiar'),
        ('delivery', 'Delivery'),
        ('technician', 'Técnico'),
        ('provider', 'Proveedor'),
        ('other', 'Otro'),
    )
    
    STATUS_CHOICES = (
        ('pending', 'Esperando'),
        ('authorized', 'Autorizado'),
        ('rejected', 'Rechazado'),
        ('completed', 'Completado'),
        ('cancelled', 'Cancelado'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    apartment = models.ForeignKey(Apartment, on_delete=CASCADE, related_name='visitors')
    registered_by = models.ForeignKey(User, on_delete=PROTECT, related_name='visitors_registered')
    
    name = models.CharField(max_length=100)
    document = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    reason = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(max_length=30, choices=TYPE_CHOICES, default='other')
    
    vehicle_plate = models.CharField(max_length=20, blank=True, null=True)
    
    scheduled_entry = models.DateTimeField()
    scheduled_exit = models.DateTimeField(blank=True, null=True)
    actual_entry = models.DateTimeField(blank=True, null=True)
    actual_exit = models.DateTimeField(blank=True, null=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    authorized_by = models.ForeignKey(
        User,
        on_delete=SET_NULL,
        null=True,
        blank=True,
        related_name='visitors_authorized'
    )
    
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-scheduled_entry']
        verbose_name_plural = 'Visitors'
        indexes = [
            models.Index(fields=['apartment']),
            models.Index(fields=['scheduled_entry']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.apartment.number} - {self.scheduled_entry.date()}"

