from rest_framework import serializers
from .models import ChatMessage


class ChatMessageSerializer(serializers.ModelSerializer):
    """Serializer para ChatMessage"""
    sender_email = serializers.CharField(source='sender.email', read_only=True)
    receiver_email = serializers.CharField(source='receiver.email', read_only=True, allow_null=True)
    
    class Meta:
        model = ChatMessage
        fields = [
            'id', 'sender', 'sender_email', 'receiver',
            'receiver_email', 'group_name', 'message',
            'is_read', 'read_at', 'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'read_at']
