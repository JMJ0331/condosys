from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db.models import CASCADE, PROTECT, SET_NULL
import uuid


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


# ==================================================
# CUSTOM USER MODEL
# ==================================================

class User(AbstractUser):
    """
    Custom User model for CONDOSYS
    Extends Django's built-in User with additional fields
    """
    username = None
    email = models.EmailField('email address', unique=True)
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

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

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

