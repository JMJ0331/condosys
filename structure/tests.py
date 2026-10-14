from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from accounts.models import User
from propietarios.forms import PropietarioForm
from propietarios.models import Propietario
from residencial.models import Residencial
from residents.forms import ResidentForm
from residents.models import Resident
from .models import Apartment, Block, Building, Garden


def crear_usuario(email='admin@test.com', role='admin'):
    return User.objects.create_user(email=email, password='Clave12345', role=role, status='active')


def crear_jerarquia():
    jardin = Garden.objects.create(name='Jardín Norte')
    bloque = Block.objects.create(garden=jardin, name='Bloque A')
    edificio = Building.objects.create(block=bloque, name='Torre 1')
    departamento = Apartment.objects.create(building=edificio, name='101')
    return jardin, bloque, edificio, departamento


def crear_propietario(cedula='001-0000001-1', email='duenno@test.com'):
    return Propietario.objects.create(full_name='Ana Duenno', cedula=cedula, phone='(809)-000-0000', email=email)


class EstructuraBaseTests(TestCase):
    def setUp(self):
        Residencial.objects.create(nombre='Residencial Rialto', distribucion='torres')
        self.admin = crear_usuario()
        self.client.force_login(self.admin)


class ModeloJerarquiaTests(TestCase):
    def test_edificio_toma_jardin_del_bloque(self):
        jardin, bloque, edificio, _ = crear_jerarquia()
        self.assertEqual(edificio.garden, jardin)

    def test_edificio_solo_con_jardin_cae_en_bloque_general(self):
        jardin = Garden.objects.create(name='Jardín Sur')
        edificio = Building.objects.create(garden=jardin, name='Torre 9')
        self.assertEqual(edificio.block.name, 'General')
        self.assertEqual(edificio.block.garden, jardin)


class EstructuraVistasTests(EstructuraBaseTests):
    def test_listados_admin(self):
        crear_jerarquia()
        for nombre in ('jardines_index', 'bloques_index', 'edificios_index'):
            respuesta = self.client.get(reverse(nombre))
            self.assertEqual(respuesta.status_code, 200, nombre)
        self.assertContains(self.client.get(reverse('bloques_index')), 'Bloque A')

    def test_manager_no_accede(self):
        self.client.force_login(crear_usuario('gestor@test.com', 'manager'))
        for nombre in ('jardines_index', 'agregar_bloque', 'agregar_edificio'):
            respuesta = self.client.get(reverse(nombre))
            self.assertRedirects(respuesta, reverse('inicio'), fetch_redirect_response=False)

    def test_crear_jardin_bloque_edificio(self):
        self.client.post(reverse('agregar_jardin'), {'name': 'Jardín Este', 'is_active': 'on'})
        jardin = Garden.objects.get(name='Jardín Este')
        self.client.post(reverse('agregar_bloque'), {'garden': jardin.pk, 'name': 'Bloque B', 'is_active': 'on'})
        bloque = Block.objects.get(name='Bloque B')
        respuesta = self.client.post(reverse('agregar_edificio'), {
            'jardin': jardin.pk, 'block': bloque.pk, 'name': 'Torre 5', 'is_active': 'on',
        })
        self.assertRedirects(respuesta, reverse('edificios_index'), fetch_redirect_response=False)
        edificio = Building.objects.get(name='Torre 5')
        self.assertEqual(edificio.garden, jardin)

    def test_no_elimina_bloque_con_edificios(self):
        _, bloque, _, _ = crear_jerarquia()
        self.client.post(reverse('eliminar_bloque', args=[bloque.pk]))
        self.assertTrue(Block.objects.filter(pk=bloque.pk).exists())

    def test_formulario_edificio_opciones_en_cascada(self):
        jardin, bloque, _, _ = crear_jerarquia()
        respuesta = self.client.get(reverse('agregar_edificio'))
        self.assertContains(respuesta, f'data-jardin="{jardin.pk}"')
        self.assertContains(respuesta, 'data-cascada="bloque"')

    def test_departamentos_filtra_por_bloque(self):
        _, bloque, _, departamento = crear_jerarquia()
        otro = Block.objects.create(garden=bloque.garden, name='Bloque Z')
        Apartment.objects.create(building=Building.objects.create(block=otro, name='Torre Z'), name='ZZ-9')
        respuesta = self.client.get(reverse('departamentos_index'), {'bloque': bloque.pk})
        self.assertContains(respuesta, departamento.name)
        self.assertNotContains(respuesta, 'ZZ-9')


