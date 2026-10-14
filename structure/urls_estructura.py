from django.urls import path

from . import views_estructura as vistas

urlpatterns = []
for clave, entidad in vistas.ENTIDADES.items():
    url_index, url_agregar, url_actualizar, url_eliminar = entidad['urls']
    urlpatterns += [
        path(f'{clave}/', vistas.listar, {'clave': clave}, name=url_index),
        path(f'{clave}/agregar/', vistas.agregar, {'clave': clave}, name=url_agregar),
        path(f'{clave}/actualizar/<uuid:pk>/', vistas.actualizar, {'clave': clave}, name=url_actualizar),
        path(f'{clave}/eliminar/<uuid:pk>/', vistas.eliminar, {'clave': clave}, name=url_eliminar),
    ]
