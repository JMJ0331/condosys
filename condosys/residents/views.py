from django.contrib import messages
from django.contrib import messages
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import redirect, render
from rest_framework import filters, viewsets
from accounts.permissions import IsManager
from structure.models import Apartment
from .forms import ResidentForm
from .models import Resident
from .serializers import ResidentSerializer

PAGINATE_BY = 15


# @login_required
def app_index(request):
    qs = Resident.objects.select_related(
        'apartment__building__garden', 'user',
        'apartment__owner', 'apartment__owner__user',
    ).all()

    estado = request.GET.get('estado', '')
    apartamento = request.GET.get('apartamento', '')

    if estado == 'activo':
        qs = qs.filter(is_active=True)
    elif estado == 'inactivo':
        qs = qs.filter(is_active=False)

    if apartamento:
        qs = qs.filter(apartment_id=apartamento)

    paginator = Paginator(qs, PAGINATE_BY)
    page = request.GET.get('page')
    try:
        residentes = paginator.page(page)
    except PageNotAnInteger:
        residentes = paginator.page(1)
    except EmptyPage:
        residentes = paginator.page(paginator.num_pages)

    query = request.GET.copy()
    query.pop('page', None)

    contexto = {
        'residentes': residentes,
        'apartamentos': Apartment.objects.filter(is_active=True).select_related('building__garden'),
        'estado_actual': estado,
        'apartamento_actual': apartamento,
        'paginacion_query': query.urlencode(),
        'module_name': 'Residentes',
    }
    return render(request, 'residents/index.html', contexto)


# @login_required
def crear_residente(request):
    if request.method == 'POST':
        form = ResidentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Residente registrado correctamente.')
            return redirect('residentes_index')
        messages.error(request, 'No se pudo registrar el residente. Revisa los datos enviados.')
    else:
        form = ResidentForm()

    contexto = {
        'form_resident': form,
        'module_name': 'Residentes',
        'titulo_modulo': 'Agregar residente',
        'url_form': 'crear_residente',
        'url_form_args': [],
        'texto_boton': 'Agregar',
    }
    return render(request, 'residents/nuevo.html', contexto)


# @login_required
def actualizar_residente(request, pk):
    residente = Resident.objects.filter(pk=pk).first()
    if not residente:
        messages.error(request, 'Residente no encontrado.')
        return redirect('residentes_index')

    if request.method == 'POST':
        form = ResidentForm(request.POST, request.FILES, instance=residente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Residente actualizado correctamente.')
            return redirect('residentes_index')
        messages.error(request, 'No se pudo actualizar el residente. Revisa los datos enviados.')
    else:
        form = ResidentForm(instance=residente)

    contexto = {
        'form_resident': form,
        'module_name': 'Residentes',
        'titulo_modulo': 'Actualizar residente',
        'url_form': 'actualizar_residente',
        'url_form_args': [str(residente.id)],
        'texto_boton': 'Actualizar',
    }
    return render(request, 'residents/nuevo.html', contexto)


# @login_required
def eliminar_residente(request, pk):
    residente = Resident.objects.filter(pk=pk).first()
    if not residente:
        messages.error(request, 'Residente no encontrado.')
        return redirect('residentes_index')

    if request.method == 'POST':
        nombre = residente.full_name
        residente.delete()
        messages.success(request, f'Residente {nombre} eliminado correctamente.')
        return redirect('residentes_index')

    # GET: no debería llegar aquí directo, pero por seguridad
    return redirect('residentes_index')


class ResidentViewSet(viewsets.ModelViewSet):
    """ViewSet para Resident"""
    queryset = Resident.objects.all()
    serializer_class = ResidentSerializer
    permission_classes = [IsManager]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['user__email', 'apartment__number']
    ordering_fields = ['created_at', 'full_name']
    ordering = ['apartment', 'full_name']
    filterset_fields = ['apartment', 'is_active', 'marital_status']

    def get_queryset(self):
        user = self.request.user
        if user.role in ['admin', 'manager']:
            return Resident.objects.all()
        return Resident.objects.filter(user=user)