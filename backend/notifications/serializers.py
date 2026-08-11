from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    """Serializer para Notification"""
    user_email = serializers.CharField(source='user.email', read_only=True)
    
    class Meta:
        model = Notification
        fields = [
            'id', 'user', 'user_email', 'type', 'title',
            'message', 'related_id', 'is_read', 'read_at',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'read_at']
