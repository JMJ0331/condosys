from django.contrib import admin
from .models import Incident, IncidentHistory, IncidentImage


class IncidentImageInline(admin.TabularInline):
    model = IncidentImage
    extra = 0


@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
    list_display = ('id', 'apartment', 'category', 'priority', 'status', 'reported_by', 'created_at')
    list_filter = ('category', 'priority', 'status', 'created_at')
    search_fields = ('title', 'apartment__number', 'reported_by__email')
    readonly_fields = ('created_at', 'updated_at', 'resolved_at')
    inlines = [IncidentImageInline]
    ordering = ('-created_at',)
    fieldsets = (
        ('Basic Info', {'fields': ('apartment', 'category', 'priority', 'title', 'description')}),
        ('Status', {'fields': ('status', 'reported_by', 'assigned_to', 'resolution_notes', 'resolved_at')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )


@admin.register(IncidentHistory)
class IncidentHistoryAdmin(admin.ModelAdmin):
    list_display = ('incident', 'status_from', 'status_to', 'changed_by', 'created_at')
    list_filter = ('created_at', 'status_from', 'status_to')
    search_fields = ('incident__id', 'changed_by__email')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

