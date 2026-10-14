from django import forms
from accounts.forms import CuentaUsuarioFormBase
from residents.forms import validate_photo
from structure.campos import campo_bloque, campo_edificio, campo_jardin
from structure.models import Apartment
from structure.widgets import CasillasCascada
from .models import Propietario


class FotoPreviewWidget(forms.ClearableFileInput):
    """Widget para foto con previsualización de la imagen actual."""
    template_name = 'propietarios/widgets/foto_preview.html'

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        if value and hasattr(value, 'url'):
            context['widget']['preview_url'] = value.url
        return context


class PropietarioForm(CuentaUsuarioFormBase):
    """Formulario de alta/edición de propietarios; usa estilos y clases compartidos.
    Crea y vincula la cuenta de acceso (User, rol 'propietario') con la
    contraseña digitada por el admin."""
    rol_cuenta = 'propietario'

    class Meta:
        model = Propietario
        fields = [
            'full_name', 'marital_status', 'cedula', 'photo',
            'phone', 'email', 'emergency_contact',
            'is_active'
        ]
        labels = {
            'full_name': 'Nombre completo',
            'marital_status': 'Estado civil',
            'cedula': 'Cedula',
            'phone': 'Teléfono',
            'email': 'Correo electrónico',
            'emergency_contact': 'Contacto de emergencia (opcional)',
            'is_active': 'Activo',
        }
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Nombre completo'}),
            'marital_status': forms.Select(attrs={'class': 'campo-seleccion'}),
            'cedula': forms.TextInput(attrs={'placeholder': '000-0000000-0', 'maxlength': '13', 'data-mascara': 'cedula'}),
            'phone': forms.TextInput(attrs={'placeholder': '(000)-000-0000', 'maxlength': '14', 'data-mascara': 'telefono'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Correo electrónico'}),
            'emergency_contact': forms.TextInput(attrs={'placeholder': '(000)-000-0000', 'maxlength': '14', 'data-mascara': 'telefono'}),
            # Clase 'entrada-interruptor' viene de static/css/formularios.css.
            'is_active': forms.CheckboxInput(attrs={'class': 'entrada-interruptor'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Texto guía ("Elegir...") como primera opción del selector.
        self.fields['marital_status'].choices = (
            [('', 'Elegir estado civil')] + list(self.fields['marital_status'].choices)
        )
        if not self.instance.pk:
            # Formulario de alta: mostrar el "Elegir..." en vez del valor por defecto.
            self.fields['marital_status'].initial = ''

        # Departamentos libres (sin propietario) más los que ya son suyos.
        libres = Apartment.objects.filter(is_active=True, owner__isnull=True)
        if not self.instance._state.adding:
            propios = Apartment.objects.filter(owner=self.instance)
            self.fields['departamentos'].queryset = (libres | propios).distinct().select_related(
                'building__garden', 'building__block', 'owner'
            ).order_by('building__garden__name', 'building__block__name', 'building__name', 'name')
            self.initial.setdefault('departamentos', list(propios.values_list('pk', flat=True)))

    # Filtros en cascada (no se guardan): reducen la lista de departamentos.
    jardin = campo_jardin()
    bloque = campo_bloque()
    edificio = campo_edificio()
    departamentos = forms.ModelMultipleChoiceField(
        queryset=Apartment.objects.filter(is_active=True, owner__isnull=True).select_related(
            'building__garden', 'building__block', 'owner'
        ).order_by('building__garden__name', 'building__block__name', 'building__name', 'name'),
        label='Departamentos',
        widget=CasillasCascada('departamento'),
        error_messages={'required': 'Elige al menos un departamento del propietario.'},
    )

    def _propios_actuales(self):
        if self.instance._state.adding:
            return Apartment.objects.none()
        return Apartment.objects.filter(owner=self.instance)

    def clean_departamentos(self):
        elegidos = self.cleaned_data['departamentos']
        quitados = self._propios_actuales().exclude(pk__in=[d.pk for d in elegidos])
        con_residentes = quitados.filter(residents__is_active=True).distinct()
        if con_residentes.exists():
            nombres = ', '.join(str(d) for d in con_residentes.select_related('building'))
            raise forms.ValidationError(
                f'No puedes quitar departamentos con residentes activos: {nombres}.'
            )
        return elegidos

    def _save_m2m(self):
        super()._save_m2m()
        elegidos = [d.pk for d in self.cleaned_data['departamentos']]
        self._propios_actuales().exclude(pk__in=elegidos).update(owner=None)
        Apartment.objects.filter(pk__in=elegidos).update(owner=self.instance)

    photo = forms.ImageField(
        required=False,
        label='Foto de perfil',
        validators=[validate_photo],
        widget=FotoPreviewWidget(attrs={
            'accept': 'image/jpeg,image/png,image/webp',
            'data-propietario': 'foto',
        }),
    )
