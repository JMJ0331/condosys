from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import ChatMessage
from .serializers import ChatMessageSerializer


class ChatMessageViewSet(viewsets.ModelViewSet):
    """ViewSet para ChatMessage"""
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['sender__email', 'receiver__email', 'message']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    filterset_fields = ['sender', 'receiver', 'group_name', 'is_read']

