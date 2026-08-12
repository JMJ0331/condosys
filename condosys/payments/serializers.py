from rest_framework import serializers
from .models import ChargeType, Payment


class ChargeTypeSerializer(serializers.ModelSerializer):
    """Serializer para ChargeType"""
    
    class Meta:
        model = ChargeType
        fields = ['id', 'name', 'description', 'is_active']


class PaymentSerializer(serializers.ModelSerializer):
    """Serializer para Payment"""
    charge_type_name = serializers.CharField(source='charge_type.name', read_only=True)
    apartment_number = serializers.CharField(source='apartment.number', read_only=True)
    is_overdue = serializers.BooleanField(read_only=True)
    days_until_due = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Payment
        fields = [
            'id', 'apartment', 'apartment_number', 'charge_type',
            'charge_type_name', 'amount', 'description',
            'invoice_date', 'due_date', 'payment_date',
            'status', 'payment_method', 'reference_number',
            'notes', 'is_overdue', 'days_until_due',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_days_until_due(self, obj):
        return obj.days_until_due
