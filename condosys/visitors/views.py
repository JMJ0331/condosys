from django.db.models import Q
from django.utils import timezone
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from condosys.accounts.permissions import CanModifyVisitor
from .models import Visitor
from .serializers import VisitorSerializer


class VisitorViewSet(viewsets.ModelViewSet):
    """ViewSet para Visitor"""
    queryset = Visitor.objects.all()
    serializer_class = VisitorSerializer
    permission_classes = [IsAuthenticated, CanModifyVisitor]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'document', 'apartment__number']
    ordering_fields = ['scheduled_entry', 'status']
    ordering = ['-scheduled_entry']
    filterset_fields = ['apartment', 'status', 'type']

    def get_queryset(self):
        user = self.request.user
        if user.role in ['admin', 'manager', 'security']:
            return Visitor.objects.all()
        return Visitor.objects.filter(
            Q(registered_by=user) | Q(apartment__residents__user=user)
        ).distinct()

    @action(detail=True, methods=['post'])
    def authorize(self, request, pk=None):
        visitor = self.get_object()
        if request.user.role not in ['admin', 'manager', 'security']:
            return Response({'detail': 'No autorizado para autorizar visitantes.'}, status=status.HTTP_403_FORBIDDEN)
        if visitor.status != 'pending':
            return Response({'detail': 'Solo visitantes en espera pueden autorizarse.'}, status=status.HTTP_400_BAD_REQUEST)
        visitor.status = 'authorized'
        visitor.authorized_by = request.user
        visitor.save()
        return Response(self.get_serializer(visitor).data)

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        visitor = self.get_object()
        if request.user.role not in ['admin', 'manager', 'security']:
            return Response({'detail': 'No autorizado para rechazar visitantes.'}, status=status.HTTP_403_FORBIDDEN)
        if visitor.status != 'pending':
            return Response({'detail': 'Solo visitantes en espera pueden rechazarse.'}, status=status.HTTP_400_BAD_REQUEST)
        visitor.status = 'rejected'
        visitor.authorized_by = request.user
        visitor.save()
        return Response(self.get_serializer(visitor).data)

    @action(detail=True, methods=['post'])
    def check_in(self, request, pk=None):
        visitor = self.get_object()
        if request.user.role not in ['admin', 'manager', 'security']:
            return Response({'detail': 'No autorizado para registrar la entrada.'}, status=status.HTTP_403_FORBIDDEN)
        if visitor.status != 'authorized':
            return Response({'detail': 'Solo visitantes autorizados pueden registrar entrada real.'}, status=status.HTTP_400_BAD_REQUEST)
        visitor.actual_entry = timezone.now()
        visitor.status = 'completed'
        visitor.save()
        return Response(self.get_serializer(visitor).data)

    @action(detail=True, methods=['post'])
    def check_out(self, request, pk=None):
        visitor = self.get_object()
        if request.user.role not in ['admin', 'manager', 'security']:
            return Response({'detail': 'No autorizado para registrar la salida.'}, status=status.HTTP_403_FORBIDDEN)
        if visitor.actual_entry is None:
            return Response({'detail': 'No se ha registrado la entrada real aún.'}, status=status.HTTP_400_BAD_REQUEST)
        visitor.actual_exit = timezone.now()
        visitor.status = 'completed'
        visitor.save()
        return Response(self.get_serializer(visitor).data)

