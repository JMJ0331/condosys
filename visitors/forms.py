from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Prefetch, Q
from django.utils import timezone
from accounts.models import User
from structure.models import Apartment
from residents.models import Resident
from .models import Visitor
from condosys.forms_utils import placeholder

TIPOS_DOCUMENTO = ('.jpg', '.jpeg', '.png', '.webp')
MAX_DOCUMENTO_MB = 2


def usuarios_autorizadores(departamento):
    """Usuarios activos vinculados a un departamento que pueden autorizar la
    visita: su propietario (Apartment.owner -> Propietario.user) y los
    residentes registrados en él (Resident.user). Los registros dados de baja
    (Propietario/Resident con is_active=False) se descartan."""
    return User.objects.filter(
        Q(
            propietario_profiles__apartments_owned=departamento,
            propietario_profiles__is_active=True,
        )
        | Q(
            resident_profiles__apartment=departamento,
            resident_profiles__is_active=True,
        ),
        is_active=True,
    ).distinct()


class VisitorForm(forms.ModelForm):
    # Fecha de entrada y salida por separado (el modelo guarda
    # scheduled_entry/scheduled_exit).
    fecha_entrada = forms.DateTimeField(
        label='Fecha de entrada',
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'campo-entrada',
            'placeholder': 'mm/dd/yyyy --:--',
        }, format='%Y-%m-%dT%H:%M'),
    )
    fecha_salida = forms.DateTimeField(
        label='Fecha de salida',
        required=False,
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'campo-entrada',
            'placeholder': 'mm/dd/yyyy --:--',
        }, format='%Y-%m-%dT%H:%M'),
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
            'document_image': forms.FileInput(attrs={
                'accept': 'image/jpeg,image/png,image/webp',
                'data-documento-visitante': '',
                'tabindex': '-1',
            }),
            'apartment': forms.Select(attrs={
                'class': 'campo-seleccion',
                'data-visitante': 'departamento',
            }),
            'authorized_by': forms.Select(attrs={
                'class': 'campo-seleccion',
                'data-visitante': 'autorizado',
            }),
            'status': forms.Select(attrs={'class': 'campo-seleccion'}),
        }

        labels = {
            'name': 'Nombre completo',
            'type': 'Tipo de visitante',
            'document_type': 'Documento de identidad',
            'document_image': 'Foto del documento',
            'apartment': 'Departamento a visitar',
            'authorized_by': 'Autorizado por',
            'status': 'Estado',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # En actualizar se precargan las fechas desde scheduled_entry/exit
        # (no son campos del modelo editables directo).
        instancia = getattr(self, 'instance', None)
        if instancia is not None and instancia.pk and instancia.scheduled_entry:
            self.initial.setdefault(
                'fecha_entrada', instancia.scheduled_entry.strftime('%Y-%m-%dT%H:%M')
            )
            if instancia.scheduled_exit:
                self.initial.setdefault(
                    'fecha_salida', instancia.scheduled_exit.strftime('%Y-%m-%dT%H:%M')
                )
        # "Autorizado por" ya registrado: se conserva aunque la persona haya
        # dejado de estar vinculada al departamento, para no perder el dato.
        autorizado_actual = instancia.authorized_by if instancia is not None else None
        self.autorizado_actual = (
            autorizado_actual if autorizado_actual and autorizado_actual.is_active else None
        )
        # Solo apartamentos activos para registrar visitas. Propietario y
        # residentes llegan precargados para armar el filtro de "Autorizado por".
        self.fields['apartment'].queryset = (
            Apartment.objects.filter(is_active=True)
            .select_related('building__garden', 'owner__user')
            .prefetch_related(
                Prefetch(
                    'residents',
                    queryset=Resident.objects.filter(
                        is_active=True, user__isnull=False
                    ).select_related('user'),
                    to_attr='residentes_vinculados',
                )
            )
        )
        self.fields['apartment'].empty_label = 'Elegir departamento'
        # Solo entran al desplegable los usuarios vinculados a algún
        # departamento activo; de ellos, static/js/visitantes.js muestra el
        # subconjunto que corresponde al departamento elegido.
        vinculados = (
            Q(
                propietario_profiles__apartments_owned__is_active=True,
                propietario_profiles__is_active=True,
            )
            | Q(
                resident_profiles__apartment__is_active=True,
                resident_profiles__is_active=True,
            )
        )
        if self.autorizado_actual is not None:
            vinculados = vinculados | Q(pk=self.autorizado_actual.pk)
        self.fields['authorized_by'].queryset = (
            User.objects.filter(vinculados, is_active=True)
            .distinct()
            .order_by('first_name', 'last_name')
        )
        self.fields['authorized_by'].empty_label = 'Elegir quién autorizó'
        # Opciones de departamento con los ids de quienes pueden autorizarlas.
        self.opciones_departamento = self._opciones_departamento()
        # Opciones "placeholder" al inicio de cada dropdown de opciones fijas.
        placeholder(self.fields['type'], 'Elegir tipo de visitante')
        placeholder(self.fields['document_type'], 'Elegir tipo de documento')
        placeholder(self.fields['status'], 'Elegir estado')

    def _opciones_departamento(self):
        """Opciones del select de departamentos. Cada una lleva en
        `autorizados` los ids de los usuarios vinculados a ese departamento,
        que la plantilla vuelca en `data-autorizado-ids` para que el JS
        filtre el desplegable de "Autorizado por"."""
        instancia = getattr(self, 'instance', None)
        autorizado_actual = self.autorizado_actual

        vinculados = {}
        for departamento in self.fields['apartment'].queryset:
            ids = []
            propietario = departamento.owner
            if (
                departamento.owner_id
                and propietario.is_active
                and propietario.user_id
            ):
                ids.append(propietario.user_id)
            ids.extend(
                residente.user_id
                for residente in departamento.residentes_vinculados
                if residente.user_id
            )
            if (
                autorizado_actual is not None
                and instancia.pk
                and departamento.pk == instancia.apartment_id
            ):
                ids.append(autorizado_actual.pk)
            vinculados[departamento.pk] = list(dict.fromkeys(ids))

        activos = set(
            User.objects.filter(
                pk__in={i for ids in vinculados.values() for i in ids},
                is_active=True,
            ).values_list('pk', flat=True)
        )
        return [
            {
                'id': departamento.pk,
                'texto': str(departamento),
                'autorizados': ' '.join(
                    str(i) for i in vinculados[departamento.pk] if i in activos
                ),
            }
            for departamento in self.fields['apartment'].queryset
        ]

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
        self._validar_autorizado(cleaned_data)
        return cleaned_data

    def _validar_autorizado(self, cleaned_data):
        """El "Autorizado por" debe ser el propietario o un residente del
        departamento a visitar. El desplegable filtrado es solo ayuda visual:
        esta validación es la que realmente lo impide."""
        usuario = cleaned_data.get('authorized_by')
        departamento = cleaned_data.get('apartment')
        if not usuario or not departamento:
            return
        instancia = getattr(self, 'instance', None)
        ya_registrado = (
            instancia is not None
            and instancia.pk
            and instancia.apartment_id == departamento.pk
            and instancia.authorized_by_id == usuario.pk
        )
        if ya_registrado:
            return
        if not usuarios_autorizadores(departamento).filter(pk=usuario.pk).exists():
            self.add_error(
                'authorized_by',
                'La persona elegida no está vinculada al departamento a visitar.',
            )

    def save(self, commit=True):
        visitante = super().save(commit=False)
        visitante.scheduled_entry = self.cleaned_data['scheduled_entry']
        visitante.scheduled_exit = self.cleaned_data.get('scheduled_exit')
        if commit:
            visitante.save()
        return visitante