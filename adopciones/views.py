from django.shortcuts import render
from django.http import HttpResponse
from .models import Mascota, Imagen

def index(request):
    mascotas = Mascota.objects.select_related('id_sede_org__comuna__region').all()

    imagenes_mascotas = {mascota.id: Imagen.objects.filter(id_mascota=mascota.id).first() for mascota in mascotas}

    return render(request, 'index.html', {'mascotas': mascotas, 'imagenes_mascotas': imagenes_mascotas})
