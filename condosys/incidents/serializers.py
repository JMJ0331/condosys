from rest_framework import serializers
from .models import Incident, IncidentHistory
from condosys.accounts.serializers import UserSerializer


class IncidentHistorySerializer(serializers.ModelSerializer):
    """Serializer para IncidentHistory"""
    changed_by_detail = UserSerializer(source='changed_by', read_only=True)
    
    class Meta:
        model = IncidentHistory
        fields = [
            'id', 'incident', 'status_from', 'status_to',
            'changed_by', 'changed_by_detail', 'comment', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class IncidentListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para Incident (listados)"""
    reported_by_email = serializers.CharField(source='reported_by.email', read_only=True)
    assigned_to_email = serializers.CharField(source='assigned_to.email', read_only=True, allow_null=True)
    apartment_number = serializers.CharField(source='apartment.number', read_only=True)
    
    class Meta:
        model = Incident
        fields = [
            'id', 'apartment', 'apartment_number', 'category',
            'priority', 'title', 'status', 'reported_by',
            'reported_by_email', 'assigned_to', 'assigned_to_email',
            'created_at', 'resolved_at'
        ]
        read_only_fields = ['id', 'created_at', 'resolved_at']


class IncidentDetailSerializer(serializers.ModelSerializer):
    """Serializer detallado para Incident"""
    reported_by_detail = UserSerializer(source='reported_by', read_only=True)
    assigned_to_detail = UserSerializer(source='assigned_to', read_only=True)
    history = IncidentHistorySerializer(source='incidenthistory_set', many=True, read_only=True)
    
    class Meta:
        model = Incident
        fields = [
            'id', 'apartment', 'category', 'priority', 'title',
            'description', 'status', 'reported_by', 'reported_by_detail',
            'assigned_to', 'assigned_to_detail', 'resolution_notes',
            'image_urls', 'history', 'created_at', 'updated_at', 'resolved_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'resolved_at', 'history']
