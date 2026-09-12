from django.db import models
from django.db.models import CASCADE
from accounts.models import User
from structure.models import Apartment
import uuid

# ==================================================
# RESIDENTES Y OCUPANTES
# ==================================================

class Resident(models.Model):
    """
    Residente/Ocupante
    Vinculación entre persona y apartamento
    """
    MARITAL_CHOICES = (
        ('single', 'Soltero/a'),
        ('married', 'Casado/a'),
        ('divorced', 'Divorciado/a'),
        ('widowed', 'Viudo/a'),
        ('other', 'Otro'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='resident_profiles',
        null=True,
        blank=True,
    )
    apartment = models.ForeignKey(Apartment, on_delete=CASCADE, related_name='residents')

    # Información del personal
    full_name = models.CharField(max_length=100)
    marital_status = models.CharField(max_length=30, choices=MARITAL_CHOICES, default='single')
    cedula = models.CharField(max_length=50, unique=True)
    photo = models.ImageField(upload_to='residents/', blank=True, null=True)

    # Información de contacto
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    emergency_contact = models.CharField(max_length=20, blank=True, null=True)

    # Estado del registro
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['apartment', 'full_name']
        verbose_name_plural = 'Residents'
        indexes = [
            models.Index(fields=['apartment']),
            models.Index(fields=['user']),
        ]

    def __str__(self):
        return f"{self.full_name} - {self.apartment.name}"

    @property
    def is_current(self):
        """Compatibilidad: el residente está activo"""
        return self.is_active