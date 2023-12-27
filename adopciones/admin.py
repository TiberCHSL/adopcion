from django.contrib import admin
from .models import Organizacion, Usuario, TipoMascota, Mascota, Imagen, Seguimiento, Vacuna, Verificacion,Colecta,SedeOrganizacion
from d3_dpa_chile.models import Region, Provincia, Comuna
#Region, Comuna,

admin.site.register(Region)
admin.site.register(Comuna)
admin.site.register(Provincia)
admin.site.register(SedeOrganizacion)
admin.site.register(Organizacion)
admin.site.register(Usuario)
admin.site.register(TipoMascota)
admin.site.register(Mascota)
admin.site.register(Imagen)
admin.site.register(Seguimiento)
admin.site.register(Vacuna)
admin.site.register(Verificacion)
admin.site.register(Colecta)
# Register your models here.
