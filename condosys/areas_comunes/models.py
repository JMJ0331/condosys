from django.db import models
import uuid


class AreaComun(models.Model):
    """
    Área común del residencial (gazebo, salón, piscina, etc.)
    Vista como módulo propio (areas_comunes) con su información completa.
    """

    TIPO_AREA_CHOICES = (
        ('gazebo', 'Gazebo'),
        ('salon_eventos', 'Salón de eventos'),
        ('area_social', 'Área social'),
        ('piscina', 'Piscina'),
        ('cancha_deportiva', 'Cancha deportiva'),
        ('gimnasio', 'Gimnasio'),
        ('zona_parrillas', 'Zona de parrillas'),
        ('otro', 'Otro'),
    )

    DIAS_HABILITADOS_CHOICES = (
        ('todos', 'Todos los días'),
        ('lun_vie', 'Lunes a Viernes'),
        ('fines_semana', 'Fines de semana'),
        ('personalizado', 'Personalizado'),
    )

    ESTADO_CHOICES = (
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
        ('mantenimiento', 'En mantenimiento'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    area_type = models.CharField(max_length=30, choices=TIPO_AREA_CHOICES)
    capacity = models.PositiveIntegerField(blank=True, null=True)

    available_from = models.TimeField(blank=True, null=True)
    available_until = models.TimeField(blank=True, null=True)
    available_days = models.CharField(max_length=20, choices=DIAS_HABILITADOS_CHOICES)

    usage_conditions = models.TextField(blank=True, null=True)

    status = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='activo')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Áreas Comunes'

    def __str__(self):
        return f"{self.get_area_type_display()} - {self.name}"