# Generated manually for structure model redesign

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('residents', '0001_initial'),
        ('structure', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='building',
            name='tower',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='building',
            name='block',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.RenameField(
            model_name='apartment',
            old_name='number',
            new_name='name',
        ),
        migrations.AlterField(
            model_name='apartment',
            name='name',
            field=models.CharField(help_text='Nombre del departamento', max_length=50),
        ),
        migrations.AddField(
            model_name='apartment',
            name='owner',
            field=models.ForeignKey(blank=True, help_text='Propietario/Residente del departamento', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='apartments_owned', to='residents.resident'),
        ),
        migrations.AddField(
            model_name='apartment',
            name='photo',
            field=models.ImageField(blank=True, help_text='Imagen del departamento', null=True, upload_to='apartments/'),
        ),
        migrations.AlterField(
            model_name='apartment',
            name='status',
            field=models.CharField(choices=[('empty', 'Vacío'), ('occupied', 'Ocupado'), ('maintenance', 'En reparación'), ('blocked', 'Bloqueado')], default='empty', max_length=30),
        ),
        migrations.RemoveField(
            model_name='apartment',
            name='area_m2',
        ),
        migrations.RemoveField(
            model_name='apartment',
            name='type',
        ),
        migrations.AlterUniqueTogether(
            name='apartment',
            unique_together={('building', 'name')},
        ),
    ]