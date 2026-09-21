from datetime import date, time, timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone


class Command(BaseCommand):
    help = 'Carga 5 registros de ejemplo en cada sección completa (idempotente).'

    def handle(self, *args, **options):
        from accounts.models import User
        from structure.models import Garden, Building, Apartment
        from propietarios.models import Propietario
        from residents.models import Resident
        from payments.models import Payment
        from visitors.models import Visitor
        from incidents.models import Incident
        from maintenance.models import MaintenanceCharge
        from areas_comunes.models import AreaComun
        from reservations.models import CommonArea, Reservation
        from solicitudes.models import Solicitud
        from communications.models import Communication
        from notifications.models import Notification
        from chat.models import ChatGroup, ChatMessage

        ahora = timezone.now()
        hoy = timezone.localdate()

        with transaction.atomic():
            # ---------- Usuarios base (soporte de las FK) ----------
            usuarios_datos = [
                ('admin@condosys.do', 'Ana', 'Administradora', 'admin', '809-555-0101', '402-0000001-1'),
                ('gestion@condosys.do', 'Luis', 'Gestor', 'manager', '809-555-0102', '402-0000002-1'),
                ('residente1@condosys.do', 'María', 'Pérez', 'resident', '809-555-0111', '402-0000011-1'),
                ('residente2@condosys.do', 'Carlos', 'Gómez', 'resident', '809-555-0112', '402-0000012-1'),
                ('residente3@condosys.do', 'Laura', 'Fernández', 'resident', '809-555-0113', '402-0000013-1'),
                ('residente4@condosys.do', 'Pedro', 'Martínez', 'resident', '809-555-0114', '402-0000014-1'),
                ('residente5@condosys.do', 'Sofía', 'Ramírez', 'resident', '809-555-0115', '402-0000015-1'),
            ]
            usuarios = []
            for email, nombre, apellido, rol, telefono, documento in usuarios_datos:
                usuario, creado = User.objects.update_or_create(
                    email=email,
                    defaults={
                        'first_name': nombre,
                        'last_name': apellido,
                        'role': rol,
                        'status': 'active',
                        'phone': telefono,
                        'document': documento,
                        'is_active': True,
                    },
                )
                if creado:
                    usuario.set_password('Condosys123*')
                    usuario.save()
                usuarios.append(usuario)
            admin, gestor = usuarios[0], usuarios[1]
            usuarios_residentes = usuarios[2:]

            # ---------- Estructura: 5 jardines, 5 edificios, 5 apartamentos ----------
            jardines_datos = [
                ('Jardín Las Flores', 'Av. Las Américas Km 3'),
                ('Jardín Los Pinos', 'Calle Los Pinos #12'),
                ('Jardín El Roble', 'Av. El Roble #45'),
                ('Jardín Las Palmas', 'Calle Las Palmas #8'),
                ('Jardín El Mirador', 'Av. El Mirador #101'),
            ]
            jardines = [
                Garden.objects.update_or_create(
                    name=nombre,
                    defaults={'location': ubicacion, 'is_active': True},
                )[0]
                for nombre, ubicacion in jardines_datos
            ]

            edificios_datos = [
                ('Torre A', 'A', 'Bloque 1', 10),
                ('Torre B', 'B', 'Bloque 1', 8),
                ('Edificio C', 'C', 'Bloque 2', 5),
                ('Edificio D', 'D', 'Bloque 2', 6),
                ('Torre E', 'E', 'Bloque 3', 12),
            ]
            edificios = []
            for i, (nombre, torre, bloque, pisos) in enumerate(edificios_datos):
                edificio, _ = Building.objects.update_or_create(
                    garden=jardines[i], name=nombre,
                    defaults={'tower': torre, 'block': bloque,
                              'number_of_floors': pisos, 'is_active': True},
                )
                edificios.append(edificio)

            # ---------- Propietarios (5) ----------
            propietarios_datos = [
                ('María Pérez', '402-0000011-1', '809-555-0111', 'residente1@condosys.do'),
                ('Carlos Gómez', '402-0000012-1', '809-555-0112', 'residente2@condosys.do'),
                ('Laura Fernández', '402-0000013-1', '809-555-0113', 'residente3@condosys.do'),
                ('Pedro Martínez', '402-0000014-1', '809-555-0114', 'residente4@condosys.do'),
                ('Sofía Ramírez', '402-0000015-1', '809-555-0115', 'residente5@condosys.do'),
            ]
            propietarios = []
            for i, (nombre, cedula, telefono, email) in enumerate(propietarios_datos):
                propietario, _ = Propietario.objects.update_or_create(
                    cedula=cedula,
                    defaults={'full_name': nombre, 'phone': telefono,
                              'email': email, 'user': usuarios_residentes[i],
                              'is_active': True},
                )
                propietarios.append(propietario)

            # ---------- Apartamentos (5) ----------
            apartamentos_datos = [
                ('A-101', 1, 'occupied'), ('B-202', 2, 'occupied'),
                ('C-301', 3, 'occupied'), ('D-102', 1, 'occupied'),
                ('E-501', 5, 'maintenance'),
            ]
            apartamentos = []
            for i, (nombre, piso, estado) in enumerate(apartamentos_datos):
                apartamento, _ = Apartment.objects.update_or_create(
                    building=edificios[i], name=nombre,
                    defaults={'floor': piso, 'status': estado,
                              'owner': propietarios[i], 'is_active': True},
                )
                apartamentos.append(apartamento)

            # ---------- Residentes (5) ----------
            residentes_datos = [
                ('María Pérez', '402-0000011-1', 'propietario'),
                ('Carlos Gómez', '402-0000012-1', 'propietario'),
                ('Laura Fernández', '402-0000013-1', 'inquilino'),
                ('Pedro Martínez', '402-0000014-1', 'familiar'),
                ('Sofía Ramírez', '402-0000015-1', 'inquilino'),
            ]
            residentes = []
            for i, (nombre, cedula, relacion) in enumerate(residentes_datos):
                residente, _ = Resident.objects.update_or_create(
                    cedula=cedula,
                    defaults={'full_name': nombre, 'apartment': apartamentos[i],
                              'user': usuarios_residentes[i],
                              'phone': f'809-555-01{i + 11}',
                              'email': f'residente{i + 1}@condosys.do',
                              'tipo_relacion': relacion,
                              'fecha_ingreso': hoy - timedelta(days=30 * (i + 1)),
                              'is_active': True},
                )
                residentes.append(residente)

            # ---------- Cargos de mantenimiento (5) ----------
            cargos_datos = [
                ('maintenance', 'monthly', Decimal('2500.00'), 'cash'),
                ('security', 'monthly', Decimal('1200.00'), 'transfer'),
                ('cleaning', 'monthly', Decimal('800.00'), 'cash'),
                ('reserve_fund', 'quarterly', Decimal('5000.00'), 'transfer'),
                ('water', 'monthly', Decimal('600.00'), 'online'),
            ]
            for concepto, periodicidad, monto, metodo in cargos_datos:
                MaintenanceCharge.objects.update_or_create(
                    concept=concepto, periodicity=periodicidad, amount=monto,
                    defaults={'payment_methods': metodo,
                              'effective_date': hoy.replace(day=1),
                              'is_active': True},
                )

            # ---------- Pagos (5) ----------
            pagos_datos = [
                (0, Decimal('2500.00'), 'maintenance', 'paid', 'transfer'),
                (1, Decimal('2500.00'), 'maintenance', 'pending', None),
                (2, Decimal('1200.00'), 'services', 'overdue', None),
                (3, Decimal('800.00'), 'parking', 'paid', 'cash'),
                (4, Decimal('5000.00'), 'extraordinary', 'pending', None),
            ]
            for i, (idx, monto, concepto, estado, metodo) in enumerate(pagos_datos):
                periodo = (hoy.replace(day=1) - timedelta(days=30 * (4 - i))).replace(day=1)
                Payment.objects.update_or_create(
                    apartment=apartamentos[idx], resident=residentes[idx],
                    period=periodo, concept=concepto,
                    defaults={'amount': monto, 'status': estado,
                              'payment_method': metodo,
                              'payment_date': hoy if estado == 'paid' else None,
                              'registered_by': gestor},
                )

            # ---------- Visitantes (5) ----------
            visitantes_datos = [
                ('Juan Pérez', 'family', 'authorized', 0),
                ('Mensajero Express', 'delivery', 'completed', 1),
                ('Técnico Claro', 'technician', 'authorized', 2),
                ('Ana Lucía', 'family', 'pending', 3),
                ('Proveedor Limpieza', 'provider', 'completed', 4),
            ]
            for i, (nombre, tipo, estado, idx) in enumerate(visitantes_datos):
                entrada = ahora - timedelta(days=4 - i, hours=2)
                Visitor.objects.update_or_create(
                    name=nombre, apartment=apartamentos[idx],
                    scheduled_entry=entrada,
                    defaults={'type': tipo, 'status': estado,
                              'scheduled_exit': entrada + timedelta(hours=3),
                              'actual_entry': entrada if estado in ('authorized', 'completed') else None,
                              'actual_exit': entrada + timedelta(hours=2) if estado == 'completed' else None,
                              'reason': f'Visita de ejemplo #{i + 1}',
                              'registered_by': gestor},
                )

            # ---------- Incidencias (5) ----------
            incidencias_datos = [
                ('Fuga de agua en baño', 'plumbing', 'high', 'in_progress', 0),
                ('Corto circuito pasillo', 'electricity', 'urgent', 'new', 1),
                ('Ruido excesivo nocturno', 'noise', 'normal', 'assigned', 2),
                ('Limpieza de escaleras', 'cleaning', 'low', 'resolved', 3),
                ('Puerta principal dañada', 'security', 'high', 'new', 4),
            ]
            for titulo, categoria, prioridad, estado, idx in incidencias_datos:
                Incident.objects.update_or_create(
                    title=titulo, apartment=apartamentos[idx],
                    defaults={'category': categoria, 'priority': prioridad,
                              'status': estado,
                              'description': f'{titulo}. Reporte de ejemplo.',
                              'resident': residentes[idx], 'reported_by': usuarios_residentes[idx]},
                )

            # ---------- Áreas comunes (5) ----------
            areas_datos = [
                ('Gazebo Central', 'gazebo', 30, time(8, 0), time(22, 0), 'todos'),
                ('Salón de Eventos', 'salon_eventos', 100, time(9, 0), time(23, 0), 'todos'),
                ('Piscina Principal', 'piscina', 50, time(7, 0), time(19, 0), 'todos'),
                ('Cancha Deportiva', 'cancha_deportiva', 22, time(6, 0), time(21, 0), 'lun_vie'),
                ('Gimnasio', 'gimnasio', 20, time(5, 0), time(22, 0), 'todos'),
            ]
            areas = []
            for nombre, tipo, capacidad, desde, hasta, dias in areas_datos:
                area, _ = AreaComun.objects.update_or_create(
                    name=nombre,
                    defaults={'area_type': tipo, 'capacity': capacidad,
                              'available_from': desde, 'available_until': hasta,
                              'available_days': dias, 'status': 'activo'},
                )
                areas.append(area)
                CommonArea.objects.update_or_create(
                    garden=jardines[0], name=nombre,
                    defaults={'description': f'{nombre} de ejemplo.',
                              'capacity': capacidad, 'is_active': True},
                )

            # ---------- Reservas (5) ----------
            estados_reserva = ['approved', 'requested', 'completed', 'approved', 'requested']
            for i in range(5):
                inicio_r = (ahora + timedelta(days=i + 1)).replace(hour=15, minute=0, second=0, microsecond=0)
                fin_r = inicio_r + timedelta(hours=3)
                Reservation.objects.update_or_create(
                    common_area=areas[i], start_time=inicio_r, end_time=fin_r,
                    defaults={'apartment': apartamentos[i], 'resident': residentes[i],
                              'reserved_by': usuarios_residentes[i],
                              'reason': f'Evento familiar #{i + 1}',
                              'expected_guests': 10 * (i + 1),
                              'status': estados_reserva[i]},
                )

            # ---------- Solicitudes (5) ----------
            solicitudes_datos = [
                ('certificado', 'pendiente', 0),
                ('permiso', 'en_proceso', 1),
                ('mantenimiento', 'aprobada', 2),
                ('instalacion', 'pendiente', 3),
                ('reparacion', 'completada', 4),
            ]
            tipos_desc = {
                'certificado': 'Certificado de residencia para trámite bancario.',
                'permiso': 'Permiso para mudanza el fin de semana.',
                'mantenimiento': 'Mantenimiento de aire acondicionado.',
                'instalacion': 'Instalación de internet en el apartamento.',
                'reparacion': 'Reparación de cerradura principal.',
            }
            for tipo, estado, idx in solicitudes_datos:
                Solicitud.objects.update_or_create(
                    apartment=apartamentos[idx], resident=residentes[idx],
                    request_type=tipo, description=tipos_desc[tipo],
                    defaults={'status': estado, 'request_date': hoy - timedelta(days=idx)},
                )

            # ---------- Comunicados (5) ----------
            comunicados_datos = [
                ('Corte de agua programado', 'mantenimiento'),
                ('Fiesta de fin de año', 'evento'),
                ('Refuerzo de seguridad nocturna', 'seguridad'),
                ('Horario de piscina en feriado', 'piscinas'),
                ('Asamblea general de vecinos', 'aviso'),
            ]
            for titulo, categoria in comunicados_datos:
                Communication.objects.update_or_create(
                    title=titulo, garden=jardines[0],
                    defaults={'category': categoria,
                              'body': f'{titulo}. Comunicado de ejemplo.',
                              'sender': gestor, 'target_type': 'general',
                              'is_published': True, 'published_at': ahora},
                )

            # ---------- Notificaciones (5) ----------
            notificaciones_datos = [
                ('payment_due', 'Pago próximo a vencer', 'Tu cuota de mantenimiento vence pronto.'),
                ('payment_overdue', 'Pago vencido', 'Tienes un pago vencido pendiente.'),
                ('reservation_approved', 'Reserva aprobada', 'Tu reserva fue aprobada.'),
                ('incident_updated', 'Incidencia actualizada', 'Tu incidencia cambió de estado.'),
                ('general', 'Aviso general', 'Recuerda la asamblea de vecinos.'),
            ]
            for i, (tipo, titulo, mensaje) in enumerate(notificaciones_datos):
                Notification.objects.update_or_create(
                    user=usuarios_residentes[i], type=tipo, title=titulo,
                    defaults={'message': mensaje, 'is_read': False},
                )

            # ---------- Chat (5 mensajes) ----------
            grupo, _ = ChatGroup.objects.get_or_create(name='Vecinos General')
            mensajes_chat = [
                (0, 1, 'Hola vecinos, ¿cómo están?'),
                (1, 0, 'Todo bien por aquí.'),
                (2, None, 'Recuerden la reunión de mañana.'),
                (3, 4, '¿Alguien tiene un taladro que me preste?'),
                (4, 3, 'Yo te lo presto sin problema.'),
            ]
            for remitente, destino, texto in mensajes_chat:
                ChatMessage.objects.get_or_create(
                    sender=usuarios_residentes[remitente],
                    receiver=usuarios_residentes[destino] if destino is not None else None,
                    group=grupo if destino is None else None,
                    message=texto,
                )

        self.stdout.write(self.style.SUCCESS('Datos de ejemplo cargados: 5 por cada sección completa.'))
