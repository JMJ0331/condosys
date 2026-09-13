from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render
from rest_framework import filters, viewsets
from accounts.permissions import IsManager
from residents.models import Resident
from structure.models import Apartment
from .serializers import PropietarioSerializer

PAGINATE_BY = 15


# @login_required
def app_index(request):
    qs = (
        Resident.objects.filter(apartments_owned__isnull=False)
        .select_related('apartment__building__garden', 'user')
        .prefetch_related('apartments_owned__building__garden')
        .distinct()
    )

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


class PropietarioViewSet(viewsets.ModelViewSet):
    """ViewSet para propietarios (residentes dueños de apartamentos)."""
    queryset = Resident.objects.filter(apartments_owned__isnull=False).distinct()
    serializer_class = PropietarioSerializer
    permission_classes = [IsManager]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['full_name', 'cedula', 'email', 'apartments_owned__name']
    ordering_fields = ['full_name', 'created_at']
    ordering = ['full_name']
    filterset_fields = ['apartments_owned', 'is_active']

    def get_queryset(self):
        user = self.request.user
        if user.role in ['admin', 'manager']:
            return Resident.objects.filter(apartments_owned__isnull=False).distinct()
        return Resident.objects.none()