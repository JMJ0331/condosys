from django.contrib import admin
from .models import CommonArea, Reservation


@admin.register(CommonArea)
class CommonAreaAdmin(admin.ModelAdmin):
    list_display = ('name', 'garden', 'capacity', 'is_active', 'created_at')
    list_filter = ('garden', 'is_active')
    search_fields = ('name', 'garden__name')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('common_area', 'apartment', 'resident', 'reserved_by', 'start_time', 'status')
    list_filter = ('common_area', 'status', 'start_time')
    search_fields = ('reserved_by__email', 'common_area__name', 'apartment__name', 'resident__full_name')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-start_time',)
    fieldsets = (
        ('Reservation Info', {'fields': ('common_area', 'apartment', 'resident', 'reserved_by', 'reason', 'expected_guests')}),
        ('Schedule', {'fields': ('start_time', 'end_time')}),
        ('Status', {'fields': ('status', 'approved_by')}),
        ('Notes', {'fields': ('notes',)}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )

