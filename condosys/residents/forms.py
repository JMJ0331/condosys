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
            'apartment', 'is_active'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Nombre completo'}),
            'cedula': forms.TextInput(attrs={'placeholder': 'Cédula'}),
            'phone': forms.TextInput(attrs={'placeholder': '000-000-0000'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Correo electrónico'}),
            'emergency_contact': forms.TextInput(attrs={'placeholder': '000-000-0000'}),
            # Clases 'campo-seleccion' y 'entrada-interruptor' vienen de static/css/formularios.css.
            'apartment': forms.Select(attrs={'class': 'campo-seleccion'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'entrada-interruptor'}),
        }

    photo = forms.ImageField(
        required=False,
        label='Foto de perfil',
        validators=[validate_photo],
        widget=forms.ClearableFileInput(attrs={'accept': 'image/jpeg,image/png,image/webp'}),
    )