from django.db import models
from django.db.models import CASCADE, PROTECT, SET_NULL
from accounts.models import User
import uuid

# ==================================================
# NOTIFICACIONES
# ==================================================

class Notification(models.Model):
    """
    Notificación para usuario
    """
    TYPE_CHOICES = (
        ('incident_assigned', 'Incidencia asignada'),
        ('incident_updated', 'Incidencia actualizada'),
        ('payment_due', 'Pago próximo a vencer'),
        ('payment_overdue', 'Pago vencido'),
        ('message', 'Nuevo mensaje'),
        ('reservation_approved', 'Reserva aprobada'),
        ('reservation_rejected', 'Reserva rechazada'),
        ('visitor_arrival', 'Visitante llegó'),
        ('general', 'Notificación general'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=CASCADE, related_name='notifications')
    
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    
    related_id = models.UUIDField(blank=True, null=True)  # incident_id, payment_id, etc
    
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Notifications'
        indexes = [
            models.Index(fields=['user', 'is_read']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.user.email} - {self.type}"
    
    def mark_as_read(self):
        """Marcar notificación como leída"""
        if not self.is_read:
            from django.utils import timezone
            self.is_read = True
            self.read_at = timezone.now()
            self.save()

