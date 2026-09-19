from django.contrib.auth import authenticate, login as django_login
from django.shortcuts import redirect, render

def login_view(request):
    error = None

    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=email, password=password)

        if user is not None and user.is_active and user.status == 'active':
            django_login(request, user)
            # Admin/manager nuevo: si aún no hay residencial configurado,
            # va directo a configurarlo antes de usar el sistema.
            if user.role in ('admin', 'manager'):
                from residencial.models import Residencial
                if Residencial.obtener_unico() is None:
                    return redirect('residencial_index')
            return redirect('inicio')

        error = 'El email o la contraseña no son válidos.'

    return render(request, 'login/index.html', {'error': error})
