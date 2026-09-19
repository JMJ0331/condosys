from django.test import TestCase
from django.urls import reverse

from accounts.models import User

from .models import Residencial


def crear_usuario(email, role):
    return User.objects.create_user(
        email=email,
        password='Clave12345',
        role=role,
        status='active',
    )


DATOS_VALIDOS = {
    'nombre': 'Residencial Rialto',
    'rnc': '131-12345-1',
    'nombre_via': 'Calle Central',
    'numero_edificacion': 'No. 15',
    'sector': 'Bella Vista',
    'codigo_postal': '10112',
    'municipio': 'Santo Domingo de Guzmán',
    'provincia': 'Distrito Nacional',
    'mapa_iframe': '<iframe src="https://maps.google.com"></iframe>',
    'distribucion': 'torres',
    'cantidad_edificios': 12,
    'cantidad_pisos': 8,
    'telefono': '809-000-0000',
    'correo': 'residencial@gmail.com',
}


class ResidencialViewTests(TestCase):
    # TEMP pruebas: login deshabilitado, el anónimo puede ver y guardar.
    def test_anonimo_puede_ver_y_guardar(self):
        respuesta = self.client.get(reverse('residencial_index'))
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, 'Nombre del residencial')
        respuesta = self.client.post(reverse('residencial_index'), DATOS_VALIDOS)
        self.assertEqual(respuesta.status_code, 302)
        self.assertEqual(Residencial.objects.count(), 1)

    def test_get_muestra_formulario(self):
        crear_usuario('admin@test.com', 'admin')
        self.client.force_login(User.objects.get(email='admin@test.com'))
        respuesta = self.client.get(reverse('residencial_index'))
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, 'Nombre del residencial')
        self.assertContains(respuesta, 'Agregar')

    def test_post_crea_registro_unico(self):
        crear_usuario('manager@test.com', 'manager')
        self.client.force_login(User.objects.get(email='manager@test.com'))
        respuesta = self.client.post(reverse('residencial_index'), DATOS_VALIDOS)
        self.assertEqual(respuesta.status_code, 302)
        self.assertEqual(Residencial.objects.count(), 1)
        self.assertEqual(Residencial.objects.first().nombre, 'Residencial Rialto')

    def test_segundo_post_actualiza_sin_duplicar(self):
        crear_usuario('admin@test.com', 'admin')
        self.client.force_login(User.objects.get(email='admin@test.com'))
        self.client.post(reverse('residencial_index'), DATOS_VALIDOS)
        datos = dict(DATOS_VALIDOS, nombre='Residencial Actualizado')
        self.client.post(reverse('residencial_index'), datos)
        self.assertEqual(Residencial.objects.count(), 1)
        self.assertEqual(Residencial.objects.first().nombre, 'Residencial Actualizado')
        respuesta = self.client.get(reverse('residencial_index'))
        self.assertContains(respuesta, 'Actualizar')

    def test_residente_no_puede_guardar(self):
        crear_usuario('vecino@test.com', 'resident')
        self.client.force_login(User.objects.get(email='vecino@test.com'))
        respuesta = self.client.post(reverse('residencial_index'), DATOS_VALIDOS)
        self.assertEqual(respuesta.status_code, 302)
        self.assertEqual(Residencial.objects.count(), 0)

    def test_distribucion_solo_torres_y_edificios(self):
        from .forms import ResidencialForm

        opciones = [valor for valor, _ in ResidencialForm().fields['distribucion'].choices if valor]
        self.assertEqual(opciones, ['torres', 'edificios'])
