from django import forms
from .models import Communication


class CommunicationForm(forms.ModelForm):
    class Meta:
        model = Communication
        fields = [
            'garden', 'sender', 'title', 'body', 'target_type',
            'target_id', 'is_published', 'published_at',
        ]
