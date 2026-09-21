from django.test import TestCase
from django.urls import reverse

from payments.models import Payment
from residents.models import Resident
from structure.models import Apartment, Building, Garden


def crear_pago(apartamento, residente, periodo):
    return Payment.objects.create(
        apartment=apartamento, resident=residente,
        amount=1500, concept='maintenance', period=periodo,
    )


class PagosFiltroMesAnioTests(TestCase):
    def setUp(self):
        jardin = Garden.objects.create(name='Jardín Central')
        edificio = Building.objects.create(garden=jardin, name='Torre A')
        self.apartamento = Apartment.objects.create(building=edificio, name='A-102')
        self.residente = Resident.objects.create(
            apartment=self.apartamento, full_name='Juan Perez',
            cedula='001-1234567-8', phone='809-000-0000',
        )
        crear_pago(self.apartamento, self.residente, '2026-09-01')
        crear_pago(self.apartamento, self.residente, '2025-09-01')

    def test_filtra_por_mes(self):
        respuesta = self.client.get(reverse('pagos_index'), {'mes': '9'})
        self.assertContains(respuesta, '2026')
        respuesta = self.client.get(reverse('pagos_index'), {'mes': '1'})
        self.assertNotContains(respuesta, 'Juan Perez')

    def test_filtra_por_anio(self):
        respuesta = self.client.get(reverse('pagos_index'), {'anio': '2026'})
        self.assertContains(respuesta, '01/09/2026')
        self.assertNotContains(respuesta, '01/09/2025')
        respuesta = self.client.get(reverse('pagos_index'), {'anio': '2025'})
        self.assertContains(respuesta, '01/09/2025')
        self.assertNotContains(respuesta, '01/09/2026')

    def test_filtra_por_mes_y_anio(self):
        respuesta = self.client.get(reverse('pagos_index'), {'mes': '9', 'anio': '2026'})
        self.assertContains(respuesta, '01/09/2026')

    def test_mes_invalido_no_filtra(self):
        respuesta = self.client.get(reverse('pagos_index'), {'mes': '13'})
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, 'Juan Perez')

    def test_selects_presentes(self):
        respuesta = self.client.get(reverse('pagos_index'))
        self.assertContains(respuesta, 'Todos los meses')
        self.assertContains(respuesta, 'Todos los años')
        self.assertContains(respuesta, 'id="panel-mes"')
        self.assertContains(respuesta, 'id="panel-anio"')
        self.assertContains(respuesta, 'data-mes="9"')
        respuesta = self.client.get(reverse('pagos_index'), {'mes': '9'})
        self.assertContains(respuesta, 'Septiembre')
