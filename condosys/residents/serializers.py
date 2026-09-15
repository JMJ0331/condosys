from rest_framework import serializers
from .models import Resident
from accounts.serializers import UserSerializer
from structure.serializers import ApartmentListSerializer


class ResidentSerializer(serializers.ModelSerializer):
    """Serializer para Resident"""
    user_detail = UserSerializer(source='user', read_only=True, allow_null=True)
    apartment_detail = ApartmentListSerializer(source='apartment', read_only=True)
    is_current = serializers.BooleanField(read_only=True)
    photo_url = serializers.SerializerMethodField()

    class Meta:
        model = Resident
        fields = [
            'id', 'user', 'user_detail', 'apartment', 'apartment_detail',
            'full_name', 'marital_status', 'cedula', 'photo', 'photo_url',
            'phone', 'email', 'emergency_contact',
            'tipo_relacion', 'fecha_ingreso', 'mascotas',
            'is_active', 'is_current', 'created_at', 'updated_at'
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