from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Region(models.Model):
    nombre_region = models.CharField(primary_key = True, max_length=10, verbose_name="Género", choices=[('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')])

class Comuna(models.Model):
    nombre_comuna = models.CharField(primary_key = True, max_length=10, verbose_name="Género", choices=[('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')])

class Organizacion(models.Model):
    nombre_org = models.CharField(primary_key=True, max_length=50, verbose_name="Nombre de la organizacion")
    tipo_organizacion = models.CharField(max_length=50, verbose_name= "Tipo de Organizacion")
    comuna = models.ForeignKey(Comuna, on_delete=models.CASCADE)
    logo_org = models.ImageField(upload_to="logo", verbose_name= "Logo de la Organizacion")
    direccion = models.CharField(max_length = 100, verbose_name = "Direccion de la Organizacion")

class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,verbose_name = "Nombre de usuario")
    phone = models.CharField(max_length=20, verbose_name="Teléfono")
    rut = models.CharField(primary_key=True, max_length=12, verbose_name="RUT")
    birth_date = models.DateField(verbose_name="Fecha de Nacimiento", null=True, blank=True)
    gender = models.CharField(max_length=10, verbose_name="Género", choices=[('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')])
    role = models.CharField(max_length=10, verbose_name="Rol de usuario", choices=[('P', 'Postulante'), ('E', 'Empleador')])
    comuna = models.ForeignKey(Comuna, on_delete=models.CASCADE)

class TipoMascota(models.Model):
    tipo_nombre = models.CharField(primary_key = True, max_length=10, verbose_name="Tipo de mascota", choices=[('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')])

class Mascota(models.Model):
    tipo_nombre = models.ForeignKey(TipoMascota, on_delete=models.CASCADE)
    descripcion = models.TextField(verbose_name = "Descripcion de la mascota")
    caracteristicas =  models.CharField(max_length=100, verbose_name="Caracteristicas de la mascota", null=True, blank=True)
    rut = models.ForeignKey(Usuario, max_length=12, verbose_name="RUT" , on_delete=models.CASCADE)
    nombre_org = models.ForeignKey(Organizacion, max_length=12, verbose_name="Nombre de la organizacion" , on_delete=models.CASCADE)
    edad_est = models.IntegerField(verbose_name = "Edad estimada de la mascota")
    #Revisar

class Imagen(models.Model):
    img_mascota = models.ImageField(upload_to="mascota", verbose_name= "Imagen de la mascota")
    id_mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE)
    #Averiguar como heredar ID default

class Seguimiento(models.Model):
    fecha = models.DateField
    centro_veterinario = models.CharField(max_length=100, verbose_name="Centro veterinario",null=True, blank=True)
    medico_veterinario = models.CharField(max_length=100, verbose_name="Medico veterinario", null=True, blank=True)
    diagnostico = models.TextField(verbose_name = "Diagnostico del seguimiento")
    receta = models.CharField(max_length=200, verbose_name= "Receta de la visita")
    rut = models.ForeignKey(Usuario, max_length=12, verbose_name="RUT del dueño" , on_delete=models.CASCADE)
    id_mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE)

class Vacuna(models.Model):
    fecha = models.DateField(verbose_name="Fecha de Nacimiento", null=True, blank=True)
    tipo_vacuna = models.CharField(max_length=100, verbose_name="Tipo de vacuna", null=True, blank=True)
    vigencia = models.CharField(max_length=100, verbose_name="Vigencia de la vacuna (meses o años)", null=True, blank=True)
    id_seguimiento = models.ForeignKey(Seguimiento, on_delete=models.CASCADE)

class Verificacion(models.Model):
    tipo_ver = models.CharField(max_length = 20,choices = [("O","Online"),("P","Presencial")])
    descripcion = models.TextField(verbose_name = "Descripcion de la verificacion")
    fecha = models.DateField(verbose_name="Fecha de la verificacion", null=True, blank=True)
    vigencia_animal = models.BooleanField(verbose_name = "Debe ser devuelto o no", null = True, blank = True)
    rut = models.ForeignKey(Usuario, max_length=12, verbose_name="RUT del dueño" , on_delete=models.CASCADE)
    nombre_org = models.ForeignKey(Organizacion, max_length=12, verbose_name="Nombre de la organizacion" , on_delete=models.CASCADE)


#Debe ser mayor de edad, validacion

