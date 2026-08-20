from django import forms
from .models import Incident, IncidentHistory, IncidentImage


class IncidentForm(forms.ModelForm):
    class Meta:
        model = Incident
        fields = [
            'apartment', 'reported_by', 'assigned_to', 'category',
            'priority', 'title', 'description', 'status', 'resolution_notes',
        ]


class IncidentImageForm(forms.ModelForm):
    class Meta:
        model = IncidentImage
        fields = ['incident', 'url']


class IncidentHistoryForm(forms.ModelForm):
    class Meta:
        model = IncidentHistory
        fields = ['incident', 'status_from', 'status_to', 'changed_by', 'comment']
