from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from accounts.models import User
from residencial.models import Residencial
from structure.models import Apartment, Building, Garden

from .models import Visitor


def crear_base():
    Residencial.objects.create(nombre='Residencial Rialto', distribucion='torres')
    jardin = Garden.objects.create(name='Jardín Central')
    edificio = Building.objects.create(garden=jardin, name='Torre A')
    apartamento = Apartment.objects.create(building=edificio, name='A-102')
    usuario = User.objects.create_user(
        email='admin@test.com', password='Clave12345',
        role='admin', status='active',
    )
    return {'apartamento': apartamento, 'usuario': usuario}


def crear_visita(base, nombre='Pedro Visita', tipo='family', estado='pending'):
    entrada = timezone.make_aware(timezone.datetime(2026, 9, 15, 10, 0))
    salida = timezone.make_aware(timezone.datetime(2026, 9, 15, 12, 0))
    return Visitor.objects.create(
        apartment=base['apartamento'], registered_by=base['usuario'],
        name=nombre, type=tipo, scheduled_entry=entrada,
        scheduled_exit=salida, status=estado,
    )


class VisitantesViewTests(TestCase):
    def test_index_muestra_cuadricula(self):
        base = crear_base()
        crear_visita(base)
        respuesta = self.client.get(reverse('visitantes_index'))
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, 'Todas las visitas')
        self.assertContains(respuesta, 'Pedro Visita')
        self.assertContains(respuesta, 'Familiar')
        self.assertContains(respuesta, 'A-102')
        self.assertContains(respuesta, 'Esperando')

    def test_filtra_por_estado_tipo_departamento(self):
        base = crear_base()
        crear_visita(base)
        respuesta = self.client.get(reverse('visitantes_index'), {'estado': 'authorized'})
        self.assertNotContains(respuesta, '15/09/2026')
        respuesta = self.client.get(reverse('visitantes_index'), {'tipo': 'delivery'})
        self.assertNotContains(respuesta, '15/09/2026')
        respuesta = self.client.get(
            reverse('visitantes_index'), {'apartamento': str(base['apartamento'].id)}
        )
        self.assertContains(respuesta, '15/09/2026')

    def test_filtra_por_dia_mes_anio(self):
        base = crear_base()
        crear_visita(base)
        respuesta = self.client.get(reverse('visitantes_index'), {'dia': '2026-09-15'})
        self.assertContains(respuesta, 'Pedro Visita')
        respuesta = self.client.get(reverse('visitantes_index'), {'dia': '2026-09-16'})
        self.assertNotContains(respuesta, 'Pedro Visita')
        respuesta = self.client.get(reverse('visitantes_index'), {'mes': '9', 'anio': '2026'})
        self.assertContains(respuesta, 'Pedro Visita')
        respuesta = self.client.get(reverse('visitantes_index'), {'anio': '2025'})
        self.assertNotContains(respuesta, 'Pedro Visita')

    def test_agregar_crea_visita(self):
        base = crear_base()
        self.client.force_login(base['usuario'])
        respuesta = self.client.post(reverse('agregar_visitante'), {
            'name': 'María Visita',
            'type': 'delivery',
            'document_type': 'cedula',
            'apartment': str(base['apartamento'].id),
            'authorized_by': str(base['usuario'].id),
            'status': 'pending',
            'fecha_entrada': '2026-09-20T10:00',
            'fecha_salida': '2026-09-20T12:00',
        })
        self.assertEqual(respuesta.status_code, 302)
        visita = Visitor.objects.get(name='María Visita')
        self.assertEqual(visita.apartment, base['apartamento'])

    def test_actualizar_modifica_visita(self):
        base = crear_base()
        visita = crear_visita(base)
        self.client.force_login(base['usuario'])
        respuesta = self.client.post(
            reverse('actualizar_visitante', args=[str(visita.id)]),
            {
                'name': 'Pedro Visita',
                'type': 'family',
                'document_type': '',
                'apartment': str(base['apartamento'].id),
                'authorized_by': str(base['usuario'].id),
                'status': 'authorized',
                'fecha_entrada': '2026-09-15T10:00',
                'fecha_salida': '2026-09-15T12:00',
            },
        )
        self.assertEqual(respuesta.status_code, 302)
        visita.refresh_from_db()
        self.assertEqual(visita.status, 'authorized')

    def test_eliminar_borra_visita(self):
        base = crear_base()
        visita = crear_visita(base)
        respuesta = self.client.post(reverse('eliminar_visitante', args=[str(visita.id)]))
        self.assertEqual(respuesta.status_code, 302)
        self.assertEqual(Visitor.objects.count(), 0)
