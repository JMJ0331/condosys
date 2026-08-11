"""
Script to create test data
Run with: python manage.py shell < create_testdata.py
"""
from django.utils import timezone
from datetime import timedelta
from accounts.models import User
from structure.models import Garden, Building, Apartment
from residents.models import Resident
from payments.models import ChargeType, Payment

print("\n🌱 Creando datos de prueba...\n")

# 1. Create Garden
garden, created = Garden.objects.get_or_create(
    name='Conjunto Residencial Condosys',
    defaults={'location': 'Bogotá D.C., Colombia', 'is_active': True}
)
print(f'✓ Jardín: {garden.name}')

# 2. Create Buildings
buildings = []
for i in range(1, 4):
    building, _ = Building.objects.get_or_create(
        garden=garden,
        name=f'Edificio {i}',
        defaults={'number_of_floors': 5+i, 'is_active': True}
    )
    buildings.append(building)
print(f'✓ Edificios: {len(buildings)}')

# 3. Create Apartments
apartments = []
for building in buildings:
    for floor in range(1, 6):
        for apt in range(1, 4):
            apartment, _ = Apartment.objects.get_or_create(
                building=building,
                number=f'{floor}{apt:02d}',
                defaults={
                    'floor': floor,
                    'area_m2': 80+floor*5,
                    'type': 'apartment',
                    'status': 'occupied',
                    'is_active': True
                }
            )
            apartments.append(apartment)
print(f'✓ Departamentos: {len(apartments)}')

# 4. Create Users
user_count = 0
for role in ['admin', 'manager', 'resident', 'maintenance', 'security']:
    user, created = User.objects.get_or_create(
        email=f'{role}@condosys.test',
        defaults={
            'first_name': role.capitalize(),
            'last_name': 'Test',
            'role': role,
            'phone': '+5712345678',
            'document': f'100{role[:3]}',
            'is_active': True
        }
    )
    if created:
        user.set_password('password123')
        user.save()
        user_count += 1
print(f'✓ Usuarios: {user_count} nuevos')

# 5. Create Residents
resident_count = 0
residents_user = User.objects.filter(role='resident').first()
if residents_user:
    for apartment in apartments[:10]:
        resident, created = Resident.objects.get_or_create(
            user=residents_user,
            apartment=apartment,
            defaults={
                'role_in_apartment': 'owner',
                'move_in_date': timezone.now() - timedelta(days=180),
                'emergency_contact': 'Contacto Emergencia',
                'emergency_phone': '+5715555555'
            }
        )
        if created:
            resident_count += 1
print(f'✓ Residentes: {resident_count} nuevos')

# 6. Create ChargeTypes
charge_types_data = ['Mantenimiento', 'Mora', 'Parqueo', 'Agua', 'Basura']
ct_count = 0
for charge_name in charge_types_data:
    charge, created = ChargeType.objects.get_or_create(
        name=charge_name,
        defaults={'is_active': True}
    )
    if created:
        ct_count += 1
print(f'✓ Tipos de Cargos: {ct_count} nuevos')

# 7. Create some Payments
payment_count = 0
charge_types = ChargeType.objects.all()
for apartment in apartments[:5]:
    for charge in charge_types[:2]:
        payment, created = Payment.objects.get_or_create(
            apartment=apartment,
            charge_type=charge,
            invoice_date=timezone.now() - timedelta(days=15),
            defaults={
                'amount': 250000.00,
                'due_date': timezone.now() + timedelta(days=15),
                'status': 'pending',
                'payment_method': 'transfer'
            }
        )
        if created:
            payment_count += 1
print(f'✓ Pagos: {payment_count} nuevos')

print(f'\n✅ Datos de prueba creados!')
print(f'\n📋 Usuarios disponibles:')
for user in User.objects.all()[:7]:
    print(f'  - {user.email} / password123 ({user.role})')
print(f'\nℹ️  Total de datos:')
print(f'  - {Garden.objects.count()} Jardín/Conjunto')
print(f'  - {Building.objects.count()} Edificios')
print(f'  - {Apartment.objects.count()} Departamentos')
print(f'  - {User.objects.count()} Usuarios')
print(f'  - {Resident.objects.count()} Residentes')
print(f'  - {Payment.objects.count()} Pagos')
print()
