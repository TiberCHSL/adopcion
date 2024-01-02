from django.db import models
from django.contrib.auth.models import User
from d3_dpa_chile.models import Region, Provincia, Comuna


class Organizacion(models.Model):
    nombre_org = models.CharField(primary_key=True, max_length=50, verbose_name="Nombre de la organizacion")
    tipo_organizacion = models.CharField(max_length=50, verbose_name= "Tipo de Organizacion")
    #comuna = models.ForeignKey(Comuna, on_delete=models.CASCADE)
    logo_org = models.ImageField(upload_to="media", verbose_name= "Logo de la Organizacion", blank = True)
    correo = models.CharField(max_length=50, verbose_name = "Correo de contacto de la organizacion", default = "correodefault@gmail.com")
    contacto = models.CharField(max_length=25,verbose_name = 'Telefono de contacto de la organizacion', default = "+569")

    def __str__(self):
        return self.nombre_org

class SedeOrganizacion(models.Model):
    nombre_org = models.ForeignKey(Organizacion, on_delete=models.CASCADE)
    nombre_sede = models.CharField(primary_key = True, max_length = 50, verbose_name = "Nombre de la sede", default = "Nombre por defecto")
    comuna = models.ForeignKey(Comuna, on_delete=models.CASCADE)
    direccion = models.CharField(max_length = 100, verbose_name = "Direccion de la sede")
    contacto = models.CharField(max_length=25,verbose_name = 'Telefono de contacto de la sede', default = "+569")
    
    def __str__(self):
        return self.nombre_sede

class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,verbose_name = "Nombre de usuario")
    phone = models.CharField(max_length=20, verbose_name="Teléfono")
    rut = models.CharField(primary_key=True, max_length=12, verbose_name="RUT")
    birth_date = models.DateField(verbose_name="Fecha de Nacimiento", null=True, blank=True)
    gender = models.CharField(max_length=10, verbose_name="Género", choices=[('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')])
    role = models.CharField(max_length=10, verbose_name="Rol de usuario", choices=[('A', 'Adoptante'), ('O', 'Organizacion')], default= 'A')
    comuna = models.ForeignKey(Comuna, on_delete=models.CASCADE)
    nombre_org = models.ForeignKey(Organizacion, on_delete=models.CASCADE, blank = True, null = True)
    def __str__(self):
        return str(self.user)


class DatosPagoUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,verbose_name = "Nombre de usuario")
    banco = models.CharField(max_length=50)
    acc_type = models.CharField(max_length=50, choices=[('C','Cuenta corriente'),('V','Cuenta vista'),('A','Cuenta de ahorro')])
    num_cuenta = models.CharField(primary_key = True,max_length=50,verbose_name = "Numero de la cuenta")
    def __str__(self):
        return str(self.user)


class Pagos(models.Model):
    num_cuenta = models.ForeignKey(DatosPagoUsuario, on_delete=models.CASCADE, null = True)
    monto = models.IntegerField(verbose_name = 'Cantidad')
    def __str__(self):
        return str(self.num_cuenta)


class TipoMascota(models.Model):
    tipo_nombre = models.CharField(primary_key = True, max_length=10, verbose_name="Tipo de mascota", choices=[('P', 'Perro'), ('G', 'Gato'), ('O', 'Otro')])
    
    def __str__(self):
        return self.get_tipo_nombre_display()


