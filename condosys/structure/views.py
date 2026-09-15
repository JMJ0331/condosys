from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import redirect, render
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import CanAccessApartment
from .models import Garden, Building, Apartment
from .serializers import (
    GardenSerializer, BuildingSerializer,
    ApartmentListSerializer, ApartmentDetailSerializer
)
from .forms import ApartmentsForm

PAGINATE_BY = 15


# @login_required
def app_index(request):
    apartamentos_qs = (
        Apartment.objects.select_related('building__garden', 'owner')
        .order_by('building__garden__name', 'building__name', 'floor', 'name')
    )

    estado = request.GET.get('estado', '')
    jardin = request.GET.get('jardin', '')
    edificio = request.GET.get('edificio', '')

    if estado:
        apartamentos_qs = apartamentos_qs.filter(status=estado)
    if jardin:
        apartamentos_qs = apartamentos_qs.filter(building__garden_id=jardin)
    if edificio:
        apartamentos_qs = apartamentos_qs.filter(building_id=edificio)

    paginator = Paginator(apartamentos_qs, PAGINATE_BY)
    pagina = request.GET.get('page')
    try:
        departamentos = paginator.page(pagina)
    except PageNotAnInteger:
        departamentos = paginator.page(1)
    except EmptyPage:
        departamentos = paginator.page(paginator.num_pages)

    query = request.GET.copy()
    query.pop('page', None)

    contexto = {
        'departamentos': departamentos,
        'jardines': Garden.objects.filter(is_active=True),
        'edificios': Building.objects.filter(is_active=True),
        'estado_actual': estado,
        'jardin_actual': jardin,
        'edificio_actual': edificio,
        'paginacion_query': query.urlencode(),
        'module_name': 'Departamentos'
    }
    return render(request, 'structure/index.html', contexto)


# @login_required
def agregar_departamento(request):
    if request.method == 'POST':
        form = ApartmentsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Departamento creado correctamente.')
            return redirect('departamentos_index')
        messages.error(request, 'No se pudo crear el departamento. Revisa los datos enviados.')
    else:
        form = ApartmentsForm()

    contexto = {
        'form_apartments': form,
        'jardines': Garden.objects.filter(is_active=True),
        'edificios': Building.objects.filter(is_active=True),
        'module_name': 'Departamentos',
        'titulo_modulo': 'Agregar departamento',
        'url_form': 'agregar_departamento',
        'url_form_args': [],
        'texto_boton': 'Agregar',
    }
    return render(request, 'structure/agregar.html', contexto)


# @login_required
def actualizar_departamento(request, pk):
    apartamento = Apartment.objects.filter(pk=pk).first()
    if not apartamento:
        messages.error(request, 'Departamento no encontrado.')
        return redirect('departamentos_index')

    if request.method == 'POST':
        form = ApartmentsForm(request.POST, request.FILES, instance=apartamento)
        if form.is_valid():
            form.save()
            messages.success(request, 'Departamento actualizado correctamente.')
            return redirect('departamentos_index')
        messages.error(request, 'No se pudo actualizar el departamento. Revisa los datos enviados.')
    else:
        form = ApartmentsForm(instance=apartamento)

    contexto = {
        'form_apartments': form,
        'jardines': Garden.objects.filter(is_active=True),
        'edificios': Building.objects.filter(is_active=True),
        'module_name': 'Departamentos',
        'titulo_modulo': 'Actualizar departamento',
        'url_form': 'actualizar_departamento',
        'url_form_args': [str(apartamento.id)],
        'texto_boton': 'Actualizar',
    }
    return render(request, 'structure/agregar.html', contexto)


# @login_required
def eliminar_departamento(request, pk):
    apartamento = Apartment.objects.filter(pk=pk).first()
    if not apartamento:
        messages.error(request, 'Departamento no encontrado.')
        return redirect('departamentos_index')

    if request.method == 'POST':
        nombre = apartamento.name
        apartamento.delete()
        messages.success(request, f'Departamento {nombre} eliminado correctamente.')
        return redirect('departamentos_index')

    # GET: no debería llegar aquí directo, pero por seguridad
    return redirect('departamentos_index')


class GardenViewSet(viewsets.ModelViewSet):
    """ViewSet para Garden"""
    queryset = Garden.objects.filter(is_active=True)
    serializer_class = GardenSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'location']
    ordering_fields = ['created_at', 'name']
    ordering = ['-created_at']


class BuildingViewSet(viewsets.ModelViewSet):
    """ViewSet para Building"""
    queryset = Building.objects.filter(is_active=True)
    serializer_class = BuildingSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'garden__name']
    ordering_fields = ['created_at', 'name']
    ordering = ['garden', 'name']
    filterset_fields = ['garden']


class ApartmentViewSet(viewsets.ModelViewSet):
    """ViewSet para Apartment"""
    queryset = Apartment.objects.filter(is_active=True)
    permission_classes = [IsAuthenticated, CanAccessApartment]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'building__name', 'building__garden__name', 'owner__full_name']
    ordering_fields = ['created_at', 'name', 'status']
    ordering = ['building', 'floor', 'name']
    filterset_fields = ['building', 'status', 'owner']

    def get_queryset(self):
        user = self.request.user
        if user.role in ['admin', 'manager', 'maintenance', 'security']:
            return Apartment.objects.filter(is_active=True)
        return Apartment.objects.filter(is_active=True, residents__user=user, residents__is_active=True).distinct()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ApartmentDetailSerializer
        return ApartmentListSerializer

