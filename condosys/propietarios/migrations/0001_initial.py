# Generated for Propietario independiente

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Propietario',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('full_name', models.CharField(max_length=100)),
                ('marital_status', models.CharField(choices=[('single', 'Soltero/a'), ('married', 'Casado/a'), ('divorced', 'Divorciado/a'), ('widowed', 'Viudo/a'), ('other', 'Otro')], default='single', max_length=30)),
                ('cedula', models.CharField(max_length=50, unique=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='propietarios/')),
                ('phone', models.CharField(max_length=20)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('emergency_contact', models.CharField(blank=True, max_length=20, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='propietario_profiles', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Propietarios',
                'ordering': ['full_name'],
            },
        ),
    ]
