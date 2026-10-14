"""Páginas de Estructura (solo administrador): Jardines, Bloques y Edificios.

Las tres comparten vistas genéricas configuradas en ENTIDADES: listado con
tabla, filtros en cascada y paginación; formulario de alta/edición y borrado
protegido (no se elimina un nivel que todavía tiene dependientes).
"""
from django.contrib import messages
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Count, ProtectedError
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import role_required
from accounts.permissions import ROLES_ADMIN

from .forms import BlockForm, BuildingForm, GardenForm
from .models import Block, Building, Garden

PAGINATE_BY = 15


def _texto(valor):
    return '—' if valor in (None, '') else valor


ENTIDADES = {
    'jardines': {
        'modelo': Garden,
        'form': GardenForm,
        'singular': 'jardín',
        'plural': 'Jardines',
        'titulo_lista': 'Todos los jardines',
        'icono': 'images/icons/blancos/leaf_white.svg',
        'urls': ('jardines_index', 'agregar_jardin', 'actualizar_jardin', 'eliminar_jardin'),
        'queryset': lambda: Garden.objects.annotate(
            total_bloques=Count('blocks', distinct=True),
            total_edificios=Count('buildings', distinct=True),
        ).order_by('name'),
        'filtros': (),
        'columnas': (
            ('Nombre', lambda o: o.name),
            ('Ubicación', lambda o: _texto(o.location)),
            ('Bloques', lambda o: o.total_bloques),
            ('Edificios', lambda o: o.total_edificios),
            ('Estado', lambda o: 'Activo' if o.is_active else 'Inactivo'),
        ),
        'dependientes': 'bloques o edificios',
    },
    'bloques': {
        'modelo': Block,
        'form': BlockForm,
        'singular': 'bloque',
        'plural': 'Bloques',
        'titulo_lista': 'Todos los bloques',
        'icono': 'images/icons/blancos/page_white.svg',
        'urls': ('bloques_index', 'agregar_bloque', 'actualizar_bloque', 'eliminar_bloque'),
        'queryset': lambda: Block.objects.select_related('garden').annotate(
            total_edificios=Count('buildings'),
        ).order_by('garden__name', 'name'),
        'filtros': (('jardin', 'garden_id'),),
        'columnas': (
            ('Nombre', lambda o: o.name),
            ('Jardín', lambda o: o.garden.name),
            ('Edificios', lambda o: o.total_edificios),
            ('Estado', lambda o: 'Activo' if o.is_active else 'Inactivo'),
        ),
        'dependientes': 'edificios',
    },
    'edificios': {
        'modelo': Building,
        'form': BuildingForm,
        'singular': 'edificio',
        'plural': 'Edificios',
        'titulo_lista': 'Todos los edificios',
        'icono': 'images/icons/blancos/city_white.svg',
        'urls': ('edificios_index', 'agregar_edificio', 'actualizar_edificio', 'eliminar_edificio'),
        'queryset': lambda: Building.objects.select_related('garden', 'block').annotate(
            total_departamentos=Count('apartments'),
        ).order_by('garden__name', 'block__name', 'name'),
        'filtros': (('jardin', 'garden_id'), ('bloque', 'block_id')),
        'columnas': (
            ('Nombre', lambda o: o.name),
            ('Bloque', lambda o: o.block.name),
            ('Jardín', lambda o: o.garden.name),
            ('Pisos', lambda o: _texto(o.number_of_floors)),
            ('Departamentos', lambda o: o.total_departamentos),
            ('Estado', lambda o: 'Activo' if o.is_active else 'Inactivo'),
        ),
        'dependientes': 'departamentos',
    },
}


def _contexto_base(clave):
    entidad = ENTIDADES[clave]
    url_index, url_agregar, url_actualizar, url_eliminar = entidad['urls']
    return {
        'entidad': entidad,
        'clave_entidad': clave,
        'module_name': entidad['plural'],
        'url_index': url_index,
        'url_agregar': url_agregar,
        'url_actualizar': url_actualizar,
        'url_eliminar': url_eliminar,
    }


