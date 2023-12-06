from django.contrib import admin
from .models import Region, Comuna, Organizacion, Usuario, TipoMascota, Mascota, Imagen, Seguimiento, Vacuna, Verificacion

admin.site.register(Region)
admin.site.register(Comuna)
admin.site.register(Organizacion)
admin.site.register(Usuario)
admin.site.register(TipoMascota)
admin.site.register(Mascota)
admin.site.register(Imagen)
admin.site.register(Seguimiento)
admin.site.register(Vacuna)
admin.site.register(Verificacion)
# Register your models here.
