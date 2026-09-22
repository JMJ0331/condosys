from django import forms
from django.core.exceptions import ValidationError
from .models import Communication
from condosys.forms_utils import placeholder

TIPOS_IMAGEN = ('.jpg', '.jpeg', '.png', '.webp')
MAX_IMAGEN_MB = 2

ESTADO_CHOICES = (
    ('', 'Elegir estado'),
    ('published', 'Publicado'),
    ('draft', 'Borrador'),
)


class CommunicationForm(forms.ModelForm):
    publication_date = forms.DateTimeField(
        label='Fecha de publicación',
        required=False,
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'campo-entrada',
            'placeholder': 'mm/dd/yyyy --:--',
        }, format='%Y-%m-%dT%H:%M'),
    )
    estado = forms.ChoiceField(
        label='Estado',
        choices=ESTADO_CHOICES,
        widget=forms.Select(attrs={'class': 'campo-seleccion'}),
    )

    class Meta:
        model = Communication
        fields = ['title', 'category', 'body', 'image', 'target_type']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'campo-entrada',
                'placeholder': 'Ejemplo: Mantenimiento a las piscinas centrales',
            }),
            'category': forms.Select(attrs={'class': 'campo-seleccion'}),
            'body': forms.Textarea(attrs={
                'class': 'campo-entrada campo-textarea',
                'rows': 5,
                'placeholder': 'Detallar Mensaje',
                'maxlength': '400',
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'campo-entrada',
                'accept': 'image/jpeg,image/png,image/webp',
                'data-imagen-comunicado': '',
            }),
            'target_type': forms.Select(attrs={'class': 'campo-seleccion'}),
        }

        labels = {
            'title': 'Título',
            'category': 'Categoría',
            'body': 'Mensaje',
            'image': 'Adjuntar imagen',
            'target_type': 'Dirigido a',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Opciones "placeholder" al inicio de cada dropdown de opciones fijas.
        placeholder(self.fields['category'], 'Elegir categoría')
        placeholder(self.fields['target_type'], 'Elegir a quien va dirigido')

    def clean_body(self):
        mensaje = self.cleaned_data.get('body') or ''
        if len(mensaje) > 400:
            raise ValidationError('El mensaje no puede superar los 400 caracteres.')
        return mensaje

    def clean_image(self):
        archivo = self.cleaned_data.get('image')
        if not archivo:
            return archivo
        if archivo.size > MAX_IMAGEN_MB * 1024 * 1024:
            raise ValidationError(f'El archivo supera el límite de {MAX_IMAGEN_MB} MB.')
        extension = f'.{archivo.name.rsplit(".", 1)[-1].lower()}'
        if extension not in TIPOS_IMAGEN:
            raise ValidationError('Formato no permitido. Usa JPG, PNG o WEBP.')
        return archivo

    def save(self, commit=True):
        comunicado = super().save(commit=False)
        comunicado.is_published = self.cleaned_data['estado'] == 'published'
        fecha_publicacion = self.cleaned_data.get('publication_date')
        if fecha_publicacion:
            from django.utils import timezone
            if timezone.is_naive(fecha_publicacion):
                fecha_publicacion = timezone.make_aware(fecha_publicacion)
        comunicado.published_at = fecha_publicacion
        if commit:
            comunicado.save()
        return comunicado