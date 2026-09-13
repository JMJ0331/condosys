from django import forms
from residents.forms import validate_photo
from .models import Apartment, Building, Garden


class GardenForm(forms.ModelForm):
    """Formulario de alta/edición de jardines."""
    class Meta:
        model = Garden
        fields = ['name', 'location', 'description', 'is_active']


class BuildingForm(forms.ModelForm):
    """Formulario de alta/edición de edificios; placeholders en español."""
    class Meta:
        model = Building
        fields = [
            'garden', 'name', 'tower', 'block',
            'number_of_floors', 'description', 'is_active',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Edificio'}),
            'tower': forms.TextInput(attrs={'placeholder': 'Torre'}),
            'block': forms.TextInput(attrs={'placeholder': 'Bloque'}),
            'description': forms.TextInput(attrs={'placeholder': 'Descripción'}),
        }


class ApartmentsForm(forms.ModelForm):
    """Formulario de departamentos con filtros enlazados a static/js/departamentos.js."""
    class Meta:
        model = Apartment
        fields = [
            'building', 'name', 'owner', 'photo',
            'floor', 'status', 'is_active',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Nombre del departamento'}),
            # data-departamento="edificio": el select de edificios se filtra por el jardín
            # elegido; data-departamento="propietario": select de propietarios con búsqueda.
            'building': forms.Select(attrs={'class': 'campo-seleccion', 'data-departamento': 'edificio'}),
            'owner': forms.Select(attrs={'class': 'campo-seleccion', 'data-departamento': 'propietario', 'data-filtrar': 'owner'}),
            'floor': forms.NumberInput(attrs={'placeholder': 'Piso'}),
            # El estado (occupied/empty) se gestiona con un interruptor visual
            # que vuelca su valor a este campo oculto del formulario.
            'status': forms.HiddenInput(),
        }

    # Campo de imagen reutilizando la validación compartida de residents.forms
    # (solo JPG/PNG/WEBP y máximo 2 MB).
    photo = forms.ImageField(
        required=False,
        label='Imagen',
        validators=[validate_photo],
        widget=forms.ClearableFileInput(attrs={'accept': 'image/jpeg,image/png,image/webp'}),
    )

    def clean_status(self):
        # Si el interruptor nunca se tocó, el campo oculto llega vacío;
        # por defecto el departamento se da de alta como desocupado.
        return self.cleaned_data.get('status') or 'empty'
