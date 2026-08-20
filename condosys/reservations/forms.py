from django import forms
from .models import CommonArea, Reservation


class CommonAreaForm(forms.ModelForm):
    class Meta:
        model = CommonArea
        fields = ['garden', 'name', 'description', 'capacity', 'is_active']


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = [
            'common_area', 'reserved_by', 'start_time', 'end_time',
            'reason', 'expected_guests', 'status', 'approved_by', 'notes',
        ]
