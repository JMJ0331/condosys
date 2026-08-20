from django import forms
from .models import Visitor


class VisitorForm(forms.ModelForm):
    class Meta:
        model = Visitor
        fields = [
            'apartment', 'registered_by', 'name', 'document', 'phone',
            'reason', 'type', 'vehicle_plate', 'scheduled_entry',
            'scheduled_exit', 'actual_entry', 'actual_exit', 'status',
            'authorized_by', 'notes',
        ]
