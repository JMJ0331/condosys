from django import forms
from .models import Payment
from residents.models import Resident


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = [
            'apartment', 'resident', 'amount', 'concept',
            'period', 'payment_date', 'payment_method',
            'receipt_image', 'status',
        ]
        widgets = {
            'apartment': forms.Select(attrs={'class': 'select-field', 'placeholder': 'Elegir apartamento'}),
            'resident': forms.Select(attrs={'class': 'select-field', 'placeholder': 'Elegir un propietario/residente'}),
            'amount': forms.NumberInput(attrs={
                'class': 'input-field',
                'placeholder': 'Ejemplo: $15,000',
                'step': '0.01',
                'min': '0',
            }),
            'concept': forms.Select(attrs={'class': 'select-field', 'placeholder': 'Elegir concepto'}),
            'period': forms.DateInput(attrs={'type': 'date', 'class': 'input-field'}),
            'payment_date': forms.DateInput(attrs={'type': 'date', 'class': 'input-field'}),
            'payment_method': forms.Select(attrs={'class': 'select-field', 'placeholder': 'Elegir método de pago'}),
            'receipt_image': forms.ClearableFileInput(attrs={
                'class': 'input-field',
                'accept': 'image/jpeg,image/png,image/webp',
            }),
            'status': forms.Select(attrs={'class': 'select-field', 'placeholder': 'Elegir estado'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['resident'].queryset = Resident.objects.select_related('apartment').all()

    def clean(self):
        cleaned_data = super().clean()
        apartment = cleaned_data.get('apartment')
        resident = cleaned_data.get('resident')
        if apartment and resident and resident.apartment_id != apartment.id:
            self.add_error('resident', 'El residente no pertenece al apartamento seleccionado.')
        return cleaned_data