from django.contrib import admin
from .models import Communication


@admin.register(Communication)
class CommunicationAdmin(admin.ModelAdmin):
    list_display = ('title', 'garden', 'sender', 'target_type', 'is_published', 'created_at')
    list_filter = ('garden', 'target_type', 'is_published', 'published_at', 'created_at')
    search_fields = ('title', 'body', 'sender__email')
    readonly_fields = ('created_at', 'updated_at', 'published_at')
    ordering = ('-published_at', '-created_at')
    fieldsets = (
        ('Basic Info', {'fields': ('garden', 'sender', 'title', 'body')}),
        ('Targeting', {'fields': ('target_type', 'target_id')}),
        ('Publishing', {'fields': ('is_published', 'published_at')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )

