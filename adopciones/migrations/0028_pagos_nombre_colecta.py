# Generated by Django 4.2.4 on 2024-01-02 13:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adopciones', '0027_remove_verificacion_vigencia_animal'),
    ]

    operations = [
        migrations.AddField(
            model_name='pagos',
            name='nombre_colecta',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='adopciones.colecta'),
        ),
    ]