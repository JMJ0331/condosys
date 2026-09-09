from django import forms
from .models import ChargeType, Payment


class ChargeTypeForm(forms.ModelForm):
    class Meta:
        model = ChargeType
        fields = ['name', 'description', 'is_active']


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = [
            'apartment', 'charge_type', 'amount', 'description',
            'invoice_date', 'due_date', 'payment_date', 'status',
            'payment_method', 'reference_number', 'notes',
        ]
