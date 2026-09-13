from rest_framework import serializers
from .models import AreaComun


class AreaComunSerializer(serializers.ModelSerializer):
    """Serializer para AreaComun"""
    area_type_display = serializers.CharField(source='get_area_type_display', read_only=True)
    available_days_display = serializers.CharField(source='get_available_days_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = AreaComun
        fields = [
            'id', 'name', 'area_type', 'area_type_display',
            'capacity',
            'available_from', 'available_until', 'available_days', 'available_days_display',
            'usage_conditions',
            'status', 'status_display',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']