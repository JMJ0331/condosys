from django import forms
from .models import Payment
from residents.models import Resident


class PaymentForm(forms.ModelForm):
    # No es campo del modelo: solo filtra el desplegable de residentes
    # (propietarios frente a inquilinos/familiares/ocupantes).
    quien_paga = forms.ChoiceField(
        label='Quien paga',
        required=False,
        choices=[
            ('', 'Elegir'),
            ('propietario', 'Un propietario'),
            ('residente', 'Un residente'),
        ],
        widget=forms.Select(attrs={
            'class': 'campo-seleccion',
            'data-pago-quien': '',
        }),
    )

    class Meta:
        model = Payment
        fields = [
            'apartment', 'quien_paga', 'resident', 'amount', 'concept',
            'period', 'payment_date', 'payment_method',
            'receipt_image', 'status',
        ]
        labels = {
            'apartment': 'Departamento',
            'resident': 'Propietarios/Residentes',
            'amount': 'Monto',
            'concept': 'Concepto',
            'period': 'Período/Mes correspondiente',
            'payment_date': 'Fecha del pago',
            'payment_method': 'Método de pago',
            'receipt_image': 'Foto del comprobante',
            'status': 'Estado',
        }
        widgets = {
            # data-pago-apartamento y data-pago-residente son referencias que usa
            # static/js/pagos.js para filtrar los residentes según el apartamento elegido.
            'apartment': forms.Select(attrs={
                'class': 'campo-seleccion',
                'data-pago-apartamento': '',
                'placeholder': 'Elegir apartamento',
            }),
            'resident': forms.Select(attrs={
                'class': 'campo-seleccion',
                'data-pago-residente': '',
                'placeholder': 'Elegir un propietario/residente',
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'campo-entrada',
                'placeholder': 'Ejemplo: $15.000',
                'step': '0.01',
                'min': '0',
            }),
            'concept': forms.Select(attrs={'class': 'campo-seleccion', 'placeholder': 'Elegir concepto'}),
            'period': forms.DateInput(attrs={'type': 'date', 'class': 'campo-entrada'}),
            'payment_date': forms.DateInput(attrs={'type': 'date', 'class': 'campo-entrada'}),
            'payment_method': forms.Select(attrs={'class': 'campo-seleccion', 'placeholder': 'Elegir método de pago'}),
            'receipt_image': forms.ClearableFileInput(attrs={
                'class': 'campo-entrada',
                'accept': 'image/jpeg,image/png,image/webp',
                'data-pago-foto': '',
            }),
            'status': forms.Select(attrs={'class': 'campo-seleccion', 'placeholder': 'Elegir estado'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # select_related evita consultas extra al mostrar el apartamento de cada residente.
        self.fields['resident'].queryset = Resident.objects.select_related('apartment').all()
        # Textos vacíos iguales a la maqueta (Elegir ...).
        self.fields['apartment'].empty_label = 'Elegir departamento'
        self.fields['resident'].empty_label = 'Elegir un propietario/residente'
        self.fields['concept'].choices = [('', 'Elegir concepto')] + list(Payment.CONCEPT_CHOICES)
        self.fields['payment_method'].choices = [('', 'Elegir método de pago')] + list(Payment.PAYMENT_METHOD_CHOICES)
        self.fields['status'].choices = [('', 'Elegir estado')] + list(Payment.STATUS_CHOICES)
        # La maqueta muestra "Elegir estado" como punto de partida.
        self.fields['status'].initial = ''

    def clean(self):
        cleaned_data = super().clean()
        apartment = cleaned_data.get('apartment')
        resident = cleaned_data.get('resident')
        quien_paga = cleaned_data.get('quien_paga')
        # Consistencia cliente/servidor: aunque el JS ya filtra, se valida
        # que el residente pertenezca realmente al apartamento seleccionado.
        if apartment and resident and resident.apartment_id != apartment.id:
            self.add_error('resident', 'El residente no pertenece al departamento seleccionado.')
        # Coherencia con el filtro "Quien paga".
        if resident and quien_paga == 'propietario' and resident.tipo_relacion != 'propietario':
            self.add_error('resident', 'Quien paga es propietario pero el elegido no lo es.')
        if resident and quien_paga == 'residente' and resident.tipo_relacion == 'propietario':
            self.add_error('resident', 'Quien paga es residente pero el elegido es propietario.')
        return cleaned_data