from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import CommonArea, Reservation
from .serializers import (
    CommonAreaSerializer, ReservationListSerializer,
    ReservationDetailSerializer
)


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

