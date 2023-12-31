# Generated by Django 4.2.4 on 2023-12-31 17:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adopciones', '0023_usuario_nombre_org'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='datospagousuario',
            name='user',
        ),
        migrations.RemoveField(
            model_name='imagen',
            name='id_mascota',
        ),
        migrations.RemoveField(
            model_name='mascota',
            name='id_sede_org',
        ),
        migrations.RemoveField(
            model_name='mascota',
            name='rut',
        ),
        migrations.RemoveField(
            model_name='mascota',
            name='tipo_nombre',
        ),
        migrations.RemoveField(
            model_name='pagos',
            name='num_cuenta',
        ),
        migrations.RemoveField(
            model_name='sedeorganizacion',
            name='comuna',
        ),
        migrations.RemoveField(
            model_name='sedeorganizacion',
            name='nombre_org',
        ),
        migrations.RemoveField(
            model_name='seguimiento',
            name='id_mascota',
        ),
        migrations.RemoveField(
            model_name='seguimiento',
            name='rut',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='comuna',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='nombre_org',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='user',
        ),
        migrations.RemoveField(
            model_name='vacuna',
            name='id_seguimiento',
        ),
        migrations.RemoveField(
            model_name='verificacion',
            name='nombre_org',
        ),
        migrations.RemoveField(
            model_name='verificacion',
            name='rut',
        ),
        migrations.DeleteModel(
            name='Colecta',
        ),
        migrations.DeleteModel(
            name='DatosPagoUsuario',
        ),
        migrations.DeleteModel(
            name='Imagen',
        ),
        migrations.DeleteModel(
            name='Mascota',
        ),
        migrations.DeleteModel(
            name='Organizacion',
        ),
        migrations.DeleteModel(
            name='Pagos',
        ),
        migrations.DeleteModel(
            name='SedeOrganizacion',
        ),
        migrations.DeleteModel(
            name='Seguimiento',
        ),
        migrations.DeleteModel(
            name='TipoMascota',
        ),
        migrations.DeleteModel(
            name='Usuario',
        ),
        migrations.DeleteModel(
            name='Vacuna',
        ),
        migrations.DeleteModel(
            name='Verificacion',
        ),
    ]
