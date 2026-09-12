from django import forms
from residents.forms import validate_photo
from .models import Apartment, Building, Garden


class GardenForm(forms.ModelForm):
    class Meta:
        model = Garden
        fields = ['name', 'location', 'description', 'is_active']


class BuildingForm(forms.ModelForm):
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
    class Meta:
        model = Apartment
        fields = [
            'building', 'name', 'owner', 'photo',
            'floor', 'status', 'is_active',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Nombre del departamento'}),
            'building': forms.Select(attrs={'class': 'select-field'}),
            'owner': forms.Select(attrs={'class': 'select-field', 'data-filtrar': 'owner'}),
            'floor': forms.NumberInput(attrs={'placeholder': 'Piso'}),
            'status': forms.HiddenInput(),
        }

    photo = forms.ImageField(
        required=False,
        label='Imagen',
        validators=[validate_photo],
        widget=forms.ClearableFileInput(attrs={'accept': 'image/jpeg,image/png,image/webp'}),
    )

    def clean_status(self):
        return self.cleaned_data.get('status') or 'empty'
