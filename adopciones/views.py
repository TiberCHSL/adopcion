
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Mascota, Imagen, TipoMascota, Comuna, SedeOrganizacion
from .forms import BusquedaMascotaForm

def index(request):
    mascotas = Mascota.objects.select_related('id_sede_org__comuna__region').all()[:4]

    for mascota in mascotas:
        mascota.imagen = Imagen.objects.filter(id_mascota=mascota.id).first()

    return render(request, 'index.html', {'mascotas': mascotas})


def detalle_mascota(request, mascota_id):
    mascota = get_object_or_404(Mascota, id=mascota_id)
    imagenes = Imagen.objects.filter(id_mascota=mascota)

    return render(request, 'detalle_mascota.html', {'mascota': mascota, 'imagenes': imagenes})

# En views.py

def buscar_mascotas(request):
    mascotas = None
    form = BusquedaMascotaForm(request.GET or None)
    if form.is_valid():
        # Obtener datos del formulario
        tamano = form.cleaned_data['tamano']
        tipo_mascota = form.cleaned_data['tipo_mascota']
        region = form.cleaned_data['region']

        # Filtrar mascotas
        mascotas = Mascota.objects.all()
        if tamano:
            mascotas = mascotas.filter(tamano=tamano)
        if tipo_mascota:
            mascotas = mascotas.filter(tipo_nombre=tipo_mascota)
        if region:
            mascotas = mascotas.filter(id_sede_org__comuna__region=region)
            
        for mascota in mascotas:
            mascota.imagen = Imagen.objects.filter(id_mascota=mascota.id).first()

    return render(request, 'resultados_busqueda.html', {'mascotas': mascotas, 'form': form})
