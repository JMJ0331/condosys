from datetime import datetime

from django.contrib import messages
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from accounts.permissions import CanModifyVisitor
from structure.models import Apartment
from .models import Visitor
from .serializers import VisitorSerializer
from .forms import VisitorForm

PAGINATE_BY = 15

MESES_NOMBRE = {
    1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril',
    5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto',
    9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre',
}


def _anios_con_visitas():
    """Años con visitas programadas (desc), incluyendo el año actual."""
    anios = {fecha.year for fecha in Visitor.objects.dates('scheduled_entry', 'year')}
    anios.add(timezone.localdate().year)
    return sorted(anios, reverse=True)


# @login_required
def app_index(request):
    visitas_qs = (
        Visitor.objects
        .select_related('apartment__building', 'authorized_by')
        .order_by('-scheduled_entry')
    )

    estado = request.GET.get('estado', '')
    apartamento = request.GET.get('apartamento', '')
    tipo = request.GET.get('tipo', '')
    dia = request.GET.get('dia', '')
    mes = request.GET.get('mes', '')
    anio = request.GET.get('anio', '')

    if estado:
        visitas_qs = visitas_qs.filter(status=estado)
    if apartamento:
        visitas_qs = visitas_qs.filter(apartment_id=apartamento)
    if tipo:
        visitas_qs = visitas_qs.filter(type=tipo)
    try:
        fecha_dia = datetime.strptime(dia, '%Y-%m-%d').date() if dia else None
    except ValueError:
        fecha_dia = None
        dia = ''
    if fecha_dia:
        visitas_qs = visitas_qs.filter(scheduled_entry__date=fecha_dia)
    if mes.isdigit() and 1 <= int(mes) <= 12:
        visitas_qs = visitas_qs.filter(scheduled_entry__month=int(mes))
    else:
        mes = ''
    if anio.isdigit():
        visitas_qs = visitas_qs.filter(scheduled_entry__year=int(anio))
    else:
        anio = ''

    paginator = Paginator(visitas_qs, PAGINATE_BY)
    pagina = request.GET.get('page')
    try:
        visitas = paginator.page(pagina)
    except PageNotAnInteger:
        visitas = paginator.page(1)
    except EmptyPage:
        visitas = paginator.page(paginator.num_pages)

    query = request.GET.copy()
    query.pop('page', None)

    contexto = {
        'visitas': visitas,
        'apartamentos': Apartment.objects.filter(is_active=True),
        'estado_actual': estado,
        'apartamento_actual': apartamento,
        'tipo_actual': tipo,
        'dia_actual': dia,
        'mes_actual': mes,
        'anio_actual': anio,
        'mes_actual_nombre': MESES_NOMBRE.get(int(mes), 'Todos los meses') if mes else 'Todos los meses',
        'anios': _anios_con_visitas(),
        'paginacion_query': query.urlencode(),
        'module_name': 'Visitantes',
    }
    return render(request, 'visitors/index.html', contexto)


# @login_required
def agregar_visitante(request):
    if request.method == 'POST':
        form = VisitorForm(request.POST, request.FILES)
        if form.is_valid():
            visitante = form.save(commit=False)
            visitante.registered_by = request.user
            visitante.save()
            messages.success(request, 'Visitante registrado correctamente.')
            return redirect('visitantes_index')
        messages.error(request, 'No se pudo registrar el visitante. Revisa los datos enviados.')
    else:
        form = VisitorForm()

    contexto = {
        'form_visitor': form,
        'module_name': 'Visitantes',
        'titulo_modulo': 'Agregar visitante',
        'url_form': 'agregar_visitante',
        'url_form_args': [],
        'texto_boton': 'Agregar',
    }
    return render(request, 'visitors/agregar.html', contexto)


# @login_required
def actualizar_visitante(request, pk):
    visita = Visitor.objects.filter(pk=pk).first()
    if not visita:
        messages.error(request, 'Visita no encontrada.')
        return redirect('visitantes_index')

    if request.method == 'POST':
        form = VisitorForm(request.POST, request.FILES, instance=visita)
        if form.is_valid():
            form.save()
            messages.success(request, 'Visita actualizada correctamente.')
            return redirect('visitantes_index')
        messages.error(request, 'No se pudo actualizar la visita. Revisa los datos enviados.')
    else:
        form = VisitorForm(instance=visita)

    contexto = {
        'form_visitor': form,
        'visita': visita,
        'module_name': 'Visitantes',
        'titulo_modulo': 'Actualizar visitante',
        'url_form': 'actualizar_visitante',
        'url_form_args': [str(visita.id)],
        'texto_boton': 'Actualizar',
    }
    return render(request, 'visitors/agregar.html', contexto)


# @login_required
@require_POST
def eliminar_visitante(request, pk):
    visita = Visitor.objects.filter(pk=pk).first()
    if not visita:
        messages.error(request, 'Visita no encontrada.')
        return redirect('visitantes_index')

    detalle = f'{visita.name} - {visita.apartment.name}'
    visita.delete()
    messages.success(request, f'Visita {detalle} eliminada correctamente.')
    return redirect('visitantes_index')


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
