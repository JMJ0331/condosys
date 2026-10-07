import uuid

from django.db import models
from django.utils import timezone

from accounts.models import User


class PasswordResetToken(models.Model):
    """
    Token de un solo uso para restablecer la contraseña de un usuario.
    Se genera al solicitar la recuperación y se invalida tras usarse
    o al cumplir su tiempo de expiración.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='password_reset_tokens',
    )
    token = models.CharField(max_length=64, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    used_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'used_at']),
        ]

    def __str__(self):
        estado = 'usado' if self.used_at else ('expirado' if self.expirado() else 'activo')
        return f"Token de recuperación ({estado})"

    @property
    def esta_usado(self):
        return self.used_at is not None

    def expirado(self):
        return timezone.now() >= self.expires_at

    def es_valido(self):
        return not self.esta_usado and not self.expirado()

    def marcar_como_usado(self):
        self.used_at = timezone.now()
        self.save(update_fields=['used_at'])
