from django import forms
from .models import Resident


class ResidentForm(forms.ModelForm):
    class Meta:
        model = Resident
        fields = [
            'user', 'apartment', 'role_in_apartment', 'move_in_date',
            'move_out_date', 'emergency_contact', 'emergency_phone',
        ]
