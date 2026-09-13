from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import Communication
from .serializers import CommunicationSerializer
from .forms import CommunicationForm


def app_index(request):
    contexto = {
        "form": CommunicationForm(),
        'form_communication': CommunicationForm(),
        'module_name': 'Comunicados'
    }
    
    return render(request, 'communications/index.html', contexto)


@require_POST
def crear_comunicacion(request):
    form = CommunicationForm(request.POST)
    if form.is_valid():
        comunicacion = form.save(commit=False)
        comunicacion.sender = request.user
        comunicacion.save()
        messages.success(request, 'Comunicado creado correctamente.')
    else:
        messages.error(request, 'No se pudo crear el comunicado. Revisa los datos enviados.')
    return redirect('inicio')


class CommunicationViewSet(viewsets.ModelViewSet):
    """ViewSet para Communication"""
    queryset = Communication.objects.all()
    serializer_class = CommunicationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'body', 'sender__email']
    ordering_fields = ['published_at', 'created_at']
    ordering = ['-published_at', '-created_at']
    filterset_fields = ['garden', 'target_type', 'is_published']

