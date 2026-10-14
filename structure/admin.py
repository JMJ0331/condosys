from django.contrib import admin
from .models import Garden, Block, Building, Apartment


@admin.register(Garden)
class GardenAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'location')
    ordering = ('-created_at',)


@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    list_display = ('name', 'garden', 'is_active', 'created_at')
    list_filter = ('garden', 'is_active')
    search_fields = ('name', 'garden__name')
    ordering = ('garden', 'name')


@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ('name', 'block', 'garden', 'number_of_floors', 'is_active', 'created_at')
    list_filter = ('garden', 'block', 'is_active', 'created_at')
    search_fields = ('name', 'garden__name', 'block__name')
    ordering = ('garden', 'block', 'name')


@admin.register(Apartment)
class ApartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'building', 'owner', 'floor', 'status', 'is_active')
    list_filter = ('building', 'status', 'is_active')
    search_fields = ('name', 'building__name', 'owner__full_name')
    ordering = ('building', 'floor', 'name')

