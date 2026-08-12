from django.contrib import admin
from .models import Resident


@admin.register(Resident)
class ResidentAdmin(admin.ModelAdmin):
    list_display = ('user', 'apartment', 'role_in_apartment', 'move_in_date', 'is_current')
    list_filter = ('role_in_apartment', 'move_in_date')
    search_fields = ('user__email', 'apartment__number')
    ordering = ('apartment', '-move_in_date')
    readonly_fields = ('created_at', 'updated_at')

    def is_current(self, obj):
        return obj.is_current
    is_current.short_description = 'Currently Active'
    is_current.boolean = True

