from django.db import models
from django.db.models import CASCADE, SET_NULL
from accounts.models import User
import uuid

# ==================================================
# CHAT EN TIEMPO REAL
# ==================================================

class ChatGroup(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ChatMessage(models.Model):
    """
    Mensaje de chat
    Puede ser privado (receiver_id) o grupal (group_name)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(User, on_delete=CASCADE, related_name='messages_sent')
    receiver = models.ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='messages_received',
        null=True,
        blank=True  # Si es null, es un mensaje de grupo
    )
    
    group = models.ForeignKey(
        ChatGroup,
        on_delete=SET_NULL,
        related_name='messages',
        null=True,
        blank=True
    )
    message = models.TextField()
    
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Chat Messages'
        indexes = [
            models.Index(fields=['sender']),
            models.Index(fields=['receiver']),
            models.Index(fields=['group']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        if self.receiver:
            return f"{self.sender.email} → {self.receiver.email}"
        else:
            return f"{self.sender.email} → {self.group_name}"
    
    def mark_as_read(self):
        """Marcar mensaje como leído"""
        if not self.is_read:
            from django.utils import timezone
            self.is_read = True
            self.read_at = timezone.now()
            self.save()

