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
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Audit Logs'

    def __str__(self):
        return f"{self.user.email} - {self.action} ({self.entity})"


class AuditLogDetail(models.Model):
    audit_log = models.ForeignKey(AuditLog, on_delete=CASCADE, related_name='details')
    key = models.CharField(max_length=100)
    value = models.TextField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['audit_log', 'key'],
                name='unique_audit_log_detail_key'
            ),
        ]

    def __str__(self):
        return f"{self.audit_log_id} - {self.key}"
