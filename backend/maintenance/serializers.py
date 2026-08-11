from rest_framework import serializers
from .models import MaintenanceOrder


class MaintenanceOrderListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para MaintenanceOrder (listados)"""
    assigned_to_email = serializers.CharField(source='assigned_to.email', read_only=True)
    apartment_number = serializers.CharField(source='apartment.number', read_only=True, allow_null=True)
    
    class Meta:
        model = MaintenanceOrder
        fields = [
            'id', 'apartment', 'apartment_number', 'type', 'status',
            'assigned_to', 'assigned_to_email',
            'scheduled_date', 'completion_date', 'created_at'
        ]
        read_only_fields = ['id', 'completion_date', 'created_at']


class MaintenanceOrderDetailSerializer(serializers.ModelSerializer):
    """Serializer detallado para MaintenanceOrder"""
    assigned_to_email = serializers.CharField(source='assigned_to.email', read_only=True)
    apartment_number = serializers.CharField(source='apartment.number', read_only=True, allow_null=True)
    incident_id = serializers.CharField(source='incident.id', read_only=True, allow_null=True)
    
    class Meta:
        model = MaintenanceOrder
        fields = [
            'id', 'incident', 'incident_id', 'apartment',
            'apartment_number', 'type', 'description',
            'assigned_to', 'assigned_to_email',
            'status', 'scheduled_date', 'completion_date',
            'estimated_cost', 'actual_cost', 'notes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'completion_date', 'created_at', 'updated_at']
