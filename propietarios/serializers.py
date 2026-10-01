from rest_framework import serializers
from .models import Propietario
from structure.serializers import ApartmentListSerializer


class PropietarioSerializer(serializers.ModelSerializer):
    """Serializer de propietarios con sus apartamentos propios."""
    owned_apartments = serializers.SerializerMethodField()
    photo_url = serializers.SerializerMethodField()

    class Meta:
        model = Propietario
        fields = [
            'id', 'user', 'full_name', 'marital_status', 'cedula',
            'phone', 'email', 'emergency_contact',
            'photo', 'photo_url',
            'owned_apartments',
            'is_active', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_owned_apartments(self, obj):
        return [
            {
                'id': str(apartment.id),
                'name': (
                    f'{apartment.building.garden.name} - '
                    f'{apartment.building.name} - {apartment.name}'
                ),
            }
            for apartment in obj.apartments_owned.all()
        ]

    def get_photo_url(self, obj):
        if obj.photo:
            request = self.context.get('request')
            url = obj.photo.url
            if request is not None:
                return request.build_absolute_uri(url)
            return url
        return None
