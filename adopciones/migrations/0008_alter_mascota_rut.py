# Generated by Django 4.2.4 on 2023-12-27 21:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adopciones', '0007_alter_organizacion_logo_org'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mascota',
            name='rut',
            field=models.ForeignKey(blank=True, max_length=12, null=True, on_delete=django.db.models.deletion.CASCADE, to='adopciones.usuario', verbose_name='RUT'),
        ),
    ]
