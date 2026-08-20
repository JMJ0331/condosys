from django import forms
from .models import MaintenanceOrder


class MaintenanceOrderForm(forms.ModelForm):
    class Meta:
        model = MaintenanceOrder
        fields = [
            'incident', 'apartment', 'assigned_to', 'type', 'description',
            'status', 'scheduled_date', 'completion_date', 'estimated_cost',
            'actual_cost', 'notes',
        ]
