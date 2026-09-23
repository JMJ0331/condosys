from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import redirect, render
from rest_framework import filters, viewsets
from accounts.permissions import IsManager
from structure.models import Apartment
from .forms import PropietarioForm
from .models import Propietario
from .serializers import PropietarioSerializer

PAGINATE_BY = 15


@login_required
def app_index(request):
    qs = (
        Propietario.objects
        .select_related('user')
        .prefetch_related('apartments_owned__building__garden')
        .order_by('-created_at')
    )

    estado = request.GET.get('estado', '')
    apartamento = request.GET.get('apartamento', '')

    if estado == 'activo':
        qs = qs.filter(is_active=True)
    elif estado == 'inactivo':
        qs = qs.filter(is_active=False)

    if apartamento:
        qs = qs.filter(apartments_owned__id=apartamento)

    paginator = Paginator(qs, PAGINATE_BY)
    page = request.GET.get('page')
    try:
        propietarios = paginator.page(page)
    except PageNotAnInteger:
        propietarios = paginator.page(1)
    except EmptyPage:
        propietarios = paginator.page(paginator.num_pages)

    query = request.GET.copy()
    query.pop('page', None)

    contexto = {
        'propietarios': propietarios,
        'apartamentos': Apartment.objects.filter(is_active=True).select_related('building__garden'),
        'estado_actual': estado,
        'apartamento_actual': apartamento,
        'paginacion_query': query.urlencode(),
        'module_name': 'Propietarios',
    }
    return render(request, 'propietarios/index.html', contexto)


@login_required
def crear_propietario(request):
    if request.method == 'POST':
        form = PropietarioForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Propietario registrado correctamente.')
            return redirect('propietarios_index')
        messages.error(request, 'No se pudo registrar el propietario. Revisa los datos enviados.')
    else:
        form = PropietarioForm()

    contexto = {
        'form_owner': form,
        'module_name': 'Propietarios',
        'titulo_modulo': 'Agregar propietario',
        'url_form': 'crear_propietario',
        'url_form_args': [],
        'texto_boton': 'Agregar',
    }
    return render(request, 'propietarios/nuevo.html', contexto)


@login_required
def actualizar_propietario(request, pk):
    propietario = Propietario.objects.filter(pk=pk).first()
    if not propietario:
        messages.error(request, 'Propietario no encontrado.')
        return redirect('propietarios_index')

    if request.method == 'POST':
        form = PropietarioForm(request.POST, request.FILES, instance=propietario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Propietario actualizado correctamente.')
            return redirect('propietarios_index')
        messages.error(request, 'No se pudo actualizar el propietario. Revisa los datos enviados.')
    else:
        form = PropietarioForm(instance=propietario)

    contexto = {
        'form_owner': form,
        'module_name': 'Propietarios',
        'titulo_modulo': 'Actualizar propietario',
        'url_form': 'actualizar_propietario',
        'url_form_args': [str(propietario.id)],
        'texto_boton': 'Actualizar',
    }
    return render(request, 'propietarios/nuevo.html', contexto)


@login_required
def eliminar_propietario(request, pk):
    propietario = Propietario.objects.filter(pk=pk).first()
    if not propietario:
        messages.error(request, 'Propietario no encontrado.')
        return redirect('propietarios_index')

    if request.method == 'POST':
        nombre = propietario.full_name
        propietario.delete()
        messages.success(request, f'Propietario {nombre} eliminado correctamente.')
        return redirect('propietarios_index')

    # GET: no debería llegar aquí directo, pero por seguridad
    return redirect('propietarios_index')


class PropietarioViewSet(viewsets.ModelViewSet):
    """ViewSet para propietarios."""
    queryset = Propietario.objects.all()
    serializer_class = PropietarioSerializer
    permission_classes = [IsManager]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['full_name', 'cedula', 'email', 'apartments_owned__name']
    ordering_fields = ['full_name', 'created_at']
    ordering = ['full_name']
    filterset_fields = ['is_active']

    def get_queryset(self):
        user = self.request.user
        if user.role in ['admin', 'manager']:
            return Propietario.objects.all()
        return Propietario.objects.filter(user=user)
