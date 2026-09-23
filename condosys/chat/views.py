from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import ChatMessage
from .serializers import ChatMessageSerializer
from .forms import ChatGroupForm, ChatMessageForm


@login_required
def app_index(request):
    contexto = {
        'form_chat_group': ChatGroupForm(),
        'form_chat_message': ChatMessageForm(),
        'module_name': 'Chat'
    }
    return render(request, 'chat/index.html', contexto)


@login_required
@require_POST
def crear_grupo_chat(request):
    form = ChatGroupForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, 'Grupo de chat creado correctamente.')
    else:
        messages.error(request, 'No se pudo crear el grupo de chat. Revisa los datos enviados.')
    return redirect('inicio')


@login_required
@require_POST
def crear_mensaje_chat(request):
    form = ChatMessageForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, 'Mensaje enviado correctamente.')
    else:
        messages.error(request, 'No se pudo enviar el mensaje. Revisa los datos enviados.')
    return redirect('inicio')


class ChatMessageViewSet(viewsets.ModelViewSet):
    """ViewSet para ChatMessage"""
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['sender__email', 'receiver__email', 'message']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    filterset_fields = ['sender', 'receiver', 'group', 'is_read']

