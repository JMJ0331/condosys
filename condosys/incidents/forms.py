from django import forms
from django.core.exceptions import ValidationError
from accounts.permissions import ROLES_GESTION
from structure.models import Apartment
from residents.models import Resident
from .models import Incident, IncidentHistory, IncidentImage
from condosys.forms_utils import placeholder

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
            'maxlength': '400',
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
                'maxlength': '400',
            }),
            'reported_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'campo-entrada',
            }, format='%Y-%m-%d'),
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
            'apartment': 'Departamento',
            'resident': 'Residente',
            'category': 'Tipo de incidencia',
            'priority': 'Prioridad',
            'description': 'Descripción',
            'reported_date': 'Fecha del reporte',
            'evidence': 'Adjuntar evidencia',
            'status': 'Estado',
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        # Residentes y propietarios no deciden el estado: lo gestiona admin/manager.
        if user is None or getattr(user, 'role', None) not in ROLES_GESTION:
            self.fields.pop('status', None)
        # Solo departamentos activos y con su edificio para el selector.
        self.fields['apartment'].queryset = (
            Apartment.objects.filter(is_active=True).select_related('building')
        )
        self.fields['apartment'].empty_label = 'Elegir departamento'
        # select_related evita consultas extra al mostrar el apartamento de cada residente.
        self.fields['resident'].queryset = Resident.objects.select_related('apartment').all()
        # Opciones "placeholder" al inicio de cada dropdown de opciones fijas.
        placeholder(self.fields['category'], 'Elegir tipo de incidencia')
        placeholder(self.fields['priority'], 'Elegir prioridad')
        if 'status' in self.fields:
            placeholder(self.fields['status'], 'Elegir estado')
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

    def clean_comment(self):
        comentario = self.cleaned_data.get('comment') or ''
        if len(comentario) > 400:
            raise ValidationError('El comentario no puede superar los 400 caracteres.')
        return comentario

    def clean_description(self):
        descripcion = self.cleaned_data.get('description') or ''
        if len(descripcion) > 400:
            raise ValidationError('La descripción no puede superar los 400 caracteres.')
        return descripcion

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