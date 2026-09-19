from django.contrib import admin

from .models import Residencial


@admin.register(Residencial)
class ResidencialAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'rnc', 'municipio', 'provincia', 'telefono', 'correo', 'updated_at')
    list_filter = ('provincia', 'distribucion')
    search_fields = ('nombre', 'rnc', 'sector', 'municipio', 'telefono', 'correo')
    ordering = ('-updated_at',)
