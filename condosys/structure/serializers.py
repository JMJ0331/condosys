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
            'tower', 'block',
            'number_of_floors', 'description',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ApartmentListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para Apartment (listados)"""
    building_name = serializers.CharField(source='building.name', read_only=True)
    garden_name = serializers.CharField(source='building.garden.name', read_only=True)
    owner_name = serializers.CharField(source='owner.full_name', read_only=True)
    photo_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Apartment
        fields = [
            'id', 'building', 'building_name', 'garden_name',
            'name', 'owner', 'owner_name', 'photo', 'photo_url',
            'floor', 'status',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_photo_url(self, obj):
        if obj.photo:
            request = self.context.get('request')
            url = obj.photo.url
            if request is not None:
                return request.build_absolute_uri(url)
            return url
        return None


class ApartmentDetailSerializer(serializers.ModelSerializer):
    """Serializer detallado para Apartment"""
    building_detail = BuildingSerializer(source='building', read_only=True)
    garden = serializers.SerializerMethodField(read_only=True)
    owner_name = serializers.CharField(source='owner.full_name', read_only=True)
    photo_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Apartment
        fields = [
            'id', 'building', 'building_detail', 'garden',
            'name', 'owner', 'owner_name', 'photo', 'photo_url',
            'floor', 'status',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_garden(self, obj):
        return {
            'id': str(obj.building.garden.id),
            'name': obj.building.garden.name
        }

    def get_photo_url(self, obj):
        if obj.photo:
            request = self.context.get('request')
            url = obj.photo.url
            if request is not None:
                return request.build_absolute_uri(url)
            return url
        return None
