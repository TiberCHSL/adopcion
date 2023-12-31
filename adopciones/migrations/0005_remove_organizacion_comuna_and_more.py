# Generated by Django 4.2.4 on 2023-12-27 19:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('d3_dpa_chile', '0002_alter_comuna_codigo_alter_provincia_codigo_and_more'),
        ('adopciones', '0004_organizacion_contacto_seguimiento_fecha_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organizacion',
            name='comuna',
        ),
        migrations.RemoveField(
            model_name='organizacion',
            name='direccion',
        ),
        migrations.AlterField(
            model_name='usuario',
            name='role',
            field=models.CharField(choices=[('A', 'Adoptante'), ('O', 'Organizacion')], default='A', max_length=10, verbose_name='Rol de usuario'),
        ),
        migrations.CreateModel(
            name='SedeOrganizacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('direccion', models.CharField(max_length=100, verbose_name='Direccion de la sede')),
                ('comuna', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='d3_dpa_chile.comuna')),
                ('nombre_org', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adopciones.organizacion')),
            ],
        ),
    ]
