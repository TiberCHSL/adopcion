# Generated by Django 4.2.4 on 2023-12-31 05:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adopciones', '0020_remove_colecta_monto_inicial_colecta_monto_final_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='datospagousuario',
            name='id',
        ),
        migrations.AlterField(
            model_name='datospagousuario',
            name='num_cuenta',
            field=models.CharField(max_length=50, primary_key=True, serialize=False, verbose_name='Numero de la cuenta'),
        ),
        migrations.DeleteModel(
            name='Pagos',
        ),
    ]