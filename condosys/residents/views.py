from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from .models import Resident
from .serializers import ResidentSerializer


def app_index(request):
    return render(request, 'residents/index.html', {'module_name': 'Residentes'})


class ResidentViewSet(viewsets.ModelViewSet):
    """ViewSet para Resident"""
    queryset = Resident.objects.all()
    serializer_class = ResidentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['user__email', 'apartment__number']
    ordering_fields = ['created_at', 'move_in_date']
    ordering = ['apartment', '-move_in_date']
    filterset_fields = ['apartment', 'role_in_apartment']

    def get_queryset(self):
        user = self.request.user
        if user.role in ['admin', 'manager']:
            return Resident.objects.all()
        return Resident.objects.filter(user=user)

    def perform_create(self, serializer):
        if self.request.user.role not in ['admin', 'manager']:
            raise PermissionDenied('Solo administradores pueden crear residentes.')
        serializer.save()

