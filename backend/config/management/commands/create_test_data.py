"""
Management command to create test data for development
python manage.py create_test_data
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from accounts.models import User
from structure.models import Garden, Building, Apartment
from residents.models import Resident
from payments.models import ChargeType, Payment
from incidents.models import Incident
from visitors.models import Visitor
from reservations.models import CommonArea, Reservation
from communications.models import Communication


class Command(BaseCommand):
    help = 'Create test data for development'

    def handle(self, *args, **options):
        self.stdout.write('🌱 Creando datos de prueba...\n')
        
        # 1. Create Garden
        garden, created = Garden.objects.get_or_create(
            name='Conjunto Residencial Condosys',
            defaults={
                'location': 'Bogotá D.C., Colombia',
                'description': 'Conjunto residencial de prueba',
                'is_active': True
            }
        )
        self.stdout.write(f'✓ Jardín: {garden.name}')
        
        # 2. Create Buildings
        buildings = []
        for i in range(1, 4):
            building, created = Building.objects.get_or_create(
                garden=garden,
                name=f'Edificio {i}',
                defaults={
                    'number_of_floors': 5 + i,
                    'description': f'Edificio residencial torre {i}',
                    'is_active': True
                }
            )
            buildings.append(building)
        self.stdout.write(f'✓ Edificios: {len(buildings)} creados')
        
        # 3. Create Apartments
        apartments = []
        for building in buildings:
            for floor in range(1, 6):
                for apt_num in range(1, 4):
                    apartment, created = Apartment.objects.get_or_create(
                        building=building,
                        number=f'{floor}{apt_num:02d}',
                        defaults={
                            'floor': floor,
                            'area_m2': 80 + (floor * 5),
                            'type': 'apartment',
                            'status': 'empty' if apt_num % 2 == 0 else 'occupied',
                            'is_active': True
                        }
                    )
                    apartments.append(apartment)
        self.stdout.write(f'✓ Departamentos: {len(apartments)} creados')
        
        # 4. Create Users with different roles
        users = []
        roles = ['admin', 'manager', 'resident', 'maintenance', 'security']
        for idx, role in enumerate(roles):
            user, created = User.objects.get_or_create(
                email=f'{role}@condosys.com',
                defaults={
                    'first_name': role.capitalize(),
                    'last_name': 'Test',
                    'phone': f'+5712345678{idx}',
                    'document': f'123456{idx}',
                    'role': role,
                    'status': 'active',
                    'garden': garden if role in ['admin', 'manager'] else None,
                    'is_active': True
                }
            )
            if created:
                user.set_password('password123')
                user.save()
            users.append(user)
        self.stdout.write(f'✓ Usuarios: {len(users)} creados')
        
        # 5. Create Residents
        residents_count = 0
        for apartment in apartments[:15]:  # Solo primeros 15 apts
            user, _ = User.objects.get_or_create(
                email=f'resident{residents_count}@condosys.com',
                defaults={
                    'first_name': f'Residente',
                    'last_name': f'{residents_count}',
                    'phone': f'+5719999{residents_count:04d}',
                    'document': f'999999{residents_count:02d}',
                    'role': 'resident',
                    'status': 'active',
                    'is_active': True
                }
            )
            if not user.has_usable_password():
                user.set_password('password123')
                user.save()
            
            resident, created = Resident.objects.get_or_create(
                user=user,
                apartment=apartment,
                defaults={
                    'role_in_apartment': 'owner' if residents_count % 2 == 0 else 'occupant',
                    'move_in_date': timezone.now() - timedelta(days=180 + residents_count*10),
                    'emergency_contact': f'Contacto {residents_count}',
                    'emergency_phone': f'+5715555{residents_count:04d}',
                }
            )
            if created:
                residents_count += 1
        self.stdout.write(f'✓ Residentes: {residents_count} creados')
        
        # 6. Create ChargeTypes
        charge_types = ['Mantenimiento', 'Mora', 'Parqueo', 'Agua', 'Basura', 'Seguridad']
        for charge_name in charge_types:
            ChargeType.objects.get_or_create(
                name=charge_name,
                defaults={'is_active': True}
            )
        self.stdout.write(f'✓ Tipos de Cargos: {len(charge_types)} creados')
        
        # 7. Create Payments
        charge_types = ChargeType.objects.all()
        payments_count = 0
        for apartment in apartments[:10]:
            for charge in charge_types[:3]:
                payment, created = Payment.objects.get_or_create(
                    apartment=apartment,
                    charge_type=charge,
                    invoice_date=timezone.now() - timedelta(days=15),
                    defaults={
                        'amount': 250000.00 + (apartment.floor * 10000),
                        'due_date': timezone.now() + timedelta(days=15),
                        'status': 'pending',
                        'payment_method': 'transfer',
                        'description': f'{charge.name} - {apartment.number}'
                    }
                )
                if created:
                    payments_count += 1
        self.stdout.write(f'✓ Pagos: {payments_count} creados')
        
        # 8. Create Incidents
        categories = ['plumbing', 'electricity', 'cleaning', 'security', 'noise']
        incidents_count = 0
        for idx, apartment in enumerate(apartments[:5]):
            incident, created = Incident.objects.get_or_create(
                apartment=apartment,
                reported_by=users[2],  # resident user
                defaults={
                    'category': categories[idx % len(categories)],
                    'priority': 'normal',
                    'title': f'Problema de {categories[idx % len(categories)]}',
                    'description': f'Reporte de incidente #{idx+1}',
                    'status': 'new',
                    'assigned_to': users[3] if idx % 2 == 0 else None,
                }
            )
            if created:
                incidents_count += 1
        self.stdout.write(f'✓ Incidentes: {incidents_count} creados')
        
        # 9. Create CommonAreas
        areas = ['Salón Social', 'Piscina', 'Cancha Deportiva', 'Parque Infantil', 'Gimnasio']
        for area_name in areas:
            CommonArea.objects.get_or_create(
                garden=garden,
                name=area_name,
                defaults={
                    'capacity': 50 + (areas.index([a for a in areas if a == area_name][0]) * 20),
                    'description': f'Área común: {area_name}',
                    'is_active': True
                }
            )
        self.stdout.write(f'✓ Áreas Comunes: {len(areas)} creadas')
        
        # 10. Create Reservations
        common_areas = CommonArea.objects.all()
        reservations_count = 0
        for idx, area in enumerate(common_areas):
            for day_offset in [1, 2, 3]:
                reservation, created = Reservation.objects.get_or_create(
                    common_area=area,
                    reserved_by=users[2],
                    start_time=timezone.now() + timedelta(days=day_offset, hours=10),
                    end_time=timezone.now() + timedelta(days=day_offset, hours=12),
                    defaults={
                        'reason': f'Evento familiar {day_offset}',
                        'expected_guests': 20 + (day_offset * 5),
                        'status': 'requested',
                        'approved_by': users[1] if day_offset == 1 else None,
                    }
                )
                if created:
                    reservations_count += 1
        self.stdout.write(f'✓ Reservas: {reservations_count} creadas')
        
        # 11. Create Visitors
        visitors_count = 0
        for apartment in apartments[:3]:
            visitor, created = Visitor.objects.get_or_create(
                apartment=apartment,
                registered_by=users[2],  # resident
                name=f'Visitante {visitors_count}',
                document=f'88888{visitors_count:03d}',
                defaults={
                    'phone': f'+5717777{visitors_count:04d}',
                    'reason': 'Visita familiar',
                    'type': 'family',
                    'scheduled_entry': timezone.now() + timedelta(hours=2),
                    'scheduled_exit': timezone.now() + timedelta(hours=5),
                    'status': 'pending',
                    'authorized_by': users[4] if visitors_count % 2 == 0 else None,
                }
            )
            if created:
                visitors_count += 1
        self.stdout.write(f'✓ Visitantes: {visitors_count} creados')
        
        # 12. Create Communications
        comms_count = 0
        for target_type in ['general', 'building', 'resident']:
            communication, created = Communication.objects.get_or_create(
                garden=garden,
                sender=users[1],  # manager
                title=f'Anuncio {target_type}',
                defaults={
                    'body': f'Este es un anuncio de tipo {target_type}',
                    'target_type': target_type,
                    'target_id': str(buildings[0].id) if target_type == 'building' else None,
                    'is_published': True,
                    'published_at': timezone.now(),
                }
            )
            if created:
                comms_count += 1
        self.stdout.write(f'✓ Comunicaciones: {comms_count} creadas')
        
        self.stdout.write(self.style.SUCCESS('\n✅ Datos de prueba creados exitosamente!'))
        self.stdout.write('\n📋 Usuarios de prueba:')
        for user in users:
            self.stdout.write(f'  - {user.email} / password123 ({user.role})')
        self.stdout.write(f'\nℹ️  Total de datos:')
        self.stdout.write(f'  - 1 Jardín (Conjunto)')
        self.stdout.write(f'  - 3 Edificios')
        self.stdout.write(f'  - {len(apartments)} Departamentos')
        self.stdout.write(f'  - {len(users)} Usuarios')
        self.stdout.write(f'  - {residents_count} Residentes')
        self.stdout.write(f'  - {payments_count} Pagos')
        self.stdout.write(f'  - {incidents_count} Incidentes')
        self.stdout.write(f'  - {reservations_count} Reservas')
        self.stdout.write(f'  - {visitors_count} Visitantes')
        self.stdout.write(f'  - {comms_count} Comunicaciones')
