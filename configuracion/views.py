import json

from accounts.decorators import role_required
from accounts.models import User
from accounts.permissions import ROLES_ADMIN
from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import IntegracionIAForm, UsuarioCreateForm, UsuarioForm
from .models import IntegracionIA


@role_required(*ROLES_ADMIN)
def app_index(request):
    """Página de configuración: pestaña Usuarios visible, resto pendiente."""
    usuarios_qs = User.objects.all().order_by('-created_at')

    estado = request.GET.get('estado', '')
    if estado:
        usuarios_qs = usuarios_qs.filter(status=estado)

    integracion = IntegracionIA.obtener_unica()
    contexto = {
        'module_name': 'Configuración',
        'usuarios': usuarios_qs,
        'total_usuarios': usuarios_qs.count(),
        'estado_actual': estado,
        'form_ia': IntegracionIAForm(instance=integracion),
        'ia_configurada': bool(integracion and integracion.api_key),
        'modelos_json': json.dumps(IntegracionIA.MODELOS_POR_PROVEEDOR),
    }
    return render(request, 'configuracion/index.html', contexto)


@role_required(*ROLES_ADMIN)
def guardar_ia(request):
    """Guarda el modelo AI y su API Key (registro único)."""
    if request.method != 'POST':
        return redirect('configuracion_index')

    integracion = IntegracionIA.obtener_unica()
    form = IntegracionIAForm(request.POST, instance=integracion)
    if form.is_valid():
        # En blanco se guarda vacío (permite quitar la clave).
        form.save()
        messages.success(request, 'Integración AI guardada correctamente.')
    else:
        messages.error(request, 'No se pudo guardar la integración AI. Revisa los datos enviados.')
    return redirect('configuracion_index')


@role_required(*ROLES_ADMIN)
def crear_usuario(request):
    """Alta de un usuario con contraseña temporal (igual que las demás secciones)."""
    if request.method == 'POST':
        form = UsuarioCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario creado correctamente.')
            return redirect('configuracion_index')
        messages.error(request, 'No se pudo crear el usuario. Revisa los datos enviados.')
    else:
        form = UsuarioCreateForm(initial={'role': 'resident', 'status': 'active'})

    contexto = {
        'form_usuario': form,
        'module_name': 'Configuración',
        'titulo_modulo': 'Agregar usuario',
        'url_form': 'crear_usuario',
        'url_form_args': [],
        'texto_boton': 'Agregar',
        'es_alta': True,
    }
    return render(request, 'configuracion/crear.html', contexto)


@role_required(*ROLES_ADMIN)
def actualizar_usuario(request, pk):
    """Edición de un usuario (misma página de formulario que las demás secciones)."""
    usuario = User.objects.filter(pk=pk).first()
    if not usuario:
        messages.error(request, 'Usuario no encontrado.')
        return redirect('configuracion_index')

    es_propia = usuario.pk == request.user.pk
    if request.method == 'POST':
        form = UsuarioForm(request.POST, request.FILES, instance=usuario)
        if form.is_valid():
            cuenta = form.save(commit=False)
            if es_propia:
                # La cuenta propia no se puede desactivar ni degradar:
                # bloquearía el acceso de quien la edita.
                cuenta.role = 'admin'
                cuenta.status = 'active'
                cuenta.is_active = True
                messages.warning(
                    request,
                    'No puedes cambiar el rol ni desactivar tu propia cuenta; se mantuvo activa.',
                )
            cuenta.save()
            messages.success(request, 'Usuario actualizado correctamente.')
            return redirect('configuracion_index')
        messages.error(request, 'No se pudo actualizar el usuario. Revisa los datos enviados.')
    else:
        form = UsuarioForm(instance=usuario)

    contexto = {
        'form_usuario': form,
        'module_name': 'Configuración',
        'titulo_modulo': 'Actualizar usuario',
        'url_form': 'actualizar_usuario',
        'url_form_args': [str(usuario.pk)],
        'texto_boton': 'Actualizar',
    }
    return render(request, 'configuracion/editar.html', contexto)


@role_required(*ROLES_ADMIN)
def eliminar_usuario(request, pk):
    """Eliminación con confirmación por diálogo (igual que las demás secciones)."""
    usuario = User.objects.filter(pk=pk).first()
    if not usuario:
        messages.error(request, 'Usuario no encontrado.')
        return redirect('configuracion_index')

    if request.method == 'POST':
        if usuario.pk == request.user.pk:
            messages.error(request, 'No puedes eliminar tu propia cuenta.')
            return redirect('configuracion_index')
        correo = usuario.email
        usuario.delete()
        messages.success(request, f'Usuario {correo} eliminado correctamente.')
        return redirect('configuracion_index')

    return redirect('configuracion_index')
