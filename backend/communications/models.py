from django.db import models
from django.db.models import CASCADE, PROTECT, SET_NULL
from structure.models import Garden, Building
from accounts.models import User
import uuid

# ==================================================
# COMUNICACIONES Y AVISOS
# ==================================================

class Communication(models.Model):
    """
    Comunicado/Aviso general
    """
    TARGET_TYPE_CHOICES = (
        ('general', 'General'),
        ('building', 'Por edificio'),
        ('resident', 'Para residente'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    garden = models.ForeignKey(Garden, on_delete=CASCADE, related_name='communications')
    sender = models.ForeignKey(User, on_delete=PROTECT, related_name='communications_sent')
    
    title = models.CharField(max_length=200)
    body = models.TextField()
    
    target_type = models.CharField(max_length=30, choices=TARGET_TYPE_CHOICES, default='general')
    target_id = models.UUIDField(blank=True, null=True)  # building_id o user_id según target_type
    
    is_published = models.BooleanField(default=True)
    published_at = models.DateTimeField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-published_at', '-created_at']
        verbose_name_plural = 'Communications'
        indexes = [
            models.Index(fields=['garden']),
            models.Index(fields=['published_at']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.created_at.date()}"

