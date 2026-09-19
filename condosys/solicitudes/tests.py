from django.test import TestCase
from django.urls import reverse

from residents.models import Resident
from structure.models import Apartment, Building, Garden

from .models import Solicitud


def crear_base():
    jardin = Garden.objects.create(name='Jardín Central')
    edificio = Building.objects.create(garden=jardin, name='Torre A')
    apartamento = Apartment.objects.create(building=edificio, name='A-102')
    residente = Resident.objects.create(
        apartment=apartamento, full_name='Juan Perez',
        cedula='001-1234567-8', phone='809-000-0000',
    )
    return {'apartamento': apartamento, 'residente': residente}


def crear_solicitud(base, tipo='mantenimiento', estado='pendiente'):
    return Solicitud.objects.create(
        apartment=base['apartamento'], resident=base['residente'],
        request_type=tipo, description='Ruido nocturno constante en el pasillo',
        request_date='2026-09-10', status=estado,
    )


class SolicitudesViewTests(TestCase):
    def test_index_muestra_cuadricula(self):
        base = crear_base()
        crear_solicitud(base)
        respuesta = self.client.get(reverse('solicitudes_index'))
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, 'Todas las solicitudes')
        self.assertContains(respuesta, 'A-102')
        self.assertContains(respuesta, 'Juan Perez')
        self.assertContains(respuesta, 'Pendiente')

    def test_filtra_por_estado_departamento_residente(self):
        base = crear_base()
        crear_solicitud(base)
        respuesta = self.client.get(reverse('solicitudes_index'), {'estado': 'aprobada'})
        self.assertNotContains(respuesta, '10/09/2026')
        respuesta = self.client.get(
            reverse('solicitudes_index'), {'apartamento': str(base['apartamento'].id)}
        )
        self.assertContains(respuesta, '10/09/2026')
        respuesta = self.client.get(
            reverse('solicitudes_index'), {'residente': str(base['residente'].id)}
        )
        self.assertContains(respuesta, 'Juan Perez')

    def test_agregar_crea_solicitud(self):
        base = crear_base()
        respuesta = self.client.post(reverse('agregar_solicitud'), {
            'apartment': str(base['apartamento'].id),
            'resident': str(base['residente'].id),
            'request_type': 'permiso',
            'description': 'Filtración en el techo',
            'request_date': '2026-09-12',
            'tracking_response': '',
            'status': 'pendiente',
        })
        self.assertEqual(respuesta.status_code, 302)
        solicitud = Solicitud.objects.get()
        self.assertEqual(solicitud.request_type, 'permiso')

    def test_actualizar_modifica_solicitud(self):
        base = crear_base()
        solicitud = crear_solicitud(base)
        respuesta = self.client.post(
            reverse('actualizar_solicitud', args=[str(solicitud.id)]),
            {
                'apartment': str(base['apartamento'].id),
                'resident': str(base['residente'].id),
                'request_type': 'mantenimiento',
                'description': solicitud.description,
                'request_date': '2026-09-10',
                'tracking_response': 'Técnico asignado',
                'status': 'en_proceso',
            },
        )
        self.assertEqual(respuesta.status_code, 302)
        solicitud.refresh_from_db()
        self.assertEqual(solicitud.status, 'en_proceso')
        self.assertEqual(solicitud.tracking_response, 'Técnico asignado')

    def test_eliminar_borra_solicitud(self):
        base = crear_base()
        solicitud = crear_solicitud(base)
        respuesta = self.client.post(reverse('eliminar_solicitud', args=[str(solicitud.id)]))
        self.assertEqual(respuesta.status_code, 302)
        self.assertEqual(Solicitud.objects.count(), 0)
