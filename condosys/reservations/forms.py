from django import forms
from django.utils import timezone
from datetime import datetime
from accounts.models import User
from structure.models import Apartment
from residents.models import Resident
from .models import CommonArea, Reservation


class CommonAreaForm(forms.ModelForm):
    class Meta:
        model = CommonArea
        fields = ['garden', 'name', 'description', 'capacity', 'is_active']


class ReservationForm(forms.ModelForm):
    # Fecha y horas por separado (el modelo guarda start_time/end_time).
    fecha_reserva = forms.DateField(
        label='Fecha de reserva',
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'campo-entrada',
            'placeholder': 'mm/dd/yyyy',
        }),
    )
    hora_inicio = forms.TimeField(
        label='Hora de inicio',
        widget=forms.TimeInput(attrs={
            'type': 'time',
            'class': 'campo-entrada',
            'placeholder': '--:-- --',
        }, format='%H:%M'),
    )
    hora_fin = forms.TimeField(
        label='Hora de fin',
        widget=forms.TimeInput(attrs={
            'type': 'time',
            'class': 'campo-entrada',
            'placeholder': '--:-- --',
        }, format='%H:%M'),
    )

    class Meta:
        model = Reservation
        fields = [
            'common_area', 'apartment', 'resident', 'reserved_by', 'status',
        ]
        widgets = {
            # data-reserva-apartamento lo usa static/js/reservas.js para
            # filtrar los propietarios/residentes por apartamento.
            'common_area': forms.Select(attrs={'class': 'campo-seleccion'}),
            'apartment': forms.Select(attrs={
                'class': 'campo-seleccion',
                'data-reserva-apartamento': '',
            }),
            'reserved_by': forms.Select(attrs={'class': 'campo-seleccion'}),
            'status': forms.Select(attrs={'class': 'campo-seleccion'}),
        }

        labels = {
            'common_area': 'Área común',
            'apartment': 'Apartamento',
            'resident': 'Propietario/Residente',
            'reserved_by': 'Quien reserva',
            'status': 'Estado',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Solo áreas y apartamentos activos para reservar.
        self.fields['common_area'].queryset = (
            CommonArea.objects.filter(is_active=True).select_related('garden')
        )
        self.fields['common_area'].empty_label = 'Elegir área común'
        self.fields['apartment'].queryset = (
            Apartment.objects.filter(is_active=True).select_related('building')
        )
        self.fields['apartment'].empty_label = 'Elegir apartamento'
        self.fields['reserved_by'].queryset = User.objects.filter(is_active=True)
        self.fields['reserved_by'].empty_label = 'Elegir quien reserva'
        # select_related evita consultas extra al mostrar el apartamento de cada residente.
        self.fields['resident'].queryset = Resident.objects.select_related('apartment').all()
        # Opciones "placeholder" al inicio de cada dropdown de opciones fijas.
        self.fields['status'].choices = [('', 'Elegir estado')] + list(self.fields['status'].choices)

    def clean(self):
        cleaned_data = super().clean()
        apartment = cleaned_data.get('apartment')
        resident = cleaned_data.get('resident')
        # Consistencia cliente/servidor: aunque el JS filtra, se valida que el
        # propietario/residente pertenezca realmente al apartamento elegido.
        if apartment and resident and resident.apartment_id != apartment.id:
            self.add_error('resident', 'El propietario/residente no pertenece al apartamento seleccionado.')

        fecha = cleaned_data.get('fecha_reserva')
        hora_inicio = cleaned_data.get('hora_inicio')
        hora_fin = cleaned_data.get('hora_fin')
        if fecha and hora_inicio and hora_fin:
            inicio = timezone.make_aware(datetime.combine(fecha, hora_inicio))
            fin = timezone.make_aware(datetime.combine(fecha, hora_fin))
            if fin <= inicio:
                self.add_error('hora_fin', 'La hora de fin debe ser posterior a la hora de inicio.')
            cleaned_data['start_time'] = inicio
            cleaned_data['end_time'] = fin
        return cleaned_data

    def save(self, commit=True):
        reserva = super().save(commit=False)
        reserva.start_time = self.cleaned_data['start_time']
        reserva.end_time = self.cleaned_data['end_time']
        if commit:
            reserva.save()
        return reserva