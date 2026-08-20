from django import forms
from .models import Notification


class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = [
            'user', 'type', 'title', 'message', 'related_id',
            'is_read', 'read_at',
        ]
