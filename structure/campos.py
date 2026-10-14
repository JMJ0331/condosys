"""Campos de formulario reutilizables para la jerarquía en cascada
Jardín → Bloque → Edificio (ver structure/widgets.py y static/js/cascada.js).

Viven aparte de structure/forms.py para que otras apps (propietarios,
residentes) los importen sin crear importaciones circulares.
"""
from django import forms

from .models import Block, Building, Garden
from .widgets import SelectCascada


def campo_jardin(required=False, label='Jardín'):
    return forms.ModelChoiceField(
        queryset=Garden.objects.filter(is_active=True),
        required=required,
        label=label,
        empty_label='Elegir jardín',
        widget=SelectCascada('jardin'),
    )


def campo_bloque(required=False, label='Bloque'):
    return forms.ModelChoiceField(
        queryset=Block.objects.filter(is_active=True).select_related('garden'),
        required=required,
        label=label,
        empty_label='Elegir bloque',
        widget=SelectCascada('bloque'),
    )


def campo_edificio(required=False, label=None):
    if label is None:
        try:
            from residencial.models import Residencial
            residencial = Residencial.obtener_unico()
            es_torres = bool(residencial and residencial.distribucion == 'torres')
        except Exception:
            es_torres = False
        label = 'Torre' if es_torres else 'Edificio'
    return forms.ModelChoiceField(
        queryset=Building.objects.filter(is_active=True).select_related('garden', 'block'),
        required=required,
        label=label,
        empty_label=f'Elegir {label.lower()}',
        widget=SelectCascada('edificio'),
    )


def incluir_actual(queryset, actual):
    """Añade al queryset el valor actual de la instancia aunque esté inactivo."""
    if actual is None:
        return queryset
    return (queryset | queryset.model.objects.filter(pk=actual.pk)).distinct()
