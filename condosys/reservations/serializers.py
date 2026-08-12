from rest_framework import serializers
from .models import CommonArea, Reservation
from condosys.accounts.serializers import UserSerializer


class CommonAreaSerializer(serializers.ModelSerializer):
    """Serializer para CommonArea"""
    garden_name = serializers.CharField(source='garden.name', read_only=True)
    
    class Meta:
        model = CommonArea
        fields = [
            'id', 'garden', 'garden_name', 'name',
            'description', 'capacity', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ReservationListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para Reservation (listados)"""
    common_area_name = serializers.CharField(source='common_area.name', read_only=True)
    reserved_by_email = serializers.CharField(source='reserved_by.email', read_only=True)
    
    class Meta:
        model = Reservation
        fields = [
            'id', 'common_area', 'common_area_name',
            'reserved_by', 'reserved_by_email',
            'start_time', 'end_time', 'reason',
            'expected_guests', 'status', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class ReservationDetailSerializer(serializers.ModelSerializer):
    """Serializer detallado para Reservation"""
    common_area_detail = CommonAreaSerializer(source='common_area', read_only=True)
    reserved_by_detail = UserSerializer(source='reserved_by', read_only=True)
    approved_by_detail = UserSerializer(source='approved_by', read_only=True)
    
    class Meta:
        model = Reservation
        fields = [
            'id', 'common_area', 'common_area_detail',
            'reserved_by', 'reserved_by_detail',
            'start_time', 'end_time', 'reason', 'expected_guests',
            'status', 'approved_by', 'approved_by_detail',
            'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
