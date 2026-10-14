from django.db import models
from django.db.models import CASCADE
from accounts.models import User
from accounts.validators import validar_cedula, validar_telefono, validar_contacto_emergencia
import uuid

# ==================================================
# PROPIETARIOS
# ==================================================
# Modelo propio e independiente de `residents.Resident`.
# `structure.Apartment.owner` apunta aquí
# (related_name='apartments_owned').
# `residents.Resident` queda como ocupante del apartamento.


class Propietario(models.Model):
    """Propietario de uno o varios apartamentos."""

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
        related_name='propietario_profiles',
        null=True,
        blank=True,
    )

    # Información personal
    full_name = models.CharField(max_length=100)
    marital_status = models.CharField(max_length=30, choices=MARITAL_CHOICES, default='single')
    cedula = models.CharField(max_length=13, unique=True, validators=[validar_cedula])
    photo = models.ImageField(upload_to='propietarios/', blank=True, null=True)

    # Información de contacto
    phone = models.CharField(max_length=14, validators=[validar_telefono])
    email = models.EmailField(blank=True, null=True)
    emergency_contact = models.CharField(max_length=14, blank=True, null=True, validators=[validar_contacto_emergencia])

    # Estado del registro
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['full_name']
        verbose_name_plural = 'Propietarios'
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['cedula']),
        ]

    def __str__(self):
        return self.full_name
