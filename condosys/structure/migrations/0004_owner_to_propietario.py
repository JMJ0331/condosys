# Apartment.owner ahora apunta a propietarios.Propietario

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('propietarios', '0002_migrar_duenos'),
        ('structure', '0003_apartment_meta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apartment',
            name='owner',
            field=models.ForeignKey(blank=True, help_text='Propietario del departamento', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='apartments_owned', to='propietarios.propietario'),
        ),
    ]
