from django import forms
from .models import AreaComun
from condosys.forms_utils import placeholder


class AreaComunForm(forms.ModelForm):
    class Meta:
        model = AreaComun
        fields = [
            'name', 'area_type', 'capacity',
            'available_from', 'available_until', 'available_days',
            'usage_conditions', 'status',
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'campo-entrada',
                'placeholder': 'Ejemplo: Gazebo',
            }),
            'area_type': forms.Select(attrs={'class': 'campo-seleccion'}),
            'capacity': forms.NumberInput(attrs={
                'class': 'campo-entrada',
                'placeholder': 'Ejemplo: 10 personas',
            }),
            'available_from': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'campo-entrada',
                'placeholder': '--:-- --',
            }),
            'available_until': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'campo-entrada',
                'placeholder': '--:-- --',
            }),
            'available_days': forms.Select(attrs={'class': 'campo-seleccion'}),
            'usage_conditions': forms.Textarea(attrs={
                'class': 'campo-area-texto',
                'placeholder': 'Detallar condiciones de uso y/o reglas de uso',
                'maxlength': '400',
                'data-contador': 'contador-condiciones',
            }),
            'status': forms.Select(attrs={'class': 'campo-seleccion'}),
        }

        labels = {
            'name': 'Nombre',
            'area_type': 'Tipo de área',
            'capacity': 'Capacidad',
            'available_from': 'Disponible desde',
            'available_until': 'Disponible hasta',
            'available_days': 'Días habilitados',
            'usage_conditions': 'Condiciones de uso',
            'status': 'Estado',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Opciones "placeholder" al inicio de cada dropdown de opciones fijas.
        placeholder(self.fields['area_type'], 'Elegir tipo de área')
        placeholder(self.fields['available_days'], 'Elegir días')
        placeholder(self.fields['status'], 'Elegir estado')

    def clean_usage_conditions(self):
        condiciones = self.cleaned_data.get('usage_conditions') or ''
        if len(condiciones) > 400:
            raise forms.ValidationError('Las condiciones de uso no pueden superar los 400 caracteres.')
        return condiciones

    def clean(self):
        cleaned_data = super().clean()
        available_from = cleaned_data.get('available_from')
        available_until = cleaned_data.get('available_until')
        if available_from and available_until and available_until <= available_from:
            self.add_error('available_until', 'El fin debe ser posterior al inicio.')
        return cleaned_data