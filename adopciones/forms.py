# En forms.py
from django import forms
from .models import TipoMascota, Region

class BusquedaMascotaForm(forms.Form):
    tamano_choices = [('', 'Todos'),('S', 'Pequeño'), ('L', 'Grande'), ('M', 'Mediano')]
    tipo_mascota_choices = [('', 'Todos')] + [(tipo.tipo_nombre, tipo.get_tipo_nombre_display()) for tipo in TipoMascota.objects.all()]
    region_choices = Region.objects.values_list('nombre', 'nombre')

    tamano = forms.ChoiceField(choices=tamano_choices, required=False)
    tipo_mascota = forms.ChoiceField(choices=tipo_mascota_choices, required=False)
    region = forms.ModelChoiceField(queryset=Region.objects.all(), required=False)
