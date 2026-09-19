from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated

from accounts.permissions import IsManager

from .forms import ResidencialForm
from .models import MUNICIPIOS_POR_PROVINCIA, Residencial
from .serializers import ResidencialSerializer


# @login_required  # TEMP pruebas: login deshabilitado como en las demás apps
def app_index(request):
    """Página única del residencial: crea el registro o actualiza el existente.

    Solo admin/manager pueden guardar; el resto lo ve en solo lectura.
    El texto del botón cambia según haya o no información guardada.
    """
    residencial = Residencial.obtener_unico()
    # TEMP pruebas: sin login request.user es anónimo (sin rol), así que
    # se permite editar para poder probar el formulario. Al reactivar el
    # login, el anónimo volverá a solo lectura (puede_editar=False).
    if request.user.is_authenticated:
        puede_editar = request.user.role in ['admin', 'manager']
    else:
        puede_editar = True

    if request.method == 'POST':
        if not puede_editar:
            messages.error(request, 'No tienes permiso para modificar el residencial.')
            return redirect('residencial_index')
        form = ResidencialForm(request.POST, instance=residencial)
        if form.is_valid():
            guardado = form.save()
            messages.success(
                request,
                'Residencial actualizado correctamente.' if residencial else 'Residencial agregado correctamente.',
            )
            return redirect('residencial_index')
        messages.error(request, 'No se pudo guardar el residencial. Revisa los datos enviados.')
    else:
        form = ResidencialForm(instance=residencial)

    contexto = {
        'form': form,
        'residencial': residencial,
        'existe_registro': residencial is not None,
        'puede_editar': puede_editar,
        'texto_boton': 'Actualizar' if residencial else 'Agregar',
        'municipios_por_provincia': MUNICIPIOS_POR_PROVINCIA,
        'module_name': 'Residencial',
    }
    return render(request, 'residencial/index.html', contexto)


class ResidencialViewSet(viewsets.ModelViewSet):
    """API del residencial (solo admin/manager pueden modificar)."""
    queryset = Residencial.objects.all().order_by('-updated_at')
    serializer_class = ResidencialSerializer
    permission_classes = [IsAuthenticated, IsManager]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombre', 'rnc', 'sector', 'municipio', 'provincia']
    ordering_fields = ['updated_at', 'nombre']
    ordering = ['-updated_at']
