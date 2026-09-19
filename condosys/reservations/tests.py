from datetime import date, time

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from accounts.models import User
from areas_comunes.models import AreaComun
from residents.models import Resident
from structure.models import Apartment, Building, Garden

from .models import Reservation


def crear_base():
    jardin = Garden.objects.create(name='Jardín Central')
    edificio = Building.objects.create(garden=jardin, name='Torre A')
    apartamento = Apartment.objects.create(building=edificio, name='A-102')
    residente = Resident.objects.create(
        apartment=apartamento, full_name='Juan Perez',
        cedula='001-1234567-8', phone='809-000-0000',
    )
    usuario = User.objects.create_user(
        email='admin@test.com', password='Clave12345',
        role='admin', status='active',
    )
    area = AreaComun.objects.create(
        name='Salón de eventos', area_type='salon_eventos',
        available_days='todos', status='activo',
    )
    return {'apartamento': apartamento, 'residente': residente, 'usuario': usuario, 'area': area}


def crear_reserva(base):
    inicio = timezone.make_aware(timezone.datetime(2026, 9, 20, 10, 0))
    fin = timezone.make_aware(timezone.datetime(2026, 9, 20, 12, 0))
    return Reservation.objects.create(
        common_area=base['area'], apartment=base['apartamento'],
        resident=base['residente'], reserved_by=base['usuario'],
        start_time=inicio, end_time=fin, status='requested',
    )


class ReservasViewTests(TestCase):
    def test_index_muestra_cuadricula(self):
        base = crear_base()
        crear_reserva(base)
        respuesta = self.client.get(reverse('reservas_index'))
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, 'Todas las reservas')
        self.assertContains(respuesta, 'Juan Perez')
        self.assertContains(respuesta, 'Salón de eventos')
        self.assertContains(respuesta, 'A-102')
        self.assertContains(respuesta, 'Solicitada')

    def test_agregar_crea_reserva(self):
        base = crear_base()
        respuesta = self.client.post(reverse('agregar_reserva'), {
            'common_area': str(base['area'].id),
            'apartment': str(base['apartamento'].id),
            'resident': str(base['residente'].id),
            'reserved_by': str(base['usuario'].id),
            'status': 'requested',
            'fecha_reserva': '2026-09-20',
            'hora_inicio': '10:00',
            'hora_fin': '12:00',
        })
        self.assertEqual(respuesta.status_code, 302)
        self.assertEqual(Reservation.objects.count(), 1)

    def test_actualizar_modifica_estado(self):
        base = crear_base()
        reserva = crear_reserva(base)
        respuesta = self.client.post(
            reverse('actualizar_reserva', args=[str(reserva.id)]),
            {
                'common_area': str(base['area'].id),
                'apartment': str(base['apartamento'].id),
                'resident': str(base['residente'].id),
                'reserved_by': str(base['usuario'].id),
                'status': 'approved',
                'fecha_reserva': '2026-09-20',
                'hora_inicio': '10:00',
                'hora_fin': '12:00',
            },
        )
        self.assertEqual(respuesta.status_code, 302)
        reserva.refresh_from_db()
        self.assertEqual(reserva.status, 'approved')

    def test_actualizar_precarga_fecha_y_hora(self):
        base = crear_base()
        reserva = crear_reserva(base)
        respuesta = self.client.get(reverse('actualizar_reserva', args=[str(reserva.id)]))
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, 'Actualizar reserva')

    def test_eliminar_borra_reserva(self):
        base = crear_base()
        reserva = crear_reserva(base)
        respuesta = self.client.post(reverse('eliminar_reserva', args=[str(reserva.id)]))
        self.assertEqual(respuesta.status_code, 302)
        self.assertEqual(Reservation.objects.count(), 0)
