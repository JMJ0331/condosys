from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import Notification
from .serializers import NotificationSerializer
from .forms import NotificationForm


# @login_required
def app_index(request):
    contexto = {
        'form_notification': NotificationForm(),
        'module_name': 'Notificaciones'
    }
    return render(request, 'notifications/index.html', contexto)


# @login_required
@require_POST
def crear_notificacion(request):
    form = NotificationForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, 'Notificación creada correctamente.')
    else:
        messages.error(request, 'No se pudo crear la notificación. Revisa los datos enviados.')
    return redirect('inicio')


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
