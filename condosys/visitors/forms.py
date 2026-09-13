from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from accounts.models import User
from structure.models import Apartment
from .models import Visitor

TIPOS_DOCUMENTO = ('.jpg', '.jpeg', '.png', '.webp')
MAX_DOCUMENTO_MB = 2


class VisitorForm(forms.ModelForm):
    # Fecha de entrada y salida por separado (el modelo guarda
    # scheduled_entry/scheduled_exit).
    fecha_entrada = forms.DateTimeField(
        label='Fecha de entrada',
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'campo-entrada',
            'placeholder': 'mm/dd/yyyy --:--',
        }),
    )
    fecha_salida = forms.DateTimeField(
        label='Fecha de salida',
        required=False,
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'campo-entrada',
            'placeholder': 'mm/dd/yyyy --:--',
        }),
    )

    class Meta:
        model = Visitor
        fields = [
            'name', 'type', 'document_type', 'document_image',
            'apartment', 'authorized_by', 'status',
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'campo-entrada',
                'placeholder': 'Ejemplo: Juan Pérez',
            }),
            'type': forms.Select(attrs={'class': 'campo-seleccion'}),
            'document_type': forms.Select(attrs={'class': 'campo-seleccion'}),
            'document_image': forms.ClearableFileInput(attrs={
                'class': 'campo-entrada',
                'accept': 'image/jpeg,image/png,image/webp',
                'data-documento-visitante': '',
            }),
            'apartment': forms.Select(attrs={'class': 'campo-seleccion'}),
            'authorized_by': forms.Select(attrs={'class': 'campo-seleccion'}),
            'status': forms.Select(attrs={'class': 'campo-seleccion'}),
        }

        labels = {
            'name': 'Nombre completo',
            'type': 'Tipo de visitante',
            'document_type': 'Documento de identidad',
            'document_image': 'Foto del documento',
            'apartment': 'Apartamento a visitar',
            'authorized_by': 'Autorizado por',
            'status': 'Estado',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Solo apartamentos activos para registrar visitas.
        self.fields['apartment'].queryset = (
            Apartment.objects.filter(is_active=True).select_related('building')
        )
        self.fields['apartment'].empty_label = 'Elegir apartamento'
        self.fields['authorized_by'].queryset = User.objects.filter(is_active=True)
        self.fields['authorized_by'].empty_label = 'Elegir quien autorizó'
        # Opciones "placeholder" al inicio de cada dropdown de opciones fijas.
        self.fields['type'].choices = [('', 'Elegir tipo de visitante')] + list(self.fields['type'].choices)
        self.fields['document_type'].choices = [('', 'Elegir tipo de documento')] + list(self.fields['document_type'].choices)
        self.fields['status'].choices = [('', 'Elegir estado')] + list(self.fields['status'].choices)

    def clean_document_image(self):
        archivo = self.cleaned_data.get('document_image')
        if not archivo:
            return archivo
        if archivo.size > MAX_DOCUMENTO_MB * 1024 * 1024:
            raise ValidationError(f'El archivo supera el límite de {MAX_DOCUMENTO_MB} MB.')
        extension = f'.{archivo.name.rsplit(".", 1)[-1].lower()}'
        if extension not in TIPOS_DOCUMENTO:
            raise ValidationError('Formato no permitido. Usa JPG, PNG o WEBP.')
        return archivo

    def clean(self):
        cleaned_data = super().clean()
        fecha_entrada = cleaned_data.get('fecha_entrada')
        fecha_salida = cleaned_data.get('fecha_salida')

        if fecha_entrada:
            if timezone.is_naive(fecha_entrada):
                fecha_entrada = timezone.make_aware(fecha_entrada)
            cleaned_data['scheduled_entry'] = fecha_entrada
        if fecha_salida:
            if timezone.is_naive(fecha_salida):
                fecha_salida = timezone.make_aware(fecha_salida)
            if fecha_entrada and fecha_salida <= fecha_entrada:
                self.add_error('fecha_salida', 'La fecha de salida debe ser posterior a la de entrada.')
            cleaned_data['scheduled_exit'] = fecha_salida
        return cleaned_data

    def save(self, commit=True):
        visitante = super().save(commit=False)
        visitante.scheduled_entry = self.cleaned_data['scheduled_entry']
        visitante.scheduled_exit = self.cleaned_data.get('scheduled_exit')
        if commit:
            visitante.save()
        return visitante