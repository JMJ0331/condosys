from rest_framework import serializers
from .models import AuditLog


class AuditLogSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source='user.email', read_only=True)
    details = serializers.SerializerMethodField()

    def get_details(self, obj):
        return {detail.key: detail.value for detail in obj.details.all()}

    class Meta:
        model = AuditLog
        fields = ['id', 'user', 'user_email', 'action', 'entity', 'entity_id', 'details', 'created_at']
        read_only_fields = ['id', 'created_at']
