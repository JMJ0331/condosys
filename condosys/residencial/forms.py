from django import forms

from .models import DISTRIBUCION_CHOICES, MUNICIPIOS_POR_PROVINCIA, PROVINCIAS_RD, Residencial


def _municipio_choices(provincia_actual=''):
    """Opciones del select de municipio según la provincia elegida."""
    opciones = [('', 'Elegir municipio/ciudad')]
    if provincia_actual in MUNICIPIOS_POR_PROVINCIA:
        for municipio in MUNICIPIOS_POR_PROVINCIA[provincia_actual]:
            opciones.append((municipio, municipio))
    elif provincia_actual:
        opciones.append((provincia_actual, provincia_actual))
    return opciones


class ResidencialForm(forms.ModelForm):
    """Formulario del residencial con selects enlazados a static/js/residencial.js."""

    class Meta:
        model = Residencial
        fields = [
            'nombre', 'rnc',
            'nombre_via', 'numero_edificacion', 'sector', 'codigo_postal',
            'municipio', 'provincia', 'mapa_iframe',
            'distribucion', 'cantidad_edificios', 'cantidad_pisos',
            'telefono', 'correo',
        ]
        labels = {
            'nombre': 'Nombre del residencial',
            'rnc': 'RNC',
            'nombre_via': 'Nombre de la vía',
            'numero_edificacion': 'Número de la edificación',
            'sector': 'Sector',
            'codigo_postal': 'Código Postal',
            'municipio': 'Municipio/Ciudad',
            'provincia': 'Provincia',
            'mapa_iframe': 'Subir iframe de Google Map',
            'distribucion': 'Distribución',
            'cantidad_edificios': 'Cantidad de edificios/torres',
            'cantidad_pisos': 'Cantidad de pisos por edificio/torre',
            'telefono': 'Teléfono de administración',
            'correo': 'Correo de administración',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre del residencial'}),
            'rnc': forms.TextInput(attrs={
                'placeholder': '000-00000-0',
                'data-mascara': 'rnc',
                'inputmode': 'numeric',
                'maxlength': '11',
            }),
            'nombre_via': forms.TextInput(attrs={'placeholder': 'Ej. Calle Central'}),
            'numero_edificacion': forms.TextInput(attrs={'placeholder': 'Ej. No. 15'}),
            'sector': forms.TextInput(attrs={'placeholder': 'Ej. Bella Vista'}),
            'codigo_postal': forms.TextInput(attrs={'placeholder': 'Ej. 10112'}),
            # data-residencial="provincia|municipio|mapa": el JS filtra
            # municipios por provincia y muestra la vista previa del mapa.
            'municipio': forms.Select(attrs={'class': 'campo-seleccion', 'data-residencial': 'municipio'}),
            'provincia': forms.Select(attrs={'class': 'campo-seleccion', 'data-residencial': 'provincia'}),
            'mapa_iframe': forms.Textarea(attrs={
                'placeholder': 'Pega aquí el <iframe> de Google Maps…',
                'rows': 4,
                'data-residencial': 'mapa',
            }),
            'distribucion': forms.Select(attrs={'class': 'campo-seleccion', 'data-residencial': 'distribucion'}),
            'cantidad_edificios': forms.NumberInput(attrs={'placeholder': 'Ej. 12', 'min': 0}),
            'cantidad_pisos': forms.NumberInput(attrs={'placeholder': 'Ej. 12', 'min': 0}),
            'telefono': forms.TextInput(attrs={
                'placeholder': '000-000-0000',
                'data-mascara': 'telefono-admin',
                'inputmode': 'numeric',
                'maxlength': '12',
            }),
            'correo': forms.EmailInput(attrs={'placeholder': 'Ej. residencial@gmail.com'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # La distribución solo se elige una vez: si ya hay valor guardado,
        # el select queda deshabilitado (los disabled conservan su valor).
        instancia = getattr(self, 'instance', None)
        if instancia is not None and instancia.pk and instancia.distribucion:
            self.fields['distribucion'].disabled = True
        # empty_label solo funciona en ModelChoiceField; en ChoiceField la
        # opción vacía se antepone a mano para respetar la maqueta.
        self.fields['provincia'].choices = [('', 'Elegir provincia')] + list(PROVINCIAS_RD)
        self.fields['distribucion'].choices = [('', 'Elegir distribución')] + list(DISTRIBUCION_CHOICES)
        provincia_actual = ''
        if self.is_bound:
            provincia_actual = self.data.get('provincia', '')
        elif self.instance and self.instance.pk:
            provincia_actual = self.instance.provincia or ''
        # El municipio acepta lo guardado aunque no esté en el catálogo.
        municipios = _municipio_choices(provincia_actual)
        guardado = (self.instance.municipio if self.instance and self.instance.pk else '') or ''
        if guardado and guardado not in dict(municipios):
            municipios.append((guardado, guardado))
        self.fields['municipio'].choices = municipios
