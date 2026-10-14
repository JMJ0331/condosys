from django.urls import path

from .views import actualizar_usuario, app_index, crear_usuario, eliminar_usuario, guardar_ia

urlpatterns = [
    path('agregar/', crear_usuario, name='crear_usuario'),
    path('guardar-ia/', guardar_ia, name='guardar_ia'),
    path('actualizar/<uuid:pk>/', actualizar_usuario, name='actualizar_usuario'),
    path('eliminar/<uuid:pk>/', eliminar_usuario, name='eliminar_usuario'),
    path('', app_index, name='configuracion_index'),
]
