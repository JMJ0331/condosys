from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from residents.models import Resident
from residencial.models import Residencial
from structure.models import Apartment, Building, Garden

from .models import Incident, IncidentHistory


def crear_base():
    Residencial.objects.create(nombre='Residencial Rialto', distribucion='torres')
    jardin = Garden.objects.create(name='Jardín Central')
    edificio = Building.objects.create(garden=jardin, name='Torre A')
    apartamento = Apartment.objects.create(building=edificio, name='A-102')
    residente = Resident.objects.create(
        apartment=apartamento, full_name='Juan Perez',
        cedula='001-1234567-8', phone='809-000-0000',
    )
    usuario = User.objects.create_user(
        email='admin@test.com', password='Clave12345',
        role='admin', status='active',
    )
    return {'apartamento': apartamento, 'residente': residente, 'usuario': usuario}


def crear_incidencia(base, descripcion='Fuga de agua en el baño principal del apartamento', estado='new'):
    return Incident.objects.create(
        apartment=base['apartamento'], resident=base['residente'],
        reported_by=base['usuario'], category='plumbing',
        priority='high', title='Plomería: Fuga',
        description=descripcion, reported_date='2026-09-10',
        status=estado,
    )


class IncidenciasViewTests(TestCase):
    def test_index_muestra_cuadricula(self):
        base = crear_base()
        crear_incidencia(base)
        respuesta = self.client.get(reverse('incidencias_index'))
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, 'Todas las incidencias')
        self.assertContains(respuesta, 'A-102')
        self.assertContains(respuesta, 'Juan Perez')
        self.assertContains(respuesta, 'Plomería')
        self.assertContains(respuesta, 'Nueva')

    def test_columna_comentarios_recortada(self):
        base = crear_base()
        incidencia = crear_incidencia(base)
        IncidentHistory.objects.create(
            incident=incidencia, status_from='new', status_to='assigned',
            changed_by=base['usuario'],
            comment='Se asignó al técnico con prioridad alta para revisión inmediata del daño',
        )
        respuesta = self.client.get(reverse('incidencias_index'))
        self.assertContains(respuesta, 'Se asignó al técnico')
        self.assertNotContains(respuesta, 'revisión inmediata del daño')

    def test_filtra_por_estado_departamento_residente(self):
        base = crear_base()
        crear_incidencia(base)
        respuesta = self.client.get(reverse('incidencias_index'), {'estado': 'resolved'})
        self.assertNotContains(respuesta, '10/09/2026')
        respuesta = self.client.get(
            reverse('incidencias_index'), {'apartamento': str(base['apartamento'].id)}
        )
        self.assertContains(respuesta, '10/09/2026')
        respuesta = self.client.get(
            reverse('incidencias_index'), {'residente': str(base['residente'].id)}
        )
        self.assertContains(respuesta, 'Juan Perez')

    def test_agregar_crea_incidencia(self):
        base = crear_base()
        self.client.force_login(base['usuario'])
        respuesta = self.client.post(reverse('agregar_incidencia'), {
            'apartment': str(base['apartamento'].id),
            'resident': str(base['residente'].id),
            'category': 'electricity',
            'priority': 'normal',
            'description': 'Corto en el pasillo',
            'reported_date': '2026-09-12',
            'status': 'new',
            'comment': 'Revisar el breaker',
        })
        self.assertEqual(respuesta.status_code, 302)
        incidencia = Incident.objects.get()
        self.assertEqual(incidencia.category, 'electricity')
        self.assertEqual(incidencia.history.count(), 1)

    def test_actualizar_modifica_incidencia(self):
        base = crear_base()
        incidencia = crear_incidencia(base)
        self.client.force_login(base['usuario'])
        respuesta = self.client.post(
            reverse('actualizar_incidencia', args=[str(incidencia.id)]),
            {
                'apartment': str(base['apartamento'].id),
                'resident': str(base['residente'].id),
                'category': 'plumbing',
                'priority': 'urgent',
                'description': incidencia.description,
                'reported_date': '2026-09-10',
                'status': 'in_progress',
                'comment': '',
            },
        )
        self.assertEqual(respuesta.status_code, 302)
        incidencia.refresh_from_db()
        self.assertEqual(incidencia.priority, 'urgent')

    def test_eliminar_borra_incidencia(self):
        base = crear_base()
        incidencia = crear_incidencia(base)
        respuesta = self.client.post(reverse('eliminar_incidencia', args=[str(incidencia.id)]))
        self.assertEqual(respuesta.status_code, 302)
        self.assertEqual(Incident.objects.count(), 0)
