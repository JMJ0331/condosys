import secrets
from datetime import timedelta

from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone

from accounts.models import User

from .correos import enviar_correo_recuperacion
from .models import PasswordResetToken

# Vigencia del enlace de recuperación (regla: 15 a 30 minutos).
DURACION_TOKEN_MINUTOS = 30

# Respuesta genérica: se muestra exista o no el correo en la base de datos
# para evitar el reconocimiento de usuarios (user enumeration).
MENSAJE_ENVIADO = (
    'Si el correo corresponde a una cuenta activa, recibirás un mensaje con '
    'las instrucciones para restablecer tu contraseña en los próximos minutos.'
)


def login_view(request):
    error = None

    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=email, password=password)

        if user is not None and user.is_active and user.status == 'active':
            django_login(request, user)
            # Solo el admin configura el residencial: el resto de roles entra
            # directo a su módulo. Si el gate de configuración incluyera al
            # manager, /residencial/ lo rechazaría y volvería a /inicio/, que
            # el middleware volvería a mandar a /residencial/ (bucle).
            if user.role == 'admin':
                from residencial.models import Residencial
                if Residencial.obtener_unico() is None:
                    return redirect('residencial_index')
            if user.role == 'security':
                return redirect('visitantes_index')
            return redirect('inicio')

        error = 'El email o la contraseña no son válidos.'

    return render(request, 'login/index.html', {'error': error})


def cerrar_sesion(request):
    if request.method == 'POST':
        django_logout(request)
    return redirect('login')


def solicitar_recuperacion(request):
    """Paso 1: pide el correo y envía el enlace de restablecimiento."""
    enviado = False

    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        user = (
            User.objects
            .filter(email__iexact=email, is_active=True, status='active')
            .first()
        )

        if user is not None:
            # Un solo enlace vigente por usuario: el último pedido invalida
            # los anteriores.
            PasswordResetToken.objects.filter(user=user, used_at__isnull=True).delete()

            token = secrets.token_hex(32)
            PasswordResetToken.objects.create(
                user=user,
                token=token,
                expires_at=timezone.now() + timedelta(minutes=DURACION_TOKEN_MINUTOS),
            )
            enlace = request.build_absolute_uri(
                reverse('restablecer_clave') + '?token=' + token
            )
            try:
                enviar_correo_recuperacion(user, enlace)
            except Exception:
                # El fallo ya quedó logueado en el servicio de correo; aquí se
                # responde igual de forma genérica para no revelar cuentas.
                pass

        enviado = True

    return render(request, 'login/recuperar_clave.html', {
        'enviado': enviado,
        'mensaje': MENSAJE_ENVIADO,
    })


def restablecer_clave(request):
    """Paso 2: valida el token del enlace y guarda la nueva contraseña."""
    token = request.POST.get('token') or request.GET.get('token', '')
    registro = (
        PasswordResetToken.objects
        .select_related('user')
        .filter(token=token)
        .first()
    ) if token else None

    valido = registro is not None and registro.es_valido()
    error = None
    exitoso = False

    if request.method == 'POST':
        if not valido:
            error = 'El enlace no es válido, ya fue usado o ha expirado. Solicita uno nuevo.'
        else:
            clave1 = request.POST.get('password', '')
            clave2 = request.POST.get('password_confirmacion', '')

            if clave1 != clave2:
                error = 'Las contraseñas no coinciden.'
            else:
                try:
                    validate_password(clave1, registro.user)
                except ValidationError as exc:
                    error = ' '.join(exc.messages)
                else:
                    registro.user.set_password(clave1)
                    registro.user.save(update_fields=['password'])
                    registro.marcar_como_usado()
                    exitoso = True

    return render(request, 'login/restablecer_clave.html', {
        'token': token,
        'valido': valido,
        'error': error,
        'exitoso': exitoso,
    })
