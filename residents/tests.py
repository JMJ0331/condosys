from django.contrib.auth import authenticate
from django.test import TestCase

from accounts.models import User
from accounts.serializers import UserSerializer
from structure.models import Apartment, Building, Garden

from .forms import ResidentForm
from .models import Resident
from .serializers import ResidentSerializer

CLAVE = 'ClaveSegura123!'


def crear_apartamento(nombre='T-101'):
    jardin = Garden.objects.create(name='Jardín Pruebas')
    edificio = Building.objects.create(garden=jardin, name='Torre P')
    return Apartment.objects.create(building=edificio, name=nombre)


def datos_residente(apartamento, **extras):
    datos = {
        'full_name': 'Rosa Perez',
        'marital_status': 'single',
        'cedula': '402-0000001-9',
        'phone': '809-555-0001',
        'email': 'rosa@test.com',
        'emergency_contact': '',
        'apartment': str(apartamento.pk),
        'tipo_relacion': 'propietario',
        'fecha_ingreso': '',
        'mascotas': 'no',
        'is_active': 'on',
        'password': CLAVE,
        'password_confirmation': CLAVE,
    }
    datos.update(extras)
    return datos


class ResidentFormTests(TestCase):
    def setUp(self):
        self.apartamento = crear_apartamento()

    def test_alta_crea_cuenta_hasheada_y_puede_entrar(self):
        form = ResidentForm(data=datos_residente(self.apartamento))
        self.assertTrue(form.is_valid(), form.errors)
        residente = form.save()

        cuenta = residente.user
        self.assertIsNotNone(cuenta)
        self.assertEqual(cuenta.role, 'resident')
        self.assertEqual(cuenta.status, 'active')
        self.assertTrue(cuenta.is_active)
        # Nunca queda la contraseña en texto plano en la base de datos.
        self.assertNotEqual(cuenta.password, CLAVE)
        self.assertTrue(cuenta.check_password(CLAVE))
        self.assertIsNotNone(authenticate(email='rosa@test.com', password=CLAVE))

    def test_alta_requiere_password(self):
        form = ResidentForm(data=datos_residente(self.apartamento, password='', password_confirmation=''))
        self.assertFalse(form.is_valid())
        self.assertIn('password', form.errors)

    def test_alta_rechaza_passwords_que_no_coinciden(self):
        form = ResidentForm(data=datos_residente(self.apartamento, password_confirmation='OtraClave123!'))
        self.assertFalse(form.is_valid())
        self.assertIn('password_confirmation', form.errors)

    def test_alta_rechaza_email_ya_registrado(self):
        User.objects.create_user(email='rosa@test.com', password='OtraClave123!')
        form = ResidentForm(data=datos_residente(self.apartamento))
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_edicion_sin_password_conserva_la_actual(self):
        form = ResidentForm(data=datos_residente(self.apartamento))
        residente = form.save()
        cuenta = residente.user

        datos = datos_residente(self.apartamento)
        del datos['password']
        del datos['password_confirmation']
        datos['full_name'] = 'Rosa Perez Actualizada'

        form_edicion = ResidentForm(data=datos, instance=residente)
        self.assertTrue(form_edicion.is_valid(), form_edicion.errors)
        residente_editado = form_edicion.save()

        self.assertEqual(residente_editado.user_id, cuenta.pk)
        self.assertTrue(cuenta.check_password(CLAVE))

    def test_edicion_con_password_la_cambia(self):
        form = ResidentForm(data=datos_residente(self.apartamento))
        residente = form.save()
        cuenta = residente.user

        nueva = 'NuevaClave123!'
        datos = datos_residente(self.apartamento, password=nueva, password_confirmation=nueva)
        form_final = ResidentForm(data=datos, instance=residente)
        self.assertTrue(form_final.is_valid(), form_final.errors)
        form_final.save()

        cuenta.refresh_from_db()
        self.assertTrue(cuenta.check_password(nueva))
        self.assertFalse(cuenta.check_password(CLAVE))

    def test_residente_sin_cuenta_puede_recibir_password_al_editar(self):
        residente = Resident.objects.create(
            apartment=self.apartamento, full_name='Luis Soto',
            cedula='402-0000002-9', phone='809-555-0002',
            email='luis@test.com', tipo_relacion='inquilino', is_active=True,
        )
        self.assertIsNone(residente.user)

        datos = datos_residente(
            self.apartamento, email='luis@test.com',
            cedula='402-0000002-9', full_name='Luis Soto',
        )
        form = ResidentForm(data=datos, instance=residente)
        self.assertTrue(form.is_valid(), form.errors)
        residente_editado = form.save()

        self.assertIsNotNone(residente_editado.user)
        self.assertEqual(residente_editado.user.role, 'resident')
        self.assertTrue(residente_editado.user.check_password(CLAVE))

    def test_serializadores_no_exponen_password(self):
        form = ResidentForm(data=datos_residente(self.apartamento))
        residente = form.save()

        self.assertNotIn('password', ResidentSerializer(residente).data)
        self.assertNotIn('password', UserSerializer(residente.user).data)
        self.assertNotIn('password', ResidentSerializer(residente).data.get('user_detail', {}))