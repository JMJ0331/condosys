from django import forms
from django.core.exceptions import ValidationError
from .models import MaintenanceCharge

TIPOS_FOTO = ('.jpg', '.jpeg', '.png', '.webp')
MAX_FOTO_MB = 2


class MaintenanceChargeForm(forms.ModelForm):
    class Meta:
        model = MaintenanceCharge
        fields = [
            'concept', 'periodicity', 'amount',
            'payment_methods', 'effective_date', 'photo', 'is_active',
        ]
        widgets = {
            'concept': forms.Select(attrs={'class': 'campo-seleccion'}),
            'periodicity': forms.Select(attrs={'class': 'campo-seleccion'}),
            'payment_methods': forms.Select(attrs={'class': 'campo-seleccion'}),
            'amount': forms.NumberInput(attrs={
                'class': 'campo-entrada',
                'placeholder': 'Ejemplo: $15,000',
                'step': '0.01',
                'min': '0',
            }),
            'effective_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'campo-entrada',
            }),
            'photo': forms.ClearableFileInput(attrs={
                'class': 'campo-entrada',
                'accept': 'image/jpeg,image/png,image/webp',
                'data-foto-mantenimiento': '',
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'entrada-interruptor',
            }),
        }

        labels = {
            'concept': 'Concepto',
            'periodicity': 'Periodicidad',
            'amount': 'Monto',
            'payment_methods': 'Método de pago',
            'effective_date': 'Fecha de generación/vigencia',
            'photo': 'Foto del mantenimiento',
            'is_active': 'Activo',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Opciones "placeholder" al inicio de cada dropdown de opciones fijas.
        self.fields['concept'].choices = [('', 'Elegir concepto')] + list(self.fields['concept'].choices)
        self.fields['periodicity'].choices = [('', 'Elegir periodicidad')] + list(self.fields['periodicity'].choices)
        self.fields['payment_methods'].choices = [('', 'Elegir método de pago')] + list(self.fields['payment_methods'].choices)
        # El cargo nuevo viene activo por defecto.
        self.fields['is_active'].initial = True

    def clean_photo(self):
        archivo = self.cleaned_data.get('photo')
        if not archivo:
            return archivo
        if archivo.size > MAX_FOTO_MB * 1024 * 1024:
            raise ValidationError(f'El archivo supera el límite de {MAX_FOTO_MB} MB.')
        extension = f'.{archivo.name.rsplit(".", 1)[-1].lower()}'
        if extension not in TIPOS_FOTO:
            raise ValidationError('Formato no permitido. Usa JPG, PNG o WEBP.')
        return archivo