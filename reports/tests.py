from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from structure.models import Apartment, Building, Garden
from residents.models import Resident
from payments.models import Payment


def crear_base():
    jardin = Garden.objects.create(name='Jardín Central')
    edificio = Building.objects.create(garden=jardin, name='Torre A')
    apartamento = Apartment.objects.create(building=edificio, name='A-102', status='occupied')
    residente = Resident.objects.create(
        apartment=apartamento, full_name='Juan Perez',
        cedula='001-1234567-8', phone='809-000-0000',
    )
    return {'edificio': edificio, 'apartamento': apartamento, 'residente': residente}


class ReportesViewTests(TestCase):
    def test_index_muestra_kpis_y_generador(self):
        respuesta = self.client.get(reverse('reportes_index'))
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, 'Generar reporte')
        self.assertContains(respuesta, 'Ingresos del mes')
        self.assertContains(respuesta, 'Reportes disponibles')
        self.assertContains(respuesta, 'Vista previa')

    def test_tipos_requisito_presentes(self):
        respuesta = self.client.get(reverse('reportes_index'))
        for etiqueta in [
            'Apartamentos ocupados / disponibles',
            'Residentes activos',
            'Pagos realizados',
            'Pagos pendientes',
            'Morosidad',
            'Incidencias por estado',
            'Visitas registradas',
            'Reservas de áreas comunes',
            'Ingresos mensuales',
        ]:
            self.assertContains(respuesta, etiqueta)

    def test_tipo_invalido_usa_ingresos(self):
        respuesta = self.client.get(reverse('reportes_index'), {'tipo': 'inexistente'})
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, 'Últimos 7 meses')

    def test_exportar_csv(self):
        respuesta = self.client.get(reverse('reportes_index'), {'tipo': 'residentes', 'formato': 'csv'})
        self.assertEqual(respuesta.status_code, 200)
        self.assertIn('text/csv', respuesta['Content-Type'])
        self.assertIn('reporte-residentes.csv', respuesta['Content-Disposition'])

    def test_reporte_pagos_con_datos(self):
        base = crear_base()
        hoy = timezone.localdate()
        Payment.objects.create(
            apartment=base['apartamento'], resident=base['residente'],
            amount=2500, concept='maintenance', period=hoy.replace(day=1),
            payment_date=hoy, status='paid',
        )
        respuesta = self.client.get(reverse('reportes_index'), {'tipo': 'pagos_realizados'})
        self.assertContains(respuesta, 'Juan Perez')
        respuesta = self.client.get(reverse('reportes_index'), {'tipo': 'ingresos'})
        self.assertContains(respuesta, 'Pagos recibidos')

    def test_filtro_edificio_y_rango(self):
        base = crear_base()
        respuesta = self.client.get(reverse('reportes_index'), {
            'tipo': 'apartamentos',
            'edificio': str(base['edificio'].id),
            'desde': '2026-01-01',
            'hasta': '2026-12-31',
        })
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, 'A-102')
