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
            return redirect('inicio')

        error = 'El email o la contraseña no son válidos.'

    return render(request, 'login/index.html', {'error': error})


# Create your views here.


def login_view(request):
    return render(request, 'login/index.html')