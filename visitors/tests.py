from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from accounts.models import User
from propietarios.models import Propietario
from residencial.models import Residencial
from residents.models import Resident
from structure.models import Apartment, Building, Garden

from .forms import VisitorForm
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
    # "Autorizado por" solo admite al propietario o a un residente del
    # departamento, así que la base necesita al menos uno vinculado.
    residente = User.objects.create_user(
        email='residente@test.com', password='Clave12345',
        role='resident', status='active',
        first_name='Lucía', last_name='Soto',
    )
    Resident.objects.create(
        user=residente, apartment=apartamento,
        full_name='Lucía Soto', cedula='101010101', phone='3001234567',
    )
    return {'apartamento': apartamento, 'usuario': usuario, 'residente': residente}


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

    def test_filtra_por_mes_anio(self):
        base = crear_base()
        crear_visita(base)
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
            'authorized_by': str(base['residente'].id),
            'status': 'pending',
            'fecha_entrada': '2026-09-20T10:00',
            'fecha_salida': '2026-09-20T12:00',
        })
        self.assertEqual(respuesta.status_code, 302)
        visita = Visitor.objects.get(name='María Visita')
        self.assertEqual(visita.apartment, base['apartamento'])
        self.assertEqual(visita.authorized_by, base['residente'])

    def test_agregar_rechaza_autorizado_sin_vinculo(self):
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
        })
        self.assertEqual(respuesta.status_code, 200)
        self.assertFalse(Visitor.objects.filter(name='María Visita').exists())

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
                'authorized_by': str(base['residente'].id),
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


class VisitantesFormTests(TestCase):
    """El desplegable de "Autorizado por" se arma con la gente vinculada al
    departamento elegido, no con todos los usuarios del sistema."""

    def _base_con_dos_departamentos(self):
        base = crear_base()
        otra = User.objects.create_user(
            email='otro@test.com', password='Clave12345',
            role='resident', status='active',
            first_name='Carlos', last_name='Ríos',
        )
        edificio = base['apartamento'].building
        segundo = Apartment.objects.create(building=edificio, name='A-103')
        Resident.objects.create(
            user=otra, apartment=segundo,
            full_name='Carlos Ríos', cedula='202020202', phone='3007654321',
        )
        return base, segundo

    def _opciones(self, formulario, departamento_id):
        return next(
            o for o in formulario.opciones_departamento if o['id'] == departamento_id
        )

    def test_opciones_departamento_llevan_solo_a_sus_vinculados(self):
        base, segundo = self._base_con_dos_departamentos()
        otro_id = Resident.objects.get(apartment=segundo).user_id
        formulario = VisitorForm()
        ids_primero = self._opciones(formulario, base['apartamento'].id)['autorizados']
        ids_segundo = self._opciones(formulario, segundo.id)['autorizados']
        self.assertEqual(ids_primero, str(base['residente'].id))
        self.assertEqual(ids_segundo, str(otro_id))
        self.assertNotIn(str(otro_id), ids_primero)

    def test_desplegable_no_trae_usuarios_sin_vinculo(self):
        base, _ = self._base_con_dos_departamentos()
        disponibles = {
            str(valor)
            for valor, _etiqueta in VisitorForm().fields['authorized_by'].choices
            if valor
        }
        self.assertNotIn(str(base['usuario'].id), disponibles)
        self.assertIn(str(base['residente'].id), disponibles)

    def test_validar_rechaza_usuario_de_otro_departamento(self):
        base, segundo = self._base_con_dos_departamentos()
        visitante_otro = Resident.objects.get(apartment=segundo).user
        formulario = VisitorForm(data={
            'name': 'Visitante', 'type': 'family', 'document_type': 'cedula',
            'apartment': str(base['apartamento'].id),
            'authorized_by': str(visitante_otro.id),
            'status': 'pending',
            'fecha_entrada': '2026-09-20T10:00',
        })
        self.assertFalse(formulario.is_valid())
        self.assertIn('authorized_by', formulario.errors)

    def test_residente_dado_de_baja_deja_de_autorizar(self):
        base, _ = self._base_con_dos_departamentos()
        Resident.objects.filter(user=base['residente']).update(is_active=False)
        formulario = VisitorForm()
        self.assertEqual(
            self._opciones(formulario, base['apartamento'].id)['autorizados'], ''
        )

    def test_propietario_dado_de_baja_deja_de_autorizar(self):
        base = crear_base()
        duenno = User.objects.create_user(
            email='duenno@test.com', password='Clave12345',
            role='propietario', status='active',
            first_name='Andrés', last_name='Vega',
        )
        propietario = Propietario.objects.create(
            user=duenno, full_name='Andrés Vega',
            cedula='303030303', phone='3005555555',
        )
        base['apartamento'].owner = propietario
        base['apartamento'].save()
        departamento_id = base['apartamento'].id

        ids = self._opciones(VisitorForm(), departamento_id)['autorizados']
        self.assertIn(str(duenno.id), ids.split())

        propietario.is_active = False
        propietario.save()
        ids = self._opciones(VisitorForm(), departamento_id)['autorizados']
        self.assertNotIn(str(duenno.id), ids.split())

    def test_editar_conserva_autorizado_registro_inactivo(self):
        """Un "Autorizado por" ya guardado no se pierde aunque su registro
        de Residente/Propietario se haya dado de baja después."""
        base = crear_base()
        visita = crear_visita(base)
        visita.authorized_by = base['residente']
        visita.save()
        Resident.objects.filter(user=base['residente']).update(is_active=False)

        formulario = VisitorForm(instance=visita)
        ids = self._opciones(formulario, base['apartamento'].id)['autorizados']
        self.assertEqual(ids, str(base['residente'].id))

        formulario = VisitorForm(
            data={
                'name': 'Pedro Visita', 'type': 'family', 'document_type': '',
                'apartment': str(base['apartamento'].id),
                'authorized_by': str(base['residente'].id),
                'status': 'authorized',
                'fecha_entrada': '2026-09-15T10:00',
            },
            instance=visita,
        )
        self.assertTrue(formulario.is_valid(), formulario.errors)
