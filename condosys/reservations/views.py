from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import CommonArea, Reservation
from residents.models import Resident
from .serializers import (
    CommonAreaSerializer, ReservationListSerializer,
    ReservationDetailSerializer
)
from .forms import CommonAreaForm, ReservationForm


# @login_required
def app_index(request):
    contexto = {
        'form_common_area': CommonAreaForm(),
        'form_reservation': ReservationForm(),
        'residentes': Resident.objects.select_related('apartment').all(),
        'module_name': 'Reservas'
    }
    return render(request, 'reservations/index.html', contexto)


# @login_required
@require_POST
def crear_area_comun(request):
    form = CommonAreaForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, 'Área común creada correctamente.')
    else:
        messages.error(request, 'No se pudo crear el área común. Revisa los datos enviados.')
    return redirect('inicio')


# @login_required
@require_POST
def crear_reserva(request):
    form = ReservationForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, 'Reserva creada correctamente.')
    else:
        messages.error(request, 'No se pudo crear la reserva. Revisa los datos enviados.')
    return redirect('inicio')


class CommonAreaViewSet(viewsets.ModelViewSet):
    """ViewSet para CommonArea"""
    queryset = CommonArea.objects.filter(is_active=True)
    serializer_class = CommonAreaSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    filterset_fields = ['garden']


class ReservationViewSet(viewsets.ModelViewSet):
    """ViewSet para Reservation"""
    queryset = Reservation.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['reserved_by__email', 'common_area__name']
    ordering_fields = ['start_time', 'status']
    ordering = ['-start_time']
    filterset_fields = ['common_area', 'status', 'reserved_by']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ReservationDetailSerializer
        return ReservationListSerializer

