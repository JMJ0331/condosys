from django.contrib import messages
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import AreaComun
from .serializers import AreaComunSerializer
from .forms import AreaComunForm

PAGINATE_BY = 15


@login_required
def app_index(request):
    areas_qs = AreaComun.objects.all().order_by('name')

    estado = request.GET.get('estado', '')
    tipo = request.GET.get('tipo', '')

    if estado:
        areas_qs = areas_qs.filter(status=estado)
    if tipo:
        areas_qs = areas_qs.filter(area_type=tipo)

    paginator = Paginator(areas_qs, PAGINATE_BY)
    pagina = request.GET.get('page')
    try:
        areas = paginator.page(pagina)
    except PageNotAnInteger:
        areas = paginator.page(1)
    except EmptyPage:
        areas = paginator.page(paginator.num_pages)

    query = request.GET.copy()
    query.pop('page', None)

    contexto = {
        'areas': areas,
        'tipos_area': AreaComun.TIPO_AREA_CHOICES,
        'estados_area': AreaComun.ESTADO_CHOICES,
        'estado_actual': estado,
        'tipo_actual': tipo,
        'paginacion_query': query.urlencode(),
        'module_name': 'Áreas Comunes'
    }
    return render(request, 'areas_comunes/index.html', contexto)


@login_required
def agregar_area_comun(request):
    if request.method == 'POST':
        form = AreaComunForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Área común creada correctamente.')
            return redirect('areas_comunes_index')
        messages.error(request, 'No se pudo crear el área común. Revisa los datos enviados.')
    else:
        form = AreaComunForm()

    contexto = {
        'form_area': form,
        'module_name': 'Áreas Comunes',
        'titulo_modulo': 'Agregar área común',
        'url_form': 'agregar_area_comun',
        'url_form_args': [],
        'texto_boton': 'Agregar',
    }
    return render(request, 'areas_comunes/agregar.html', contexto)


@login_required
def actualizar_area_comun(request, pk):
    area = AreaComun.objects.filter(pk=pk).first()
    if not area:
        messages.error(request, 'Área común no encontrada.')
        return redirect('areas_comunes_index')

    if request.method == 'POST':
        form = AreaComunForm(request.POST, instance=area)
        if form.is_valid():
            form.save()
            messages.success(request, 'Área común actualizada correctamente.')
            return redirect('areas_comunes_index')
        messages.error(request, 'No se pudo actualizar el área común. Revisa los datos enviados.')
    else:
        form = AreaComunForm(instance=area)

    contexto = {
        'form_area': form,
        'module_name': 'Áreas Comunes',
        'titulo_modulo': 'Actualizar área común',
        'url_form': 'actualizar_area_comun',
        'url_form_args': [str(area.id)],
        'texto_boton': 'Actualizar',
    }
    return render(request, 'areas_comunes/agregar.html', contexto)


@login_required
def eliminar_area_comun(request, pk):
    area = AreaComun.objects.filter(pk=pk).first()
    if not area:
        messages.error(request, 'Área común no encontrada.')
        return redirect('areas_comunes_index')

    if request.method == 'POST':
        nombre = area.name
        area.delete()
        messages.success(request, f'Área común {nombre} eliminada correctamente.')
        return redirect('areas_comunes_index')

    # GET: no debería llegar aquí directo, pero por seguridad
    return redirect('areas_comunes_index')


class AreaComunViewSet(viewsets.ModelViewSet):
    queryset = AreaComun.objects.all()
    serializer_class = AreaComunSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'area_type', 'status']
    ordering_fields = ['name', 'created_at']
