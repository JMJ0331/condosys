from rest_framework import serializers

from .models import Residencial


class ResidencialSerializer(serializers.ModelSerializer):
    """Serializer del registro único del residencial."""

    class Meta:
        model = Residencial
        fields = [
            'id', 'nombre', 'rnc',
            'nombre_via', 'numero_edificacion', 'sector', 'codigo_postal',
            'municipio', 'provincia', 'mapa_iframe',
            'distribucion', 'cantidad_edificios', 'cantidad_pisos',
            'telefono', 'correo',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
