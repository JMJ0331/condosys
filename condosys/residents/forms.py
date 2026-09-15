from django import forms
from django.core.exceptions import ValidationError
from PIL import Image
from .models import Resident

# Restricciones de imagen compartidas por todos los formularios que suben fotos.
ALLOWED_FORMATS = ('JPEG', 'PNG', 'WEBP')
MAX_SIZE_MB = 2


def validate_photo(image):
    """Valida que el archivo sea una imagen JPG/PNG/WEBP de máximo 2 MB."""
    if image is None:
        return
    if image.size > MAX_SIZE_MB * 1024 * 1024:
        raise ValidationError(f"La imagen no puede superar {MAX_SIZE_MB} MB.")
    try:
        # verify() abre y comprueba la integridad del archivo sin dejarlo en memoria.
        img = Image.open(image)
        img.verify()
        fmt = (img.format or '').upper()
    except Exception:
        raise ValidationError("El archivo no es una imagen válida.")
    if fmt not in ALLOWED_FORMATS:
        raise ValidationError("Solo se permiten imágenes JPG, PNG o WEBP.")


class ResidentForm(forms.ModelForm):
    """Formulario de alta/edición de residentes; usa estilos y clases compartidos."""
    class Meta:
        model = Resident
        fields = [
            'full_name', 'marital_status', 'cedula', 'photo',
            'phone', 'email', 'emergency_contact',
            'apartment', 'tipo_relacion', 'fecha_ingreso', 'mascotas',
            'is_active'
        ]
        labels = {
            'full_name': 'Nombre completo',
            'marital_status': 'Estado civil',
            'cedula': 'Cedula',
            'phone': 'Teléfono',
            'email': 'Correo electrónico',
            'emergency_contact': 'Contacto de emergencia (opcional)',
            'apartment': 'Departamento',
            'tipo_relacion': 'Tipo de relación',
            'fecha_ingreso': 'Fecha de ingreso',
            'mascotas': 'Mascotas',
            'is_active': 'Activo',
        }
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Nombre completo'}),
            'marital_status': forms.Select(attrs={'class': 'campo-seleccion'}),
            'cedula': forms.TextInput(attrs={'placeholder': '000-0000000-0', 'maxlength': '13', 'data-mascara': 'cedula'}),
            'phone': forms.TextInput(attrs={'placeholder': '(000)-000-0000', 'maxlength': '14', 'data-mascara': 'telefono'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Correo electrónico'}),
            'emergency_contact': forms.TextInput(attrs={'placeholder': '(000)-000-0000', 'maxlength': '14', 'data-mascara': 'telefono'}),
            # Clases 'campo-seleccion' y 'entrada-interruptor' vienen de static/css/formularios.css.
            'apartment': forms.Select(attrs={'class': 'campo-seleccion'}),
            'tipo_relacion': forms.Select(attrs={'class': 'campo-seleccion'}),
            'fecha_ingreso': forms.DateInput(attrs={'type': 'date', 'class': 'campo-entrada'}),
            'mascotas': forms.Select(attrs={'class': 'campo-seleccion'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'entrada-interruptor'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Textos guía ("Elegir...") como primera opción de cada selector.
        self.fields['marital_status'].choices = (
            [('', 'Elegir estado civil')] + list(self.fields['marital_status'].choices)
        )
        self.fields['tipo_relacion'].choices = (
            [('', 'Elegir tipo de relación')] + list(self.fields['tipo_relacion'].choices)
        )
        self.fields['mascotas'].choices = (
            [('', 'Elegir')] + list(self.fields['mascotas'].choices)
        )
        self.fields['apartment'].empty_label = 'Elegir departamento'
        if not self.instance.pk:
            # Formulario de alta: mostrar los "Elegir..." en vez de los valores por defecto.
            self.fields['marital_status'].initial = ''
            self.fields['tipo_relacion'].initial = ''

    photo = forms.ImageField(
        required=False,
        label='Foto de perfil',
        validators=[validate_photo],
        widget=forms.ClearableFileInput(attrs={
            'accept': 'image/jpeg,image/png,image/webp',
            'data-residente': 'foto',
        }),
    )