from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Residencial',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=150, verbose_name='Nombre del residencial')),
                ('rnc', models.CharField(blank=True, max_length=20, verbose_name='RNC')),
                ('nombre_via', models.CharField(blank=True, max_length=150, verbose_name='Nombre de la vía')),
                ('numero_edificacion', models.CharField(blank=True, max_length=30, verbose_name='Número de la edificación')),
                ('sector', models.CharField(blank=True, max_length=120, verbose_name='Sector')),
                ('codigo_postal', models.CharField(blank=True, max_length=10, verbose_name='Código Postal')),
                ('municipio', models.CharField(blank=True, max_length=120, verbose_name='Municipio/Ciudad')),
                ('provincia', models.CharField(blank=True, choices=[('Distrito Nacional', 'Distrito Nacional'), ('Azua', 'Azua'), ('Baoruco', 'Baoruco'), ('Barahona', 'Barahona'), ('Dajabón', 'Dajabón'), ('Duarte', 'Duarte'), ('Elías Piña', 'Elías Piña'), ('El Seibo', 'El Seibo'), ('Espaillat', 'Espaillat'), ('Independencia', 'Independencia'), ('La Altagracia', 'La Altagracia'), ('La Romana', 'La Romana'), ('La Vega', 'La Vega'), ('María Trinidad Sánchez', 'María Trinidad Sánchez'), ('Monte Cristi', 'Monte Cristi'), ('Pedernales', 'Pedernales'), ('Peravia', 'Peravia'), ('Puerto Plata', 'Puerto Plata'), ('Hermanas Mirabal', 'Hermanas Mirabal'), ('Samaná', 'Samaná'), ('San Cristóbal', 'San Cristóbal'), ('San Juan', 'San Juan'), ('San Pedro de Macorís', 'San Pedro de Macorís'), ('Sánchez Ramírez', 'Sánchez Ramírez'), ('Santiago', 'Santiago'), ('Santiago Rodríguez', 'Santiago Rodríguez'), ('Valverde', 'Valverde'), ('Monseñor Nouel', 'Monseñor Nouel'), ('Monte Plata', 'Monte Plata'), ('Hato Mayor', 'Hato Mayor'), ('San José de Ocoa', 'San José de Ocoa'), ('Santo Domingo', 'Santo Domingo')], max_length=60, verbose_name='Provincia')),
                ('mapa_iframe', models.TextField(blank=True, verbose_name='Iframe de Google Map')),
                ('distribucion', models.CharField(blank=True, choices=[('edificios', 'Edificios'), ('torres', 'Torres'), ('bloques', 'Bloques'), ('casas', 'Casas'), ('mixto', 'Mixto')], max_length=20, verbose_name='Distribución')),
                ('cantidad_edificios', models.PositiveIntegerField(blank=True, null=True, verbose_name='Cantidad de edificios/torres')),
                ('cantidad_pisos', models.PositiveIntegerField(blank=True, null=True, verbose_name='Cantidad de pisos por edificio/torre')),
                ('telefono', models.CharField(blank=True, max_length=20, verbose_name='Teléfono de administración')),
                ('correo', models.EmailField(blank=True, max_length=254, verbose_name='Correo de administración')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Residencial',
                'verbose_name_plural': 'Residencial',
            },
        ),
    ]
