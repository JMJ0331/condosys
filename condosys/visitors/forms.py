from django import forms
from .models import Visitor


class VisitorForm(forms.ModelForm):
    class Meta:
        model = Visitor
        fields = [
            'apartment', 'name', 'document', 'phone',
            'reason', 'type', 'vehicle_plate', 'scheduled_entry',
            'scheduled_exit', 'status', 'notes',
        ]
