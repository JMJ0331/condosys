from rest_framework import serializers
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    """Serializer para Payment"""
    apartment_name = serializers.CharField(source='apartment.name', read_only=True)
    resident_name = serializers.CharField(source='resident.full_name', read_only=True)
    concept_display = serializers.CharField(source='get_concept_display', read_only=True)
    receipt_image_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Payment
        fields = [
            'id', 'apartment', 'apartment_name', 'resident', 'resident_name',
            'amount', 'concept', 'concept_display', 'period',
            'payment_date', 'payment_method', 'receipt_image', 'receipt_image_url',
            'status', 'registered_by', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_receipt_image_url(self, obj):
        if obj.receipt_image:
            request = self.context.get('request')
            url = obj.receipt_image.url
            if request is not None:
                return request.build_absolute_uri(url)
            return url
        return None