from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Communication
from condosys.forms_utils import placeholder

TIPOS_IMAGEN = ('.jpg', '.jpeg', '.png', '.webp')
MAX_IMAGEN_MB = 2


class CommunicationForm(forms.ModelForm):
    class Meta:
        model = Communication
        fields = [
            'title', 'category', 'body', 'image',
            'target_type', 'target_id', 'published_at', 'is_published',
        ]
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
            'target_id': forms.TextInput(attrs={
                'class': 'campo-entrada',
                'placeholder': 'ID del edificio o residente (opcional)',
            }),
            'published_at': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'campo-entrada',
                'placeholder': 'mm/dd/yyyy --:--',
            }, format='%Y-%m-%dT%H:%M'),
            'is_published': forms.CheckboxInput(attrs={'class': 'entrada-interruptor'}),
        }

        labels = {
            'title': 'Título',
            'category': 'Categoría',
            'body': 'Mensaje',
            'image': 'Adjuntar imagen',
            'target_type': 'Dirigido a',
            'target_id': 'ID de destino (opcional)',
            'published_at': 'Fecha de publicación',
            'is_published': 'Publicado',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Opciones "placeholder" al inicio de cada dropdown de opciones fijas.
        placeholder(self.fields['category'], 'Elegir categoría')
        placeholder(self.fields['target_type'], 'Elegir a quien va dirigido')
        # El comunicado nuevo viene publicado por defecto.
        if not self.instance.pk:
            self.fields['is_published'].initial = True

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
        fecha_publicacion = self.cleaned_data.get('published_at')
        if fecha_publicacion and timezone.is_naive(fecha_publicacion):
            fecha_publicacion = timezone.make_aware(fecha_publicacion)
        comunicado.published_at = fecha_publicacion
        if commit:
            comunicado.save()
        return comunicado
