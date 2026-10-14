from django.db import models
from django.db.models import CASCADE, PROTECT, SET_NULL
import uuid

# ==================================================
# ESTRUCTURA FÍSICA: Jardín → Bloque → Edificio → Apartamento
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


class Block(models.Model):
    """
    Bloque
    Pertenece a un Jardín y agrupa edificios (torres)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    garden = models.ForeignKey(Garden, on_delete=PROTECT, related_name='blocks')
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['garden', 'name']
        unique_together = ('garden', 'name')
        verbose_name_plural = 'Blocks'

    def __str__(self):
        return f"{self.garden.name} - {self.name}"


class Building(models.Model):
    """
    Edificio (torre)
    Pertenece a un Bloque; `garden` se mantiene sincronizado con el del bloque
    para conservar los filtros existentes por jardín.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    garden = models.ForeignKey(Garden, on_delete=PROTECT, related_name='buildings')
    block = models.ForeignKey(Block, on_delete=PROTECT, related_name='buildings')
    name = models.CharField(max_length=50)
    number_of_floors = models.PositiveIntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['garden', 'block', 'name']
        unique_together = ('block', 'name')
        verbose_name_plural = 'Buildings'
        indexes = [
            models.Index(fields=['garden']),
        ]
    
    def __str__(self):
        return f"{self.garden.name} - {self.block.name} - {self.name}"

    def save(self, *args, **kwargs):
        if self.block_id:
            self.garden_id = self.block.garden_id
        elif self.garden_id:
            # Compatibilidad: un edificio creado solo con jardín cae en el bloque "General".
            self.block, _ = Block.objects.get_or_create(garden_id=self.garden_id, name='General')
        super().save(*args, **kwargs)


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
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    building = models.ForeignKey(Building, on_delete=PROTECT, related_name='apartments')
    name = models.CharField(max_length=50, help_text='Nombre del departamento')
    owner = models.ForeignKey(
        'propietarios.Propietario',
        on_delete=SET_NULL,
        related_name='apartments_owned',
        null=True,
        blank=True,
        help_text='Propietario del departamento',
    )
    photo = models.ImageField(
        upload_to='apartments/',
        blank=True,
        null=True,
        help_text='Imagen del departamento',
    )
    floor = models.PositiveIntegerField(blank=True, null=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='empty')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['building', 'floor', 'name']
        unique_together = ('building', 'name')
        verbose_name_plural = 'Apartments'
        indexes = [
            models.Index(fields=['building']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.building.garden.name} - {self.building.name} - {self.name}"
    
    @property
    def garden(self):
        """Acceso directo al jardín"""
        return self.building.garden

