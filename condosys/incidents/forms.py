from django import forms
from django.core.exceptions import ValidationError
from structure.models import Apartment
from residents.models import Resident
from .models import Incident, IncidentHistory, IncidentImage

TIPOS_EVIDENCIA = ('.jpg', '.jpeg', '.png', '.webp', '.pdf')
MAX_EVIDENCIA_MB = 2


class IncidentForm(forms.ModelForm):
    # Campo de "Seguimiento" (no existe en el modelo: se guarda como primer
    # registro de IncidentHistory al crear la incidencia).
    comment = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'campo-entrada texto-area',
            'rows': 4,
            'placeholder': 'Descripción',
        }),
        label='Comentarios/actualizaciones',
    )

    class Meta:
        model = Incident
        fields = [
            'apartment', 'resident', 'category', 'priority',
            'description', 'reported_date', 'evidence', 'status',
        ]
        widgets = {
            # data-incidencia-apartamento y data-incidencia-residente los usa
            # static/js/incidencias.js para filtrar residentes por apartamento.
            'apartment': forms.Select(attrs={
                'class': 'campo-seleccion',
                'data-incidencia-apartamento': '',
            }),
            'category': forms.Select(attrs={
                'class': 'campo-seleccion',
            }),
            'priority': forms.Select(attrs={
                'class': 'campo-seleccion',
            }),
            'description': forms.Textarea(attrs={
                'class': 'campo-entrada texto-area',
                'rows': 4,
                'placeholder': 'Descripción',
            }),
            'reported_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'campo-entrada',
            }),
            'evidence': forms.ClearableFileInput(attrs={
                'class': 'campo-entrada',
                'accept': 'image/jpeg,image/png,image/webp,application/pdf',
                'data-evidencia': '',
            }),
            'status': forms.Select(attrs={
                'class': 'campo-seleccion',
            }),
        }

        labels = {
            'apartment': 'Apartamento',
            'resident': 'Residente',
            'category': 'Tipo de incidencia',
            'priority': 'Prioridad',
            'description': 'Descripción',
            'reported_date': 'Fecha del reporte',
            'evidence': 'Adjuntar evidencia',
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
        # Opciones "placeholder" al inicio de cada dropdown de opciones fijas.
        self.fields['category'].choices = [('', 'Elegir tipo de incidencia')] + list(self.fields['category'].choices)
        self.fields['priority'].choices = [('', 'Elegir prioridad')] + list(self.fields['priority'].choices)
        self.fields['status'].choices = [('', 'Elegir estado')] + list(self.fields['status'].choices)
        # La fecha se rellena sola con la de hoy si el usuario no la cambia.
        self.fields['reported_date'].required = False

    def clean_evidence(self):
        archivo = self.cleaned_data.get('evidence')
        if not archivo:
            return archivo
        if archivo.size > MAX_EVIDENCIA_MB * 1024 * 1024:
            raise ValidationError(f'El archivo supera el límite de {MAX_EVIDENCIA_MB} MB.')
        extension = f'.{archivo.name.rsplit(".", 1)[-1].lower()}'
        if extension not in TIPOS_EVIDENCIA:
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


class IncidentImageForm(forms.ModelForm):
    class Meta:
        model = IncidentImage
        fields = ['incident', 'url']


class IncidentHistoryForm(forms.ModelForm):
    class Meta:
        model = IncidentHistory
        fields = ['incident', 'status_from', 'status_to', 'changed_by', 'comment']