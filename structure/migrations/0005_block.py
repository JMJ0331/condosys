# Jerarquía Jardín → Bloque → Edificio: crea Block y un FK temporal en Building

import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('structure', '0004_owner_to_propietario'),
    ]

    operations = [
        migrations.CreateModel(
            name='Block',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('garden', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='blocks', to='structure.garden')),
            ],
            options={
                'verbose_name_plural': 'Blocks',
                'ordering': ['garden', 'name'],
                'unique_together': {('garden', 'name')},
            },
        ),
        migrations.AddField(
            model_name='building',
            name='nuevo_bloque',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='structure.block'),
        ),
    ]
