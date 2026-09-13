from django.contrib import admin
from .models import AreaComun


@admin.register(AreaComun)
class AreaComunAdmin(admin.ModelAdmin):
    list_display = ('name', 'area_type', 'capacity', 'available_days', 'status')
    list_filter = ('area_type', 'status', 'available_days')
    search_fields = ('name', 'usage_conditions')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('name',)