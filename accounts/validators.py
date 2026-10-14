import re

from django.core.exceptions import ValidationError


def solo_digitos(valor):
    """Descarta todo lo que no sea dígito (guiones, paréntesis, espacios)."""
    return re.sub(r'\D', '', valor or '')


def validar_cedula(valor):
    if valor and len(solo_digitos(valor)) != 11:
        raise ValidationError('La cédula debe tener 11 dígitos.')


def validar_telefono(valor):
    if valor and len(solo_digitos(valor)) != 10:
        raise ValidationError('El teléfono debe tener 10 dígitos.')


def validar_contacto_emergencia(valor):
    if valor and len(solo_digitos(valor)) != 10:
        raise ValidationError('El contacto de emergencia debe tener 10 dígitos.')
