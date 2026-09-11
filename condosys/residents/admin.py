from django.contrib import admin
from .models import Resident


@admin.register(Resident)
class ResidentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'cedula', 'apartment', 'email', 'phone', 'is_active')
    list_filter = ('is_active', 'marital_status', 'apartment')
    search_fields = ('full_name', 'cedula', 'email', 'apartment__number')
    ordering = ('apartment', 'full_name')
    readonly_fields = ('created_at', 'updated_at')

    def is_current(self, obj):
        return obj.is_current
    is_current.short_description = 'Currently Active'
    is_current.boolean = True