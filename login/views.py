from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.shortcuts import redirect, render

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
