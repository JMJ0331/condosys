# Reemplaza los textos tower/block de Building por el FK obligatorio a Block

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('structure', '0006_migrar_bloques'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='building',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='building',
            name='tower',
        ),
        migrations.RemoveField(
            model_name='building',
            name='block',
        ),
        migrations.RenameField(
            model_name='building',
            old_name='nuevo_bloque',
            new_name='block',
        ),
        migrations.AlterField(
            model_name='building',
            name='block',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='buildings', to='structure.block'),
        ),
        migrations.AlterField(
            model_name='building',
            name='garden',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='buildings', to='structure.garden'),
        ),
        migrations.AlterField(
            model_name='apartment',
            name='building',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='apartments', to='structure.building'),
        ),
        migrations.AlterModelOptions(
            name='building',
            options={'ordering': ['garden', 'block', 'name'], 'verbose_name_plural': 'Buildings'},
        ),
        migrations.AlterUniqueTogether(
            name='building',
            unique_together={('block', 'name')},
        ),
    ]
