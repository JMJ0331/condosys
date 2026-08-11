from django.contrib import admin
from .models import Garden, Building, Apartment


@admin.register(Garden)
class GardenAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'location')
    ordering = ('-created_at',)


@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ('name', 'garden', 'number_of_floors', 'is_active', 'created_at')
    list_filter = ('garden', 'is_active', 'created_at')
    search_fields = ('name', 'garden__name')
    ordering = ('garden', 'name')


@admin.register(Apartment)
class ApartmentAdmin(admin.ModelAdmin):
    list_display = ('number', 'building', 'floor', 'type', 'status', 'is_active')
    list_filter = ('building', 'type', 'status', 'is_active')
    search_fields = ('number', 'building__name')
    ordering = ('building', 'floor', 'number')

