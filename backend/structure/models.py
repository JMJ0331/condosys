from django.db import models
from django.db.models import CASCADE, PROTECT, SET_NULL
import uuid

# ==================================================
# ESTRUCTURA FÍSICA: Jardín → Edificio → Apartamento
# ==================================================

class Garden(models.Model):
    """
    Jardín (residencial)
    Nivel superior de la jerarquía
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Gardens'
    
    def __str__(self):
        return self.name


class Building(models.Model):
    """
    Edificio
    Pertenece a un Jardín
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    garden = models.ForeignKey(Garden, on_delete=CASCADE, related_name='buildings')
    name = models.CharField(max_length=50)
    number_of_floors = models.PositiveIntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['garden', 'name']
        unique_together = ('garden', 'name')
        verbose_name_plural = 'Buildings'
        indexes = [
            models.Index(fields=['garden']),
        ]
    
    def __str__(self):
        return f"{self.garden.name} - {self.name}"


class Apartment(models.Model):
    """
    Apartamento/Departamento
    Pertenece a un Edificio
    """
    STATUS_CHOICES = (
        ('empty', 'Vacío'),
        ('occupied', 'Ocupado'),
        ('maintenance', 'En reparación'),
        ('blocked', 'Bloqueado'),
    )
    
    TYPE_CHOICES = (
        ('apartment', 'Apartamento'),
        ('house', 'Casa'),
        ('commercial', 'Local comercial'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    building = models.ForeignKey(Building, on_delete=CASCADE, related_name='apartments')
    number = models.CharField(max_length=20)
    floor = models.PositiveIntegerField(blank=True, null=True)
    area_m2 = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    type = models.CharField(max_length=30, choices=TYPE_CHOICES, default='apartment')
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='empty')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['building', 'floor', 'number']
        unique_together = ('building', 'number')
        verbose_name_plural = 'Apartments'
        indexes = [
            models.Index(fields=['building']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.building.garden.name} - {self.building.name} - {self.number}"
    
    @property
    def garden(self):
        """Acceso directo al jardín"""
        return self.building.garden

