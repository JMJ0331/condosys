# Convierte el texto Building.block en registros Block (o "General" si estaba vacío)

from django.db import migrations


def crear_bloques(apps, schema_editor):
    Block = apps.get_model('structure', 'Block')
    Building = apps.get_model('structure', 'Building')
    for edificio in Building.objects.all():
        nombre = (edificio.block or '').strip() or 'General'
        bloque, _ = Block.objects.get_or_create(garden_id=edificio.garden_id, name=nombre)
        edificio.nuevo_bloque = bloque
        edificio.save(update_fields=['nuevo_bloque'])


def revertir(apps, schema_editor):
    Building = apps.get_model('structure', 'Building')
    for edificio in Building.objects.select_related('nuevo_bloque'):
        edificio.block = edificio.nuevo_bloque.name if edificio.nuevo_bloque else None
        edificio.save(update_fields=['block'])


class Migration(migrations.Migration):

    dependencies = [
        ('structure', '0005_block'),
    ]

    operations = [
        migrations.RunPython(crear_bloques, revertir),
    ]
