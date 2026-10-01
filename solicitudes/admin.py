from django.contrib import admin
from .models import Solicitud


@admin.register(Solicitud)
class SolicitudAdmin(admin.ModelAdmin):
    list_display = ('description', 'request_type', 'apartment', 'resident', 'status', 'request_date')
    list_filter = ('request_type', 'status', 'request_date', 'created_at')
    search_fields = ('description', 'apartment__name', 'resident__full_name')
    readonly_fields = ('id', 'created_at', 'updated_at')
    ordering = ('-created_at',)