from django.db import models
from django.db.models import CASCADE, PROTECT, SET_NULL
from structure.models import Apartment
from accounts.models import User
import uuid

# ==================================================
# INCIDENCIAS Y SOLICITUDES
# ==================================================

class Incident(models.Model):
    """
    Incidencias / Solicitudes de servicio
    Workflow: Nueva → Asignada → En progreso → Resuelta → Cerrada
    """
    CATEGORY_CHOICES = (
        ('plumbing', 'Plomería'),
        ('electricity', 'Electricidad'),
        ('structural', 'Estructural'),
        ('cleaning', 'Limpieza'),
        ('security', 'Seguridad'),
        ('noise', 'Ruido'),
        ('water', 'Agua'),
        ('other', 'Otro'),
    )
    
    PRIORITY_CHOICES = (
        ('low', 'Baja'),
        ('normal', 'Normal'),
        ('high', 'Alta'),
        ('urgent', 'Urgente'),
    )
    
    STATUS_CHOICES = (
        ('new', 'Nueva'),
        ('assigned', 'Asignada'),
        ('in_progress', 'En progreso'),
        ('resolved', 'Resuelta'),
        ('closed', 'Cerrada'),
        ('rejected', 'Rechazada'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    apartment = models.ForeignKey(Apartment, on_delete=CASCADE, related_name='incidents')
    reported_by = models.ForeignKey(User, on_delete=PROTECT, related_name='incidents_reported')
    assigned_to = models.ForeignKey(
        User,
        on_delete=SET_NULL,
        null=True,
        blank=True,
        related_name='incidents_assigned'
    )
    
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='normal')
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='new')
    
    resolution_notes = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Incidents'
        indexes = [
            models.Index(fields=['apartment', 'status']),
            models.Index(fields=['status']),
            models.Index(fields=['assigned_to']),
            models.Index(fields=['reported_by']),
        ]
    
    def __str__(self):
        return f"#{self.id.hex[:8]} - {self.title} ({self.get_status_display()})"


class IncidentImage(models.Model):
    incident = models.ForeignKey(Incident, on_delete=CASCADE, related_name='images')
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['incident', 'url'],
                name='unique_incident_image_url'
            ),
        ]

    def __str__(self):
        return f"{self.incident_id} - {self.url}"


class IncidentHistory(models.Model):
    """
    Registro de cambios de estado en una incidencia
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    incident = models.ForeignKey(Incident, on_delete=CASCADE, related_name='history')
    status_from = models.CharField(max_length=30, blank=True, null=True)
    status_to = models.CharField(max_length=30)
    changed_by = models.ForeignKey(User, on_delete=PROTECT)
    comment = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Incident Histories'
    
    def __str__(self):
        return f"{self.incident.id.hex[:8]} - {self.status_from} → {self.status_to}"

