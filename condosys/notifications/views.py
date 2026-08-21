from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import Notification
from .serializers import NotificationSerializer
from .forms import NotificationForm


def app_index(request):
    contexto = {
        'form_notification': NotificationForm(),
        'module_name': 'Notificaciones'
    }
    return render(request, 'notifications/index.html', contexto)


class NotificationViewSet(viewsets.ModelViewSet):
    """ViewSet para Notification"""
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['user__email', 'title', 'message']
    ordering_fields = ['created_at', 'type']
    ordering = ['-created_at']
    filterset_fields = ['user', 'type', 'is_read']
    def get_queryset(self):
        user = self.request.user
        if user.role in ['admin', 'manager']:
            return Notification.objects.all()
        return Notification.objects.filter(user=user)
