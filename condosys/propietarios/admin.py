from django.contrib import admin
from .models import Propietario


@admin.register(Propietario)
class PropietarioAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'cedula', 'email', 'phone', 'is_active')
    list_filter = ('is_active', 'marital_status')
    search_fields = ('full_name', 'cedula', 'email')
    ordering = ('full_name',)
    readonly_fields = ('created_at', 'updated_at')
