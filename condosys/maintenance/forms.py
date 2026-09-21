from django import forms
from django.core.exceptions import ValidationError
from structure.models import Apartment
from .models import MaintenanceCharge
from condosys.forms_utils import placeholder

TIPOS_FOTO = ('.jpg', '.jpeg', '.png', '.webp')
MAX_FOTO_MB = 2


class MaintenanceChargeForm(forms.ModelForm):
    class Meta:
        model = MaintenanceCharge
        fields = [
            'concept', 'periodicity', 'amount', 'apartment',
            'effective_date', 'photo', 'is_active',
        ]
        widgets = {
            'concept': forms.Select(attrs={'class': 'campo-seleccion'}),
            'periodicity': forms.Select(attrs={'class': 'campo-seleccion'}),
            'apartment': forms.Select(attrs={
                'class': 'campo-seleccion',
                'data-mantenimiento': 'departamento',
            }),
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
            'photo': forms.FileInput(attrs={
                'accept': 'image/jpeg,image/png,image/webp',
                'data-foto-mantenimiento': '',
                'tabindex': '-1',
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'entrada-interruptor',
            }),
        }

        labels = {
            'concept': 'Concepto',
            'periodicity': 'Periodicidad',
            'amount': 'Monto',
            'apartment': 'Departamentos (si es aplicable)',
            'effective_date': 'Fecha de generación',
            'photo': 'Foto del mantenimiento',
            'is_active': 'Activo',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Opciones "placeholder" al inicio de cada dropdown de opciones fijas.
        placeholder(self.fields['concept'], 'Elegir concepto')
        placeholder(self.fields['periodicity'], 'Elegir periodicidad')
        self.fields['apartment'].queryset = Apartment.objects.filter(is_active=True)
        self.fields['apartment'].empty_label = 'Elegir departamento'
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