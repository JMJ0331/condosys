from rest_framework import serializers
from .models import Resident
from accounts.serializers import UserSerializer
from structure.serializers import ApartmentListSerializer


class ResidentSerializer(serializers.ModelSerializer):
    """Serializer para Resident"""
    user_detail = UserSerializer(source='user', read_only=True)
    apartment_detail = ApartmentListSerializer(source='apartment', read_only=True)
    is_current = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Resident
        fields = [
            'id', 'user', 'user_detail', 'apartment',
            'apartment_detail', 'role_in_apartment',
            'move_in_date', 'move_out_date',
            'emergency_contact', 'emergency_phone',
            'is_current', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
