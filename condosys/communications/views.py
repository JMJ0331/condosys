from django.contrib import messages
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from accounts.decorators import role_required
from accounts.permissions import ROLES_GESTION, ROLES_TODOS, IsGestionOrSoloLectura
from structure.models import Garden
from .models import Communication
from .serializers import CommunicationSerializer
from .forms import CommunicationForm

PAGINATE_BY = 15


@role_required(*ROLES_TODOS)
def app_index(request):
    comunicados_qs = (
        Communication.objects
        .select_related('garden', 'sender')
        .order_by('-published_at', '-created_at')
    )

    estado = request.GET.get('estado', '')
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
        'estado_actual': estado,
        'paginacion_query': query.urlencode(),
        'module_name': 'Comunicados'
    }

    return render(request, 'communications/index.html', contexto)


def _guardar_comunicado(request, form, es_nuevo):
    if form.is_valid():
        comunicacion = form.save(commit=False)
        if es_nuevo:
            comunicacion.sender = request.user
            comunicacion.garden = Garden.objects.first()
        comunicacion.save()
        messages.success(
            request,
            'Comunicado creado correctamente.' if es_nuevo else 'Comunicado actualizado correctamente.',
        )
        return redirect('comunicados_index')
    messages.error(request, 'No se pudo guardar el comunicado. Revisa los datos enviados.')
    return None


@role_required(*ROLES_GESTION)
def agregar_comunicado(request):
    if request.method == 'POST':
        form = CommunicationForm(request.POST, request.FILES)
        respuesta = _guardar_comunicado(request, form, es_nuevo=True)
        if respuesta:
            return respuesta
    else:
        form = CommunicationForm()

    contexto = {
        'form_communication': form,
        'module_name': 'Comunicados',
        'titulo_modulo': 'Agregar comunicado',
        'url_form': 'agregar_comunicado',
        'url_form_args': [],
        'texto_boton': 'Agregar',
    }
    return render(request, 'communications/agregar.html', contexto)


@role_required(*ROLES_GESTION)
def actualizar_comunicado(request, pk):
    comunicado = Communication.objects.filter(pk=pk).first()
    if not comunicado:
        messages.error(request, 'Comunicado no encontrado.')
        return redirect('comunicados_index')

    if request.method == 'POST':
        form = CommunicationForm(request.POST, request.FILES, instance=comunicado)
        respuesta = _guardar_comunicado(request, form, es_nuevo=False)
        if respuesta:
            return respuesta
    else:
        form = CommunicationForm(
            instance=comunicado,
            initial={
                'estado': 'published' if comunicado.is_published else 'draft',
                'publication_date': comunicado.published_at,
            },
        )

    contexto = {
        'form_communication': form,
        'module_name': 'Comunicados',
        'titulo_modulo': 'Actualizar comunicado',
        'url_form': 'actualizar_comunicado',
        'url_form_args': [str(comunicado.id)],
        'texto_boton': 'Actualizar',
    }
    return render(request, 'communications/agregar.html', contexto)


@role_required(*ROLES_GESTION)
def eliminar_comunicado(request, pk):
    comunicado = Communication.objects.filter(pk=pk).first()
    if not comunicado:
        messages.error(request, 'Comunicado no encontrado.')
        return redirect('comunicados_index')

    if request.method == 'POST':
        titulo = comunicado.title
        comunicado.delete()
        messages.success(request, f'Comunicado {titulo} eliminado correctamente.')
        return redirect('comunicados_index')

    # GET: no debería llegar aquí directo, pero por seguridad
    return redirect('comunicados_index')


class CommunicationViewSet(viewsets.ModelViewSet):
    """ViewSet para Communication"""
    queryset = Communication.objects.all()
    serializer_class = CommunicationSerializer
    permission_classes = [IsGestionOrSoloLectura]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'body', 'sender__email']
    ordering_fields = ['published_at', 'created_at']
    ordering = ['-published_at', '-created_at']
    filterset_fields = ['garden', 'target_type', 'is_published']
