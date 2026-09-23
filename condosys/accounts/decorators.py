from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


def role_required(*roles):
    """
    Decorador para vistas basadas en función: requiere inicio de sesión y
    que user.role esté entre los roles permitidos. Si no, redirige al módulo
    inicial del rol (security → visitantes) con un mensaje de error.
    """
    def decorator(view_func):
        @login_required
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            roles_planos = roles[0] if len(roles) == 1 and isinstance(roles[0], (list, tuple)) else roles
            if request.user.role not in roles_planos:
                messages.error(
                    request,
                    'No tienes permisos para acceder a este módulo.',
                )
                if request.user.role == 'security':
                    return redirect('visitantes_index')
                return redirect('inicio')
            return view_func(request, *args, **kwargs)
        return _wrapped
    return decorator