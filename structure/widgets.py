"""Widgets para los selects en cascada Jardín → Bloque → Edificio → Departamento.

Cada opción lleva en atributos data-* los ids de sus ancestros (data-jardin,
data-bloque, data-edificio) para que static/js/cascada.js filtre los niveles
inferiores al elegir uno superior, y rellene los superiores al elegir uno
inferior. El select (o cada casilla) lleva data-cascada con su nivel.
"""
from django import forms

from .models import Apartment, Block, Building


def datos_cascada(instancia):
    """Atributos data-* con los ancestros de un elemento de la jerarquía."""
    if isinstance(instancia, Block):
        return {'data-jardin': str(instancia.garden_id)}
    if isinstance(instancia, Building):
        return {
            'data-jardin': str(instancia.garden_id),
            'data-bloque': str(instancia.block_id),
        }
    if isinstance(instancia, Apartment):
        edificio = instancia.building
        return {
            'data-jardin': str(edificio.garden_id),
            'data-bloque': str(edificio.block_id),
            'data-edificio': str(edificio.id),
            'data-propietario': instancia.owner.full_name if instancia.owner_id else '',
        }
    return {}


class _OpcionesCascadaMixin:
    def __init__(self, nivel, attrs=None):
        super().__init__({'data-cascada': nivel, **(attrs or {})})

    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        opcion = super().create_option(name, value, label, selected, index, subindex, attrs)
        instancia = getattr(value, 'instance', None)
        if instancia is not None:
            opcion['attrs'].update(datos_cascada(instancia))
        return opcion


class SelectCascada(_OpcionesCascadaMixin, forms.Select):
    def __init__(self, nivel, attrs=None):
        super().__init__(nivel, {'class': 'campo-seleccion', **(attrs or {})})


class CasillasCascada(_OpcionesCascadaMixin, forms.CheckboxSelectMultiple):
    """Lista de casillas (p. ej. departamentos de un propietario)."""
