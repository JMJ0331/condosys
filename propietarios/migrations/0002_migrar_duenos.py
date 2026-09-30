# Migra los dueños actuales (Resident referenciado por Apartment.owner)
# a la nueva tabla Propietario, reutilizando el mismo UUID para que
# Apartment.owner_id siga siendo válido tras el AlterField.

from django.db import migrations


def migrar_duenos(apps, schema_editor):
    Resident = apps.get_model('residents', 'Resident')
    Propietario = apps.get_model('propietarios', 'Propietario')
    Apartment = apps.get_model('structure', 'Apartment')

    owner_ids = (
        Apartment.objects.exclude(owner_id__isnull=True)
        .values_list('owner_id', flat=True)
        .distinct()
    )
    for resident in Resident.objects.filter(id__in=owner_ids):
        Propietario.objects.get_or_create(
            id=resident.id,
            defaults={
                'user_id': resident.user_id,
                'full_name': resident.full_name,
                'marital_status': resident.marital_status,
                'cedula': resident.cedula,
                'photo': resident.photo,
                'phone': resident.phone,
                'email': resident.email,
                'emergency_contact': resident.emergency_contact,
                'is_active': resident.is_active,
            },
        )


def revertir(apps, schema_editor):
    Propietario = apps.get_model('propietarios', 'Propietario')
    Propietario.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('propietarios', '0001_initial'),
        ('residents', '0001_initial'),
        ('structure', '0002_apartment_renames'),
    ]

    operations = [
        migrations.RunPython(migrar_duenos, revertir),
    ]
