from django.contrib import messages
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import redirect, render
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from structure.models import Garden
from .models import Communication
from .serializers import CommunicationSerializer
from .forms import CommunicationForm


PAGINATE_BY = 15


def _resolver_garden(user):
    """Devuelve el jardín al que pertenece un comunicado.

    Prioriza el jardín del usuario; si no lo tiene, usa el primero activo.
    Retorna None si no hay ningún jardín configurado.
    """
    garden = getattr(user, 'garden', None)
    if garden is not None:
        return garden
    return Garden.objects.filter(is_active=True).order_by('name').first()


# @login_required
def app_index(request):
    comunicados_qs = Communication.objects.select_related('garden', 'sender').all()

    categoria = request.GET.get('categoria', '')
    estado = request.GET.get('estado', '')

    if categoria:
        comunicados_qs = comunicados_qs.filter(category=categoria)
    if estado == 'published':
        comunicados_qs = comunicados_qs.filter(is_published=True)
    elif estado == 'draft':
        comunicados_qs = comunicados_qs.filter(is_published=False)

    paginator = Paginator(comunicados_qs, PAGINATE_BY)
    pagina = request.GET.get('page')
    try:
        comunicados = paginator.page(pagina)
    except PageNotAnInteger:
        comunicados = paginator.page(1)
    except EmptyPage:
        comunicados = paginator.page(paginator.num_pages)

    query = request.GET.copy()
    query.pop('page', None)

    contexto = {
        'comunicados': comunicados,
        'categoria_actual': categoria,
        'estado_actual': estado,
        'paginacion_query': query.urlencode(),
        'module_name': 'Comunicados',
    }
    return render(request, 'communications/index.html', contexto)


# @login_required
def agregar_comunicado(request):
    if request.method == 'POST':
        form = CommunicationForm(request.POST, request.FILES)
        if form.is_valid():
            garden = _resolver_garden(request.user)
            if garden is None:
                messages.error(
                    request,
                    'No se pudo crear el comunicado: no hay ningún jardín configurado. '
                    'Crea al menos uno desde la sección de departamentos.',
                )
                return redirect('comunicados_index')
            comunicacion = form.save(commit=False)
            comunicacion.sender = request.user
            comunicacion.garden = garden
            comunicacion.save()
            messages.success(request, 'Comunicado creado correctamente.')
            return redirect('comunicados_index')
        messages.error(request, 'No se pudo crear el comunicado. Revisa los datos enviados.')
    else:
        form = CommunicationForm()

    contexto = {
        'form_communication': form,
        'module_name': 'Comunicados',
        'titulo_modulo': 'Nuevo comunicado',
    }
    return render(request, 'communications/agregar.html', contexto)


# @login_required
def eliminar_comunicado(request, pk):
    comunicado = Communication.objects.filter(pk=pk).first()
    if not comunicado:
        messages.error(request, 'Comunicado no encontrado.')
        return redirect('comunicados_index')

    if request.method == 'POST':
        comunicado.delete()
        messages.success(request, 'Comunicado eliminado correctamente.')
        return redirect('comunicados_index')

    return redirect('comunicados_index')


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