from rest_framework import serializers
from residents.models import Resident
from structure.serializers import ApartmentListSerializer


class PropietarioSerializer(serializers.ModelSerializer):
    """Serializer de propietarios: residentes dueños de apartamentos."""
    apartment_detail = ApartmentListSerializer(source='apartment', read_only=True)
    owned_apartments = serializers.SerializerMethodField()
    photo_url = serializers.SerializerMethodField()

    class Meta:
        model = Resident
        fields = [
            'id', 'full_name', 'cedula', 'phone', 'email',
            'photo', 'photo_url',
            'apartment', 'apartment_detail', 'owned_apartments',
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