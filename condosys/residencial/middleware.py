from django.shortcuts import redirect


class ResidencialSetupMiddleware:
    """Fuerza a admin/manager a configurar el residencial antes de usar el sistema.

    Mientras no exista el registro del residencial, redirige a /residencial/.
    El sidebar muestra el resto de opciones en gris (ver aside.html).
    """

    RUTAS_EXENTAS = ('/residencial/', '/admin/', '/static/', '/media/')

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, 'user', None)
        if (
            user is not None
            and user.is_authenticated
            and getattr(user, 'role', '') in ('admin', 'manager')
            and not request.path.startswith(self.RUTAS_EXENTAS)
        ):
            from residencial.models import Residencial
            if Residencial.obtener_unico() is None:
                return redirect('residencial_index')
        return self.get_response(request)
