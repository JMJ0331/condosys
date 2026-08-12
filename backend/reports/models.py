from django.db import models
from django.db.models import CASCADE
from accounts.models import User
import uuid


class AuditLog(models.Model):
    """Registro de auditoría de acciones administrativas"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=CASCADE, related_name='audit_logs')
    action = models.CharField(max_length=100)
    entity = models.CharField(max_length=100)
    entity_id = models.UUIDField(blank=True, null=True)
    details = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Audit Logs'

    def __str__(self):
        return f"{self.user.email} - {self.action} ({self.entity})"
