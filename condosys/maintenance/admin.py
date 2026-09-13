from django.contrib import admin
from .models import MaintenanceCharge


@admin.register(MaintenanceCharge)
class MaintenanceChargeAdmin(admin.ModelAdmin):
    list_display = ('concept', 'periodicity', 'amount', 'effective_date', 'is_active', 'created_at')
    list_filter = ('concept', 'periodicity', 'is_active', 'effective_date')
    search_fields = ('concept', 'payment_methods')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-effective_date',)
    fieldsets = (
        ('Cargo', {'fields': ('concept', 'periodicity', 'amount')}),
        ('Aplicación', {'fields': ('payment_methods', 'effective_date')}),
        ('Prueba', {'fields': ('photo',)}),
        ('Estado', {'fields': ('is_active',)}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )