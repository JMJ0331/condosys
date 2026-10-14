
from django.urls import path
from .views import *

urlpatterns = [
    path('', login_view, name='login'),
    path('salir/', cerrar_sesion, name='cerrar_sesion'),
    path('recuperar-clave/', solicitar_recuperacion, name='recuperar_clave'),
    path('restablecer-clave/', restablecer_clave, name='restablecer_clave'),
]
