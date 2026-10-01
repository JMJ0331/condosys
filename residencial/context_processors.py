def residencial_configurado(request):
    """Expone si ya existe la configuración del residencial y si el sidebar va bloqueado."""
    user = getattr(request, 'user', None)
    try:
        from residencial.models import Residencial
        configurado = Residencial.obtener_unico() is not None
    except Exception:
        configurado = True
    bloqueado = bool(
        user is not None
        and user.is_authenticated
        and getattr(user, 'role', '') in ('admin', 'manager')
        and not configurado
    )
    return {
        'residencial_configurado': configurado,
        'residencial_bloqueado': bloqueado,
    }
