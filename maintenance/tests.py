from django.test import TestCase
from django.urls import reverse

from residents.models import Resident
from structure.models import Apartment, Building, Garden

from .models import MaintenanceCharge


def crear_base():
    jardin = Garden.objects.create(name='Jardín Central')
    edificio = Building.objects.create(garden=jardin, name='Torre A')
    apartamento = Apartment.objects.create(building=edificio, name='A-102')
    return apartamento


def crear_cargo(apartamento=None):
    return MaintenanceCharge.objects.create(
        concept='maintenance', periodicity='monthly',
        amount=15000, apartment=apartamento,
        effective_date='2026-09-01', is_active=True,
    )


class MantenimientosViewTests(TestCase):
    def test_index_muestra_cuadricula(self):
        crear_cargo(crear_base())
        crear_cargo()
        respuesta = self.client.get(reverse('mantenimientos_index'))
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, 'Todos los mantenimientos')
        self.assertContains(respuesta, 'Mantenimiento')
        self.assertContains(respuesta, 'A-102')
        self.assertContains(respuesta, 'Todos')

    def test_agregar_crea_cargo(self):
        apartamento = crear_base()
        respuesta = self.client.post(reverse('agregar_mantenimiento'), {
            'concept': 'cleaning',
            'periodicity': 'monthly',
            'amount': '5000',
            'apartment': str(apartamento.id),
            'effective_date': '2026-09-01',
            'is_active': 'on',
        })
        self.assertEqual(respuesta.status_code, 302)
        cargo = MaintenanceCharge.objects.get()
        self.assertEqual(cargo.apartment, apartamento)
        self.assertTrue(cargo.is_active)

    def test_actualizar_modifica_cargo(self):
        cargo = crear_cargo()
        respuesta = self.client.post(
            reverse('actualizar_mantenimiento', args=[str(cargo.id)]),
            {
                'concept': 'water',
                'periodicity': 'annual',
                'amount': '12000',
                'apartment': '',
                'effective_date': '2026-10-01',
            },
        )
        self.assertEqual(respuesta.status_code, 302)
        cargo.refresh_from_db()
        self.assertEqual(cargo.concept, 'water')
        self.assertFalse(cargo.is_active)

    def test_eliminar_borra_cargo(self):
        cargo = crear_cargo()
        respuesta = self.client.post(reverse('eliminar_mantenimiento', args=[str(cargo.id)]))
        self.assertEqual(respuesta.status_code, 302)
        self.assertEqual(MaintenanceCharge.objects.count(), 0)

    def test_filtra_por_estado_mes_anio_departamento(self):
        apartamento = crear_base()
        crear_cargo(apartamento)
        inactivo = MaintenanceCharge.objects.create(
            concept='water', periodicity='annual', amount=12000,
            effective_date='2025-01-15', is_active=False,
        )
        respuesta = self.client.get(reverse('mantenimientos_index'), {'estado': 'inactivo'})
        self.assertContains(respuesta, 'Agua')
        self.assertNotContains(respuesta, '01/09/2026')
        respuesta = self.client.get(reverse('mantenimientos_index'), {'mes': '9', 'anio': '2026'})
        self.assertContains(respuesta, '01/09/2026')
        self.assertNotContains(respuesta, '15/01/2025')
        respuesta = self.client.get(
            reverse('mantenimientos_index'), {'apartamento': str(apartamento.id)}
        )
        self.assertContains(respuesta, '01/09/2026')
        self.assertNotContains(respuesta, '15/01/2025')

    def test_filtros_y_columnas_presentes(self):
        crear_cargo()
        respuesta = self.client.get(reverse('mantenimientos_index'))
        self.assertContains(respuesta, 'Todas las columnas')
        self.assertContains(respuesta, 'Todos los estados')
        self.assertContains(respuesta, 'Todos los departamentos')
        self.assertContains(respuesta, 'Todos los meses')
        self.assertContains(respuesta, 'Todos los años')
