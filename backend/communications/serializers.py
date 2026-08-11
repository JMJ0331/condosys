from rest_framework import serializers
from .models import Communication


class CommunicationSerializer(serializers.ModelSerializer):
    """Serializer para Communication"""
    sender_email = serializers.CharField(source='sender.email', read_only=True)
    garden_name = serializers.CharField(source='garden.name', read_only=True)
    
    class Meta:
        model = Communication
        fields = [
            'id', 'garden', 'garden_name', 'sender',
            'sender_email', 'title', 'body', 'target_type',
            'target_id', 'is_published', 'published_at',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'published_at']
