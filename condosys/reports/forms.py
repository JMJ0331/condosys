from django import forms
from .models import AuditLog, AuditLogDetail


class AuditLogForm(forms.ModelForm):
    class Meta:
        model = AuditLog
        fields = ['user', 'action', 'entity', 'entity_id']


class AuditLogDetailForm(forms.ModelForm):
    class Meta:
        model = AuditLogDetail
        fields = ['audit_log', 'key', 'value']