class Mascota(models.Model):
    sede_org = models.ForeignKey(SedeOrganizacion, max_length=12, verbose_name="Sede de la organizacion" , on_delete=models.CASCADE)
    tipo_nombre = models.ForeignKey(TipoMascota, on_delete=models.CASCADE)
    descripcion = models.TextField(verbose_name = "Descripcion de la mascota")
    tamano = models.CharField(max_length=25, verbose_name="Tamaño de la mascota", choices=[('S', 'Pequeño'), ('L', 'Grande'), ('M', 'Mediano')], default ='S' )
    soc_1 = models.CharField(max_length=25, verbose_name="Sociable con niños", choices=[('S', 'Si'), ('N', 'No'), ('N/A', 'No se sabe')], default ='N/A' )
    soc_2 = models.CharField(max_length=25, verbose_name="Sociable con perros", choices=[('S', 'Si'), ('N', 'No'), ('N/A', 'No se sabe')], default ='N/A' )
    soc_3 = models.CharField(max_length=25, verbose_name="Sociable con gatos", choices=[('S', 'Si'), ('N', 'No'), ('N/A', 'No se sabe')], default ='N/A' )
    rut = models.ForeignKey(Usuario, max_length=12, verbose_name="RUT" , on_delete=models.CASCADE, blank = True, null = True)
    edad_est = models.IntegerField(verbose_name = "Edad estimada de la mascota")
    estado_adopcion = models.BooleanField(default = False)
    
    def __str__(self):
        return str(self.tipo_nombre)

    #Revisar

class Imagen(models.Model):
    img_mascota = models.ImageField(upload_to="media", verbose_name= "Imagen de la mascota")
    id_mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id_mascota)

    #Averiguar como heredar ID default

class Seguimiento(models.Model):
    fecha = models.DateField(verbose_name = "Fecha del seguimiento", null=True)
    centro_veterinario = models.CharField(max_length=100, verbose_name="Centro veterinario",null=True, blank=True)
    medico_veterinario = models.CharField(max_length=100, verbose_name="Medico veterinario", null=True, blank=True)
    diagnostico = models.TextField(verbose_name = "Diagnostico del seguimiento")
    receta = models.CharField(max_length=200, verbose_name= "Receta de la visita", null = True, blank = True)
    rut = models.ForeignKey(Usuario, max_length=12, verbose_name="RUT del dueño" , on_delete=models.CASCADE)
    id_mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.fecha)

class Vacuna(models.Model):
    fecha = models.DateField(verbose_name="Fecha de Vacunacion", null=True, blank=True)
    tipo_vacuna = models.CharField(max_length=100, verbose_name="Tipo de vacuna", null=True, blank=True)
    vigencia = models.CharField(max_length=100, verbose_name="Vigencia de la vacuna (meses o años)", null=True, blank=True)
    id_seguimiento = models.ForeignKey(Seguimiento, on_delete=models.CASCADE)

    def __str__(self):
        return self.tipo_vacuna

class Verificacion(models.Model):
    tipo_ver = models.CharField(max_length = 20,choices = [("O","Online"),("P","Presencial")])
    descripcion = models.TextField(verbose_name = "Descripcion de la verificacion")
    fecha = models.DateField(verbose_name="Fecha de la verificacion", null=True, blank=True)
    #vigencia_animal = models.BooleanField(verbose_name = "Debe ser devuelto o no", null = True, blank = True)
    rut = models.ForeignKey(Usuario, max_length=12, verbose_name="RUT del dueño" , on_delete=models.CASCADE)
    id_mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE, default=0)

class Colecta(models.Model):
    nombre_org = models.ForeignKey(Organizacion, max_length=12, verbose_name="Nombre de la organizacion" , on_delete=models.CASCADE)
    nombre_colecta = models.CharField(max_length = 50, verbose_name = "Nombre de la colecta")
    descripcion_colecta = models.TextField(verbose_name = 'Descripcion de la colecta')
    banco = models.CharField(max_length=50)
    acc_type = models.CharField(max_length=50, choices=[('C','Cuenta corriente'),('V','Cuenta vista'),('A','Cuenta de ahorro')])
    num_cuenta = models.CharField(max_length=50,verbose_name = "Numero de la cuenta")
    monto_recaudado= models.IntegerField(verbose_name = "Monto recaudado", default = 0)
    monto_final = models.IntegerField(verbose_name = "Monto a recaudar", default = 100000)
    def __str__(self):
        return self.nombre_colecta



#Debe ser mayor de edad, validacion

