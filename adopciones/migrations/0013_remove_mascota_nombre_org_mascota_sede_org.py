# Generated by Django 4.2.4 on 2023-12-27 22:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adopciones', '0012_alter_vacuna_fecha'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mascota',
            name='nombre_org',
        ),
        migrations.AddField(
            model_name='mascota',
            name='sede_org',
            field=models.ForeignKey(default='0', max_length=12, on_delete=django.db.models.deletion.CASCADE, to='adopciones.sedeorganizacion', verbose_name='Sede de la organizacion'),
        ),
    ]
