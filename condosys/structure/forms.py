from django import forms
from residents.forms import validate_photo
from .models import Apartment


class ApartmentsForm(forms.ModelForm):
    """Formulario de departamentos con filtros enlazados a static/js/departamentos.js."""
    class Meta:
        model = Apartment
        fields = [
            'building', 'name', 'owner', 'photo',
            'floor', 'status', 'is_active',
        ]
        labels = {
            'name': 'Apartamento',
            'building': 'Edificio',
            'owner': 'Propietario',
            'photo': 'Imagen',
            'floor': 'Piso',
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'nombre del departamento'}),
            # data-departamento="edificio": el select de edificios se filtra por el jardín
            # elegido; data-departamento="propietario": select de propietarios.
            'building': forms.Select(attrs={'class': 'campo-seleccion', 'data-departamento': 'edificio'}),
            'owner': forms.Select(attrs={'class': 'campo-seleccion', 'data-departamento': 'propietario'}),
            'floor': forms.NumberInput(attrs={'placeholder': 'Piso'}),
            # El estado (occupied/empty) se gestiona con un interruptor visual
            # que vuelca su valor a este campo oculto del formulario.
            'status': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['building'].empty_label = 'Edificio'
        self.fields['owner'].empty_label = 'Elegir propietario'

    # Campo de imagen reutilizando la validación compartida de residents.forms
    # (solo JPG/PNG/WEBP y máximo 2 MB). FileInput simple: sin los textos
    # en inglés del ClearableFileInput ("Choose file", "Currently"...).
    photo = forms.ImageField(
        required=False,
        label='Imagen',
        validators=[validate_photo],
        widget=forms.FileInput(attrs={
            'accept': 'image/jpeg,image/png,image/webp',
            'data-departamento': 'foto',
            'tabindex': '-1',
        }),
    )

    def clean_status(self):
        # Si el interruptor nunca se tocó, el campo oculto llega vacío;
        # por defecto el departamento se da de alta como desocupado.
        return self.cleaned_data.get('status') or 'empty'
