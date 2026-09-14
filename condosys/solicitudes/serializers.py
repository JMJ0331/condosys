from rest_framework import serializers
from .models import Solicitud


class SolicitudSerializer(serializers.ModelSerializer):
    """Serializer para Solicitud"""
    apartment_name = serializers.CharField(source='apartment.name', read_only=True)
    resident_full_name = serializers.CharField(
        source='resident.full_name', read_only=True, allow_null=True
    )

    class Meta:
        model = Solicitud
        fields = [
            'id', 'apartment', 'apartment_name', 'resident', 'resident_full_name',
            'request_type', 'description', 'request_date', 'attachment',
            'tracking_response', 'status', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']