from django.contrib import admin
from .models import ChatMessage


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'group_name', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('sender__email', 'receiver__email', 'message', 'group_name')
    readonly_fields = ('created_at', 'read_at')
    ordering = ('-created_at',)
    fieldsets = (
        ('Message Info', {'fields': ('sender', 'message')}),
        ('Recipients', {'fields': ('receiver', 'group_name')}),
        ('Read Status', {'fields': ('is_read', 'read_at')}),
        ('Timestamps', {'fields': ('created_at',)}),
    )

