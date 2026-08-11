from django.db import models
from django.db.models import CASCADE, PROTECT, SET_NULL
from accounts.models import User
from structure.models import Apartment
import uuid

# ==================================================
# RESIDENTES Y OCUPANTES
# ==================================================

class Resident(models.Model):
    """
    Residente/Ocupante
    Vinculación entre Usuario y Apartamento
    Una persona puede estar en múltiples apartamentos
    """
    ROLE_CHOICES = (
        ('owner', 'Propietario'),
        ('occupant', 'Ocupante'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=CASCADE, related_name='resident_profile')
    apartment = models.ForeignKey(Apartment, on_delete=CASCADE, related_name='residents')
    role_in_apartment = models.CharField(max_length=30, choices=ROLE_CHOICES, default='occupant')
    
    move_in_date = models.DateField(blank=True, null=True)
    move_out_date = models.DateField(blank=True, null=True)
    
    emergency_contact = models.CharField(max_length=100, blank=True, null=True)
    emergency_phone = models.CharField(max_length=20, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['apartment', '-move_in_date']
        unique_together = ('user', 'apartment')  # Un usuario no puede tener 2 roles en el mismo apto
        verbose_name_plural = 'Residents'
        indexes = [
            models.Index(fields=['apartment']),
            models.Index(fields=['user']),
        ]
    
    def __str__(self):
        return f"{self.user.full_name} - {self.apartment.number} ({self.get_role_in_apartment_display()})"
    
    @property
    def is_current(self):
        """Verifica si el residente está actualmente activo"""
        from django.utils import timezone
        today = timezone.now().date()
        if self.move_in_date and today < self.move_in_date:
            return False
        if self.move_out_date and today > self.move_out_date:
            return False
        return True

