from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import AreaComun
from .serializers import AreaComunSerializer
from .forms import AreaComunForm


# @login_required
def app_index(request):
    contexto = {
        'areas': AreaComun.objects.all(),
        'form_area': AreaComunForm(),
        'module_name': 'Áreas Comunes'
    }
    return render(request, 'areas_comunes/index.html', contexto)


# @login_required
@require_POST
def crear_area_comun(request):
    form = AreaComunForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, 'Área común creada correctamente.')
    else:
        messages.error(request, 'No se pudo crear el área común. Revisa los datos enviados.')
    return redirect('inicio')


class AreaComunViewSet(viewsets.ModelViewSet):
    queryset = AreaComun.objects.all()
    serializer_class = AreaComunSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'area_type', 'status']
    ordering_fields = ['name', 'created_at']