@role_required(*ROLES_ADMIN)
def listar(request, clave):
    entidad = ENTIDADES[clave]
    qs = entidad['queryset']()

    valores_filtro = {}
    for parametro, campo in entidad['filtros']:
        valor = request.GET.get(parametro, '')
        valores_filtro[parametro] = valor
        if valor:
            qs = qs.filter(**{campo: valor})

    estado = request.GET.get('estado', '')
    if estado == 'activo':
        qs = qs.filter(is_active=True)
    elif estado == 'inactivo':
        qs = qs.filter(is_active=False)

    paginator = Paginator(qs, PAGINATE_BY)
    try:
        pagina = paginator.page(request.GET.get('page'))
    except PageNotAnInteger:
        pagina = paginator.page(1)
    except EmptyPage:
        pagina = paginator.page(paginator.num_pages)

    query = request.GET.copy()
    query.pop('page', None)

    contexto = _contexto_base(clave)
    contexto.update({
        'pagina': pagina,
        'cabeceras': [titulo for titulo, _ in entidad['columnas']],
        'filas': [
            {'objeto': objeto, 'celdas': [(titulo, valor(objeto)) for titulo, valor in entidad['columnas']]}
            for objeto in pagina
        ],
        'filtros': [parametro for parametro, _ in entidad['filtros']],
        'jardines': Garden.objects.order_by('name'),
        'bloques': Block.objects.select_related('garden').order_by('garden__name', 'name'),
        'jardin_actual': valores_filtro.get('jardin', ''),
        'bloque_actual': valores_filtro.get('bloque', ''),
        'estado_actual': estado,
        'paginacion_query': query.urlencode(),
    })
    return render(request, 'structure/estructura/index.html', contexto)


def _formulario(request, clave, instancia=None):
    entidad = ENTIDADES[clave]
    contexto = _contexto_base(clave)
    accion = 'actualizado' if instancia else 'creado'

    if request.method == 'POST':
        form = entidad['form'](request.POST, instance=instancia)
        if form.is_valid():
            objeto = form.save()
            messages.success(request, f'{entidad["singular"].capitalize()} {objeto.name} {accion} correctamente.')
            return redirect(contexto['url_index'])
        messages.error(request, f'No se pudo guardar el {entidad["singular"]}. Revisa los datos enviados.')
    else:
        form = entidad['form'](instance=instancia)

    contexto.update({
        'form': form,
        'titulo_modulo': f'{"Actualizar" if instancia else "Agregar"} {entidad["singular"]}',
        'texto_boton': 'Actualizar' if instancia else 'Agregar',
        'url_form_args': [str(instancia.pk)] if instancia else [],
        'url_form': contexto['url_actualizar'] if instancia else contexto['url_agregar'],
    })
    return render(request, 'structure/estructura/formulario.html', contexto)


@role_required(*ROLES_ADMIN)
def agregar(request, clave):
    return _formulario(request, clave)


@role_required(*ROLES_ADMIN)
def actualizar(request, clave, pk):
    instancia = get_object_or_404(ENTIDADES[clave]['modelo'], pk=pk)
    return _formulario(request, clave, instancia)


@role_required(*ROLES_ADMIN)
def eliminar(request, clave, pk):
    entidad = ENTIDADES[clave]
    url_index = entidad['urls'][0]
    if request.method != 'POST':
        return redirect(url_index)

    instancia = entidad['modelo'].objects.filter(pk=pk).first()
    if not instancia:
        messages.error(request, f'{entidad["singular"].capitalize()} no encontrado.')
        return redirect(url_index)

    nombre = instancia.name
    try:
        instancia.delete()
    except ProtectedError:
        messages.error(
            request,
            f'No se puede eliminar {nombre}: todavía tiene {entidad["dependientes"]} asociados. '
            'Elimínalos o reasígnalos primero.',
        )
    else:
        messages.success(request, f'{entidad["singular"].capitalize()} {nombre} eliminado correctamente.')
    return redirect(url_index)
