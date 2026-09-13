from rest_framework import serializers
from .models import Visitor
from accounts.serializers import UserSerializer


class VisitorSerializer(serializers.ModelSerializer):
    """Serializer para Visitor"""
    registered_by_email = serializers.CharField(source='registered_by.email', read_only=True)
    authorized_by_email = serializers.CharField(source='authorized_by.email', read_only=True, allow_null=True)
    apartment_name = serializers.CharField(source='apartment.name', read_only=True)
    document_type_display = serializers.CharField(source='get_document_type_display', read_only=True)

    class Meta:
        model = Visitor
        fields = [
            'id', 'apartment', 'apartment_name', 'name', 'document',
            'document_type', 'document_type_display', 'document_image',
            'phone', 'reason', 'type', 'vehicle_plate',
            'registered_by', 'registered_by_email',
            'scheduled_entry', 'scheduled_exit',
            'actual_entry', 'actual_exit',
            'status', 'authorized_by', 'authorized_by_email',
            'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'actual_entry', 'actual_exit', 'created_at', 'updated_at']
