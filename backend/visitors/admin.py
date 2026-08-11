from django.contrib import admin
from .models import Visitor


@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display = ('name', 'apartment', 'type', 'status', 'scheduled_entry', 'actual_entry')
    list_filter = ('type', 'status', 'scheduled_entry')
    search_fields = ('name', 'document', 'apartment__number')
    readonly_fields = ('created_at', 'updated_at', 'actual_entry', 'actual_exit')
    ordering = ('-scheduled_entry',)
    fieldsets = (
        ('Visitor Info', {'fields': ('name', 'document', 'phone', 'type')}),
        ('Apartment & Registration', {'fields': ('apartment', 'registered_by')}),
        ('Schedule', {'fields': ('scheduled_entry', 'scheduled_exit', 'actual_entry', 'actual_exit')}),
        ('Authorization', {'fields': ('status', 'authorized_by', 'reason', 'vehicle_plate', 'notes')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )

