from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import Visitor
from .serializers import VisitorSerializer


class VisitorViewSet(viewsets.ModelViewSet):
    """ViewSet para Visitor"""
    queryset = Visitor.objects.all()
    serializer_class = VisitorSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'document', 'apartment__number']
    ordering_fields = ['scheduled_entry', 'status']
    ordering = ['-scheduled_entry']
    filterset_fields = ['apartment', 'status', 'type']

