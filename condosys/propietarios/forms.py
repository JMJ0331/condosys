from django import forms
from django.core.exceptions import ValidationError
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from PIL import Image
from .models import Propietario

ALLOWED_FORMATS = ('JPEG', 'PNG', 'WEBP')
MAX_SIZE_MB = 2


class FotoPreviewWidget(forms.ClearableFileInput):
    """Widget para foto con previsualización de la imagen actual."""
    template_name = 'propietarios/widgets/foto_preview.html'

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        if value and hasattr(value, 'url'):
            context['widget']['preview_url'] = value.url
        return context


def validate_photo(image):
    """Valida que el archivo sea una imagen JPG/PNG/WEBP de máximo 2 MB."""
    if image is None:
        return
    if image.size > MAX_SIZE_MB * 1024 * 1024:
        raise ValidationError(f"La imagen no puede superar {MAX_SIZE_MB} MB.")
    try:
        img = Image.open(image)
        img.verify()
        fmt = (img.format or '').upper()
    except Exception:
        raise ValidationError("El archivo no es una imagen válida.")
    if fmt not in ALLOWED_FORMATS:
        raise ValidationError("Solo se permiten imágenes JPG, PNG o WEBP.")


class PropietarioForm(forms.ModelForm):
    """Formulario de alta/edición de propietarios; usa estilos y clases compartidos."""
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

    photo = forms.ImageField(
        required=False,
        label='Foto de perfil',
        validators=[validate_photo],
        widget=FotoPreviewWidget(attrs={
            'accept': 'image/jpeg,image/png,image/webp',
            'data-propietario': 'foto',
        }),
    )
