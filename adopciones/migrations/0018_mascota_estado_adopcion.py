# Generated by Django 4.2.4 on 2023-12-29 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adopciones', '0017_sedeorganizacion_nombre_sede'),
    ]

    operations = [
        migrations.AddField(
            model_name='mascota',
            name='estado_adopcion',
            field=models.BooleanField(default=False),
        ),
    ]