class EstructuraApiTests(TestCase):
    def setUp(self):
        Residencial.objects.create(nombre='Residencial Rialto', distribucion='torres')
        self.api = APIClient()
        self.jardin = Garden.objects.create(name='Jardín API')

    def test_manager_lee_pero_no_crea_bloques(self):
        self.api.force_authenticate(crear_usuario('gestor@test.com', 'manager'))
        self.assertEqual(self.api.get(reverse('bloque-list')).status_code, 200)
        respuesta = self.api.post(reverse('bloque-list'), {'garden': str(self.jardin.pk), 'name': 'X'})
        self.assertEqual(respuesta.status_code, 403)

    def test_admin_crea_bloques(self):
        self.api.force_authenticate(crear_usuario())
        respuesta = self.api.post(reverse('bloque-list'), {'garden': str(self.jardin.pk), 'name': 'X'})
        self.assertEqual(respuesta.status_code, 201)


class PropietarioDepartamentosTests(TestCase):
    def datos(self, departamentos, **extra):
        datos = {
            'full_name': 'Ana Duenno', 'marital_status': 'single', 'cedula': '001-0000001-1',
            'phone': '(809)-000-0000', 'email': 'duenno@test.com', 'is_active': 'on',
            'password': 'ClaveSegura#2026', 'password_confirmation': 'ClaveSegura#2026',
            'departamentos': [str(d.pk) for d in departamentos],
        }
        datos.update(extra)
        return datos

    def test_asigna_departamentos_al_crear(self):
        *_, departamento = crear_jerarquia()
        form = PropietarioForm(self.datos([departamento]))
        self.assertTrue(form.is_valid(), form.errors)
        propietario = form.save()
        departamento.refresh_from_db()
        self.assertEqual(departamento.owner, propietario)

    def test_solo_ofrece_departamentos_libres(self):
        *_, departamento = crear_jerarquia()
        departamento.owner = crear_propietario('002-0000002-2', 'otro@test.com')
        departamento.save()
        self.assertNotIn(departamento, PropietarioForm().fields['departamentos'].queryset)

    def test_quitar_departamento_libera_y_bloquea_con_residentes(self):
        _, _, edificio, departamento = crear_jerarquia()
        segundo = Apartment.objects.create(building=edificio, name='102')
        propietario = crear_propietario()
        Apartment.objects.filter(pk__in=[departamento.pk, segundo.pk]).update(owner=propietario)
        Resident.objects.create(apartment=departamento, full_name='Res Uno', cedula='003-0000003-3', phone='(809)-111-1111')

        form = PropietarioForm(self.datos([segundo], password='', password_confirmation=''), instance=propietario)
        self.assertFalse(form.is_valid())
        self.assertIn('departamentos', form.errors)

        form = PropietarioForm(self.datos([departamento], password='', password_confirmation=''), instance=propietario)
        self.assertTrue(form.is_valid(), form.errors)
        form.save()
        segundo.refresh_from_db()
        self.assertIsNone(segundo.owner)


class ResidenteDepartamentoTests(TestCase):
    def test_solo_departamentos_con_propietario(self):
        _, _, edificio, departamento = crear_jerarquia()
        libre = Apartment.objects.create(building=edificio, name='102')
        departamento.owner = crear_propietario()
        departamento.save()
        opciones = ResidentForm().fields['apartment'].queryset
        self.assertIn(departamento, opciones)
        self.assertNotIn(libre, opciones)

    def test_api_rechaza_departamento_sin_propietario(self):
        from residents.serializers import ResidentSerializer
        *_, departamento = crear_jerarquia()
        serializer = ResidentSerializer(data={
            'apartment': str(departamento.pk), 'full_name': 'Res', 'cedula': '004-0000004-4', 'phone': '(809)-222-2222',
        })
        self.assertFalse(serializer.is_valid())
        self.assertIn('apartment', serializer.errors)
