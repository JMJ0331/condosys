from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db.models import CASCADE, PROTECT, SET_NULL
import uuid

# ==================================================
# CUSTOM USER MODEL
# ==================================================

class User(AbstractUser):
    """
    Custom User model for CONDOSYS
    Extends Django's built-in User with additional fields
    """
    ROLE_CHOICES = (
        ('admin', 'Administrador'),
        ('manager', 'Encargado de Administración'),
        ('resident', 'Residente'),
        ('maintenance', 'Personal de Mantenimiento'),
        ('security', 'Seguridad/Portería'),
    )
    
    STATUS_CHOICES = (
        ('active', 'Activo'),
        ('inactive', 'Inactivo'),
        ('pending', 'En verificación'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone = models.CharField(max_length=20, blank=True, null=True)
    document = models.CharField(max_length=50, blank=True, unique=True, null=True)
    avatar_url = models.URLField(blank=True, null=True)
    
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default='resident')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # For filtering by hierarchy
    garden_id = models.ForeignKey(
        'structure.Garden',
        on_delete=SET_NULL,
        null=True,
        blank=True,
        related_name='users'
    )
    
    last_login = models.DateTimeField(null=True, blank=True, auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Users'
        indexes = [
            models.Index(fields=['role']),
            models.Index(fields=['status']),
            models.Index(fields=['email']),
        ]
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"
    
    def get_role_display(self):
        return dict(self.ROLE_CHOICES).get(self.role, self.role)
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

