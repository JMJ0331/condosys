from django.contrib.auth import authenticate
from django.test import TestCase

from accounts.models import User
from accounts.serializers import UserSerializer

from .forms import PropietarioForm
from .models import Propietario
from .serializers import PropietarioSerializer

CLAVE = 'ClaveSegura123!'


def datos_propietario(**extras):
    datos = {
        'full_name': 'Mario Lopez',
        'marital_status': 'married',
        'cedula': '402-0000003-9',
        'phone': '809-555-0003',
        'email': 'mario@test.com',
        'emergency_contact': '',
        'is_active': 'on',
        'password': CLAVE,
        'password_confirmation': CLAVE,
    }
    datos.update(extras)
    return datos


class PropietarioFormTests(TestCase):
    def test_alta_crea_cuenta_hasheada_y_puede_entrar(self):
        form = PropietarioForm(data=datos_propietario())
        self.assertTrue(form.is_valid(), form.errors)
        propietario = form.save()

        cuenta = propietario.user
        self.assertIsNotNone(cuenta)
        self.assertEqual(cuenta.role, 'propietario')
        self.assertEqual(cuenta.status, 'active')
        self.assertTrue(cuenta.is_active)
        # Nunca queda la contraseña en texto plano en la base de datos.
        self.assertNotEqual(cuenta.password, CLAVE)
        self.assertTrue(cuenta.check_password(CLAVE))
        self.assertIsNotNone(authenticate(email='mario@test.com', password=CLAVE))

    def test_alta_requiere_password(self):
        form = PropietarioForm(data=datos_propietario(password='', password_confirmation=''))
        self.assertFalse(form.is_valid())
        self.assertIn('password', form.errors)

    def test_alta_rechaza_passwords_que_no_coinciden(self):
        form = PropietarioForm(data=datos_propietario(password_confirmation='OtraClave123!'))
        self.assertFalse(form.is_valid())
        self.assertIn('password_confirmation', form.errors)

    def test_alta_rechaza_email_ya_registrado(self):
        User.objects.create_user(email='mario@test.com', password='OtraClave123!')
        form = PropietarioForm(data=datos_propietario())
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_edicion_sin_password_conserva_la_actual(self):
        form = PropietarioForm(data=datos_propietario())
        propietario = form.save()
        cuenta = propietario.user

        datos = datos_propietario()
        del datos['password']
        del datos['password_confirmation']
        datos['full_name'] = 'Mario Lopez Actualizado'

        form_edicion = PropietarioForm(data=datos, instance=propietario)
        self.assertTrue(form_edicion.is_valid(), form_edicion.errors)
        propietario_editado = form_edicion.save()

        self.assertEqual(propietario_editado.user_id, cuenta.pk)
        self.assertTrue(cuenta.check_password(CLAVE))

    def test_edicion_con_password_la_cambia(self):
        form = PropietarioForm(data=datos_propietario())
        propietario = form.save()
        cuenta = propietario.user

        nueva = 'NuevaClave123!'
        datos = datos_propietario(password=nueva, password_confirmation=nueva)
        form_final = PropietarioForm(data=datos, instance=propietario)
        self.assertTrue(form_final.is_valid(), form_final.errors)
        form_final.save()

        cuenta.refresh_from_db()
        self.assertTrue(cuenta.check_password(nueva))
        self.assertFalse(cuenta.check_password(CLAVE))

    def test_serializadores_no_exponen_password(self):
        form = PropietarioForm(data=datos_propietario())
        propietario = form.save()

        self.assertNotIn('password', PropietarioSerializer(propietario).data)
        self.assertNotIn('password', UserSerializer(propietario.user).data)