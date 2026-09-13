"""
URL configuration for condosys project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('areas-comunes/', include('areas_comunes.urls')),
    path('', include('login.urls')),
    path('inicio/', include('inicio.urls')),
    path('cuentas/', include('accounts.urls')),
    path('chat/', include('chat.urls')),
    path('comunicados/', include('communications.urls')),
    path('incidencias/', include('incidents.urls')),
    path('mantenimientos/', include('maintenance.urls')),
    path('notificaciones/', include('notifications.urls')),
    path('pagos/', include('payments.urls')),
    path('propietarios/', include('propietarios.urls')),
    path('reportes/', include('reports.urls')),
    path('reservas/', include('reservations.urls')),
    path('residentes/', include('residents.urls')),
    path('departamentos/', include('structure.urls')),
    path('visitantes/', include('visitors.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
