from datetime import date

from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from incidents.models import Incident
from payments.models import Payment
from reservations.models import Reservation
from residents.models import Resident
from structure.models import Apartment, Building, Garden


def crear_estructura(nombre='A-102'):
    jardin = Garden.objects.create(name='Jardín Central')
    edificio = Building.objects.create(garden=jardin, name='Torre A', tower='Torre A')
    return Apartment.objects.create(building=edificio, name=nombre)


def crear_residente(apartamento, nombre='Juan Perez', cedula='001-1234567-8'):
    return Resident.objects.create(
        apartment=apartamento,
        full_name=nombre,
        cedula=cedula,
        phone='809-000-0000',
    )


def crear_usuario(email='admin@test.com', role='admin'):
    return User.objects.create_user(
        email=email, password='Clave12345', role=role, status='active',
    )


class InicioViewTests(TestCase):
    def test_muestra_tarjetas_y_paneles(self):
        respuesta = self.client.get(reverse('inicio'))
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, 'Inicio')
        self.assertContains(respuesta, 'Departamentos')
        self.assertContains(respuesta, 'Incidencias abiertas')
        self.assertContains(respuesta, 'Pagos pendientes')
        self.assertContains(respuesta, 'Reservas pendientes')
        self.assertContains(respuesta, 'Pagos pendientes por vencer')
        self.assertContains(respuesta, 'Acciones Rápidas')
        self.assertContains(respuesta, 'Actividad Reciente')

    def test_tabla_pagos_pendientes_por_vencer(self):
        apartamento = crear_estructura()
        residente = crear_residente(apartamento)
        Payment.objects.create(
            apartment=apartamento, resident=residente,
            amount=1500, concept='maintenance', period=date(2026, 9, 1),
            status='pending',
        )
        Payment.objects.create(
            apartment=apartamento, resident=residente,
            amount=2000, concept='maintenance', period=date(2026, 10, 1),
            status='paid',
        )
        respuesta = self.client.get(reverse('inicio'))
        self.assertContains(respuesta, 'Juan Perez')
        self.assertContains(respuesta, 'A-102')
        self.assertContains(respuesta, 'Pendiente')
        # El pagado no sale en pendientes (solo aparece su periodo en otra fila si existiera).
        self.assertNotContains(respuesta, 'Pagado')
        self.assertContains(respuesta, '/pagos/?estado=pending')

    def test_tarjeta_aprobar_reservas(self):
        respuesta = self.client.get(reverse('inicio'))
        self.assertContains(respuesta, 'Aprobar reservas (0 pendientes)')
        self.assertContains(respuesta, reverse('reservas_index'))

    def test_actividad_reciente_con_pago_e_incidencia(self):
        apartamento = crear_estructura()
        residente = crear_residente(apartamento)
        usuario = crear_usuario()
        Payment.objects.create(
            apartment=apartamento, resident=residente,
            amount=1500, concept='maintenance', period=date(2026, 9, 1),
            registered_by=usuario,
        )
        Incident.objects.create(
            apartment=apartamento, reported_by=usuario,
            category='plumbing', title='Fuga de agua',
            description='Fuga en el baño.',
        )
        respuesta = self.client.get(reverse('inicio'))
        self.assertContains(respuesta, 'Juan Perez registró un pago.')
        self.assertContains(respuesta, 'Nueva incidencia reportada en')
        self.assertContains(respuesta, '/actividad/')

    def test_acciones_rapidas_apuntan_a_crear(self):
        respuesta = self.client.get(reverse('inicio'))
        self.assertContains(respuesta, reverse('agregar_pago'))
        self.assertContains(respuesta, reverse('crear_visitante'))
        self.assertContains(respuesta, reverse('crear_incidencia'))
        self.assertContains(respuesta, reverse('crear_comunicacion'))

    def test_conteos_reales(self):
        apartamento = crear_estructura()
        crear_residente(apartamento)
        usuario = crear_usuario()
        Incident.objects.create(
            apartment=apartamento, reported_by=usuario,
            category='plumbing', title='Fuga', description='Fuga.',
            status='new',
        )
        respuesta = self.client.get(reverse('inicio'))
        contexto = respuesta.context
        self.assertEqual(contexto['total_departamentos'], 1)
        self.assertEqual(contexto['incidencias_abiertas'], 1)
        self.assertEqual(contexto['reservas_pendientes'], 0)
