from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import CanAccessApartment
from .models import Garden, Building, Apartment
from .serializers import (
    GardenSerializer, BuildingSerializer,
    ApartmentListSerializer, ApartmentDetailSerializer
)
from .forms import *


@login_required
def app_index(request):

    contexto = {
        'form_garden': GardenForm(),
        'form_building': BuildingForm(),
        'form_apartments': ApartmentsForm(),
        'module_name': 'Departamentos'

    }
    return render(request, 'structure/index.html', contexto)


@login_required
@require_POST
def crear_jardin(request):
    form = GardenForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, 'Jardín creado correctamente.')
    else:
        messages.error(request, 'No se pudo crear el jardín. Revisa los datos enviados.')
    return redirect('inicio')


@login_required
@require_POST
def crear_edificio(request):
    form = BuildingForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, 'Edificio creado correctamente.')
    else:
        messages.error(request, 'No se pudo crear el edificio. Revisa los datos enviados.')
    return redirect('inicio')


@login_required
@require_POST
def crear_departamento(request):
    form = ApartmentsForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, 'Departamento creado correctamente.')
    else:
        messages.error(request, 'No se pudo crear el departamento. Revisa los datos enviados.')
    return redirect('inicio')


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
    search_fields = ['number', 'building__name', 'building__garden__name']
    ordering_fields = ['created_at', 'number', 'status']
    ordering = ['building', 'floor', 'number']
    filterset_fields = ['building', 'status', 'type']

    def get_queryset(self):
        user = self.request.user
        if user.role in ['admin', 'manager', 'maintenance', 'security']:
            return Apartment.objects.filter(is_active=True)
        return Apartment.objects.filter(is_active=True, residents__user=user, residents__is_active=True).distinct()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ApartmentDetailSerializer
        return ApartmentListSerializer

