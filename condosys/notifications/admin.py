from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'type', 'title', 'is_read', 'created_at')
    list_filter = ('type', 'is_read', 'created_at')
    search_fields = ('user__email', 'title', 'message')
    readonly_fields = ('created_at', 'read_at')
    ordering = ('-created_at',)
    fieldsets = (
        ('Notification Info', {'fields': ('user', 'type', 'title', 'message')}),
        ('Reference', {'fields': ('related_id',)}),
        ('Read Status', {'fields': ('is_read', 'read_at')}),
        ('Timestamps', {'fields': ('created_at',)}),
    )

