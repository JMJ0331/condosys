from rest_framework import serializers
from .models import Garden, Building, Apartment


class GardenSerializer(serializers.ModelSerializer):
    """Serializer para Garden"""
    
    class Meta:
        model = Garden
        fields = [
            'id', 'name', 'location', 'description',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class BuildingSerializer(serializers.ModelSerializer):
    """Serializer para Building"""
    garden_name = serializers.CharField(source='garden.name', read_only=True)
    
    class Meta:
        model = Building
        fields = [
            'id', 'garden', 'garden_name', 'name',
            'number_of_floors', 'description',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ApartmentListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para Apartment (listados)"""
    building_name = serializers.CharField(source='building.name', read_only=True)
    garden_name = serializers.CharField(source='building.garden.name', read_only=True)
    
    class Meta:
        model = Apartment
        fields = [
            'id', 'building', 'building_name', 'garden_name',
            'number', 'floor', 'area_m2', 'type', 'status',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ApartmentDetailSerializer(serializers.ModelSerializer):
    """Serializer detallado para Apartment"""
    building_detail = BuildingSerializer(source='building', read_only=True)
    garden = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Apartment
        fields = [
            'id', 'building', 'building_detail', 'garden',
            'number', 'floor', 'area_m2', 'type', 'status',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_garden(self, obj):
        return {
            'id': str(obj.building.garden.id),
            'name': obj.building.garden.name
        }
