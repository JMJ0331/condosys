from django.test import TestCase
from django.urls import reverse

from residencial.models import Residencial
from .models import Building, Garden


def crear_edificio(torre='Torre A'):
    jardin = Garden.objects.create(name='Jardín Central')
    return Building.objects.create(garden=jardin, name='Edificio 1', tower=torre)


def configurar_residencial(distribucion):
    return Residencial.objects.create(nombre='Residencial Rialto', distribucion=distribucion)


class DepartamentoDistribucionTests(TestCase):
    def test_modo_torres_muestra_solo_torre(self):
        crear_edificio()
        configurar_residencial('torres')
        respuesta = self.client.get(reverse('agregar_departamento'))
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, '>Torres</label>')
        self.assertContains(respuesta, 'Elegir torre')
        self.assertContains(respuesta, 'Torre A')
        self.assertNotContains(respuesta, 'id="torre-departamento"')
        self.assertNotContains(respuesta, '>Edificios</label>')

    def test_modo_edificios_muestra_solo_edificio(self):
        crear_edificio()
        configurar_residencial('edificios')
        respuesta = self.client.get(reverse('agregar_departamento'))
        self.assertContains(respuesta, '>Edificios</label>')
        self.assertContains(respuesta, 'Elegir edificio')
        self.assertNotContains(respuesta, 'id="torre-departamento"')

    def test_sin_configuracion_muestra_ambos(self):
        crear_edificio()
        respuesta = self.client.get(reverse('agregar_departamento'))
        self.assertContains(respuesta, '>Edificios</label>')
        self.assertContains(respuesta, 'Elegir edificio')
        self.assertContains(respuesta, 'id="torre-departamento"')

    def test_index_filtro_acorde_a_distribucion(self):
        crear_edificio()
        configurar_residencial('torres')
        respuesta = self.client.get(reverse('departamentos_index'))
        self.assertContains(respuesta, 'Todas las torres')
        self.assertNotContains(respuesta, 'Todos los edificios')

    def test_index_columnas_acorde_a_distribucion(self):
        crear_edificio()
        configurar_residencial('torres')
        respuesta = self.client.get(reverse('departamentos_index'))
        self.assertContains(respuesta, 'data-columna="torre"')
        self.assertNotContains(respuesta, 'data-columna="edificio"')
        Residencial.objects.update(distribucion='edificios')
        respuesta = self.client.get(reverse('departamentos_index'))
        self.assertContains(respuesta, 'data-columna="edificio"')
        self.assertNotContains(respuesta, 'data-columna="torre"')
