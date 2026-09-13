from rest_framework import serializers
from .models import MaintenanceCharge


class MaintenanceChargeListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para MaintenanceCharge (listados)"""
    class Meta:
        model = MaintenanceCharge
        fields = [
            'id', 'concept', 'periodicity', 'amount',
            'effective_date', 'is_active', 'payment_methods', 'created_at',
        ]
        read_only_fields = ['id', 'payment_methods', 'created_at']


class MaintenanceChargeDetailSerializer(serializers.ModelSerializer):
    """Serializer detallado para MaintenanceCharge"""
    class Meta:
        model = MaintenanceCharge
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']