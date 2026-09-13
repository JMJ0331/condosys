from django.contrib import messages
<<<<<<< HEAD
=======
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
>>>>>>> 92964151f67b4af53f5d5b1c0445adc7116e3df9
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


<<<<<<< HEAD
=======
# @login_required
>>>>>>> 92964151f67b4af53f5d5b1c0445adc7116e3df9
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


<<<<<<< HEAD
@require_POST
def crear_jardin(request):
    form = GardenForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, 'Jardín creado correctamente.')
    else:
        messages.error(request, 'No se pudo crear el jardín. Revisa los datos enviados.')
    return redirect('inicio')


@require_POST
def crear_edificio(request):
    form = BuildingForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, 'Edificio creado correctamente.')
    else:
        messages.error(request, 'No se pudo crear el edificio. Revisa los datos enviados.')
    return redirect('inicio')


@require_POST
def crear_departamento(request):
    form = ApartmentsForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()
        messages.success(request, 'Departamento creado correctamente.')
    else:
=======
# @login_required
def agregar_departamento(request):
    if request.method == 'POST':
        form = ApartmentsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Departamento creado correctamente.')
            return redirect('departamentos_index')
>>>>>>> 92964151f67b4af53f5d5b1c0445adc7116e3df9
        messages.error(request, 'No se pudo crear el departamento. Revisa los datos enviados.')
    else:
        form = ApartmentsForm()

    contexto = {
        'form_apartments': form,
        'jardines': Garden.objects.filter(is_active=True),
        'edificios': Building.objects.filter(is_active=True),
        'module_name': 'Departamentos'
    }
    return render(request, 'structure/agregar.html', contexto)


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

