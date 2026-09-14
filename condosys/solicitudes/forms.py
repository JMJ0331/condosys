from django import forms
from django.core.exceptions import ValidationError
from structure.models import Apartment
from residents.models import Resident
from .models import Solicitud
from condosys.forms_utils import placeholder

TIPOS_DOCUMENTO = ('.jpg', '.jpeg', '.png', '.webp', '.pdf')
MAX_DOCUMENTO_MB = 2


class SolicitudForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = [
            'apartment', 'resident', 'request_type',
            'description', 'request_date', 'attachment',
            'tracking_response', 'status',
        ]
        widgets = {
            # data-solicitud-apartamento y data-solicitud-residente los usa
            # static/js/solicitudes.js para filtrar residentes por apartamento.
            'apartment': forms.Select(attrs={
                'class': 'campo-seleccion',
                'data-solicitud-apartamento': '',
            }),
            'request_type': forms.Select(attrs={
                'class': 'campo-seleccion',
            }),
            'description': forms.Textarea(attrs={
                'class': 'campo-entrada texto-area',
                'rows': 4,
                'placeholder': 'Descripción',
            }),
            'request_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'campo-entrada',
                'placeholder': 'mm/dd/yyyy',
            }),
            'attachment': forms.ClearableFileInput(attrs={
                'class': 'campo-entrada',
                'accept': 'image/jpeg,image/png,image/webp,application/pdf',
                'data-solicitud-documento': '',
            }),
            'tracking_response': forms.Textarea(attrs={
                'class': 'campo-entrada texto-area',
                'rows': 4,
                'placeholder': 'Descripción',
            }),
            'status': forms.Select(attrs={
                'class': 'campo-seleccion',
            }),
        }

        labels = {
            'apartment': 'Apartamento',
            'resident': 'Residente',
            'request_type': 'Tipo de solicitud',
            'description': 'Descripción',
            'request_date': 'Fecha de solicitud',
            'attachment': 'Adjuntar documento',
            'tracking_response': 'Comentarios/respuesta',
            'status': 'Estado',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Solo departamentos activos y con su edificio para el selector.
        self.fields['apartment'].queryset = (
            Apartment.objects.filter(is_active=True).select_related('building')
        )
        self.fields['apartment'].empty_label = 'Elegir apartamento'
        # select_related evita consultas extra al mostrar el apartamento de cada residente.
        self.fields['resident'].queryset = Resident.objects.select_related('apartment').all()
        self.fields['resident'].empty_label = 'Elegir residente'
        # Opciones "placeholder" al inicio de cada dropdown de opciones fijas.
        placeholder(self.fields['request_type'], 'Elegir tipo de solicitud')
        placeholder(self.fields['status'], 'Elegir estado')
        # La fecha se rellena sola con la de hoy si el usuario no la cambia.
        self.fields['request_date'].required = False

    def clean_attachment(self):
        archivo = self.cleaned_data.get('attachment')
        if not archivo:
            return archivo
        if archivo.size > MAX_DOCUMENTO_MB * 1024 * 1024:
            raise ValidationError(f'El archivo supera el límite de {MAX_DOCUMENTO_MB} MB.')
        extension = f'.{archivo.name.rsplit(".", 1)[-1].lower()}'
        if extension not in TIPOS_DOCUMENTO:
            raise ValidationError('Formato no permitido. Usa JPG, PNG, WEBP o PDF.')
        return archivo

    def clean(self):
        cleaned_data = super().clean()
        apartment = cleaned_data.get('apartment')
        resident = cleaned_data.get('resident')
        # Consistencia cliente/servidor: aunque el JS filtra, se valida que el
        # residente pertenezca realmente al apartamento seleccionado.
        if apartment and resident and resident.apartment_id != apartment.id:
            self.add_error('resident', 'El residente no pertenece al apartamento seleccionado.')
        return cleaned_data