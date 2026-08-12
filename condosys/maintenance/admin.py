from django.contrib import admin
from .models import MaintenanceOrder


@admin.register(MaintenanceOrder)
class MaintenanceOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'apartment', 'type', 'status', 'assigned_to', 'scheduled_date')
    list_filter = ('type', 'status', 'scheduled_date')
    search_fields = ('apartment__number', 'assigned_to__email', 'description')
    readonly_fields = ('created_at', 'updated_at', 'completion_date')
    ordering = ('-scheduled_date',)
    fieldsets = (
        ('Order Info', {'fields': ('apartment', 'incident', 'type', 'description')}),
        ('Assignment', {'fields': ('assigned_to',)}),
        ('Schedule', {'fields': ('scheduled_date', 'completion_date')}),
        ('Cost', {'fields': ('estimated_cost', 'actual_cost')}),
        ('Status & Notes', {'fields': ('status', 'notes')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )

