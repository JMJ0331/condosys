from django import forms
from residents.forms import validate_photo
from residencial.models import Residencial
from .campos import campo_bloque, campo_edificio, campo_jardin, incluir_actual
from .models import Apartment, Block, Building, Garden


class GardenForm(forms.ModelForm):
    class Meta:
        model = Garden
        fields = ['name', 'location', 'description', 'is_active']
        labels = {
            'name': 'Nombre',
            'location': 'Ubicación',
            'description': 'Descripción',
            'is_active': 'Activo',
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Nombre del jardín'}),
            'location': forms.TextInput(attrs={'placeholder': 'Dirección o referencia'}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Descripción'}),
        }


class BlockForm(forms.ModelForm):
    garden = campo_jardin(required=True)

    class Meta:
        model = Block
        fields = ['garden', 'name', 'description', 'is_active']
        labels = {
            'name': 'Nombre',
            'description': 'Descripción',
            'is_active': 'Activo',
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Nombre del bloque'}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Descripción'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.garden_id:
            self.fields['garden'].queryset = incluir_actual(self.fields['garden'].queryset, self.instance.garden)


class BuildingForm(forms.ModelForm):
    # Filtro (no se guarda): reduce los bloques al jardín elegido.
    jardin = campo_jardin()
    block = campo_bloque(required=True)

    class Meta:
        model = Building
        fields = ['block', 'name', 'number_of_floors', 'description', 'is_active']
        labels = {
            'name': 'Nombre',
            'number_of_floors': 'Número de pisos',
            'description': 'Descripción',
            'is_active': 'Activo',
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Nombre del edificio o torre'}),
            'number_of_floors': forms.NumberInput(attrs={'placeholder': 'Pisos', 'min': 1}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Descripción'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        residencial = Residencial.obtener_unico()
        if residencial and residencial.cantidad_pisos:
            max_pisos = residencial.cantidad_pisos
            self.fields['number_of_floors'].widget.attrs['max'] = max_pisos
            self.max_pisos_config = max_pisos
        else:
            self.max_pisos_config = None
        if self.instance.block_id:
            self.fields['block'].queryset = incluir_actual(self.fields['block'].queryset, self.instance.block)
            self.initial.setdefault('jardin', self.instance.block.garden_id)

    def clean_number_of_floors(self):
        pisos = self.cleaned_data.get('number_of_floors')
        if pisos is None or pisos == '':
            return pisos
        max_pisos = getattr(self, 'max_pisos_config', None)
        if max_pisos is None:
            residencial = Residencial.obtener_unico()
            max_pisos = residencial.cantidad_pisos if residencial else None
        if max_pisos and pisos > max_pisos:
            raise forms.ValidationError(
                f'El número de pisos ({pisos}) supera el límite máximo configurado ({max_pisos} pisos).'
            )
        return pisos


class ApartmentsForm(forms.ModelForm):
    """Formulario de departamentos con ubicación en cascada (static/js/cascada.js).

    El propietario no se elige aquí: es el propietario quien elige sus
    departamentos desde su propio formulario.
    """
    jardin = campo_jardin()
    bloque = campo_bloque()
    building = campo_edificio(required=True)

    class Meta:
        model = Apartment
        fields = [
            'building', 'name', 'photo',
            'floor', 'status', 'is_active',
        ]
        labels = {
            'name': 'Apartamento',
            'photo': 'Imagen',
            'floor': 'Piso',
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'nombre del departamento'}),
            'floor': forms.NumberInput(attrs={'placeholder': 'Piso'}),
            # El estado (occupied/empty) se gestiona con un interruptor visual
            # que vuelca su valor a este campo oculto del formulario.
            'status': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        residencial = Residencial.obtener_unico()
        if residencial and residencial.cantidad_pisos:
            max_pisos = residencial.cantidad_pisos
            self.fields['floor'].widget.attrs['max'] = max_pisos
            self.max_pisos_config = max_pisos
        else:
            self.max_pisos_config = None
        if self.instance.building_id:
            edificio = self.instance.building
            self.fields['building'].queryset = incluir_actual(self.fields['building'].queryset, edificio)
            self.initial.setdefault('jardin', edificio.garden_id)
            self.initial.setdefault('bloque', edificio.block_id)

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

    def clean_floor(self):
        piso = self.cleaned_data.get('floor')
        if piso is None or piso == '':
            return piso
        max_pisos = getattr(self, 'max_pisos_config', None)
        if max_pisos is None:
            residencial = Residencial.obtener_unico()
            max_pisos = residencial.cantidad_pisos if residencial else None
        if max_pisos and piso > max_pisos:
            es_torres = False
            try:
                residencial = Residencial.obtener_unico()
                es_torres = bool(residencial and residencial.distribucion == 'torres')
            except Exception:
                es_torres = False
            tipo = 'torres' if es_torres else 'edificios'
            raise forms.ValidationError(
                f'El piso especificado supera el límite máximo configurado para las {tipo} ({max_pisos} pisos).'
            )
        return piso

    def clean_status(self):
        # Si el interruptor nunca se tocó, el campo oculto llega vacío;
        # por defecto el departamento se da de alta como desocupado.
        return self.cleaned_data.get('status') or 'empty'
