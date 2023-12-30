
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from .models import Mascota, Imagen, TipoMascota, Comuna, SedeOrganizacion, Colecta, DatosPagoUsuario,Pagos, Usuario
from .forms import BusquedaMascotaForm, RegistroUsuarioForm, LoginForm

def index(request):
    mascotas = Mascota.objects.select_related('id_sede_org__comuna__region').all()[:4]

    for mascota in mascotas:
        mascota.imagen = Imagen.objects.filter(id_mascota=mascota.id).first()

    return render(request, 'index.html', {'mascotas': mascotas})

@login_required
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

def ver_colectas(request):
    colectas = Colecta.objects.all()
    return render(request, 'ver_colectas.html', {'colectas': colectas})

@login_required
def detalle_colecta(request, colecta_id):
    colecta = Colecta.objects.get(pk=colecta_id)
    user = request.user

    if request.method == 'POST':
        monto = request.POST.get('monto')
        try:
            monto = int(monto)
            if monto <= 0:
                raise ValueError("El monto debe ser positivo.")
            
            datos_pago = DatosPagoUsuario.objects.get(user=user)

            if monto <= colecta.monto_final - colecta.monto_recaudado:
                # Realizar donación
                Pagos.objects.create(num_pago=datos_pago, monto=monto)
                colecta.monto_recaudado += monto
                colecta.save()
                messages.success(request, f'Donación de ${monto} realizada con éxito.')
            else:
                messages.error(request, 'El monto de la donación excede el objetivo de la colecta.')
        except ValueError as e:
            messages.error(request, f'Error al procesar la donación: {str(e)}')

        return redirect('detalle_colecta', colecta_id=colecta_id)
    return render(request, 'detalle_colecta.html', {'colecta': colecta})

def registro_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Iniciar sesión automáticamente después del registro

            # Crear instancia de Usuario personalizado
            usuario_personalizado = Usuario(
                user=user,
                phone=form.cleaned_data['phone'],
                rut=form.cleaned_data['rut'],
                birth_date=form.cleaned_data['birth_date'],
                gender=form.cleaned_data['gender'],
                role='A',
                comuna=form.cleaned_data['comuna']
            )
            usuario_personalizado.save()

            return redirect('index')  # Cambia 'index' por la URL a la que quieres redirigir después del registro
    else:
        form = RegistroUsuarioForm()

    return render(request, 'registro_usuario.html', {'form': form})

class LoginUsuarioView(LoginView):
    form_class = LoginForm
    template_name = 'login.html'
