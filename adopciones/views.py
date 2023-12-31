
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from .models import Mascota, Imagen, TipoMascota, Comuna, SedeOrganizacion, Colecta, DatosPagoUsuario, Usuario, Seguimiento, Pagos, Vacuna
from .forms import BusquedaMascotaForm, RegistroUsuarioForm, LoginForm, DatosPagoUsuarioForm, UsuarioForm, SeguimientoForm, VacunaForm

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
                #Realizar donación
                Pagos.objects.create(num_cuenta=datos_pago, monto=monto)
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

@login_required
def perfil_usuario(request):
    user = request.user
    usuario = Usuario.objects.get(user=user)
    datos_pago_form = DatosPagoUsuarioForm()

    if request.method == 'POST':
        usuario_form = UsuarioForm(request.POST, instance=usuario)
        if usuario_form.is_valid():
            usuario_form.save()
    else:
        usuario_form = UsuarioForm(instance=usuario)

    mascotas = Mascota.objects.filter(rut=usuario.rut)

    datos_pago = DatosPagoUsuario.objects.filter(user=request.user).first()
    return render(request, 'perfil_usuario.html', {'usuario_form': usuario_form, 'datos_pago_form': datos_pago_form, 'mascotas': mascotas, 'datos_pago': datos_pago})

@login_required
def agregar_datos_pago(request):
    user = request.user
    usuario = Usuario.objects.get(user=user)

    if request.method == 'POST':
        datos_pago_form = DatosPagoUsuarioForm(request.POST)
        if datos_pago_form.is_valid():
            datos_pago = datos_pago_form.save(commit=False)
            datos_pago.user = user
            datos_pago.save()
            return redirect('perfil_usuario')
    else:
        datos_pago_form = DatosPagoUsuarioForm()

    return render(request, 'agregar_datos_pago.html', {'datos_pago_form': datos_pago_form})

@login_required
def eliminar_datos_pago(request):
    datos_pago = DatosPagoUsuario.objects.filter(user=request.user).first()
    if datos_pago:
        datos_pago.delete()
    return redirect('perfil_usuario')

@login_required
def crear_seguimiento(request, mascota_id):
    if request.method == 'POST':
        seguimiento_form = SeguimientoForm(request.POST)
        if seguimiento_form.is_valid():
            seguimiento = seguimiento_form.save(commit=False)
            seguimiento.rut = request.user.usuario  # Asigna el usuario actual
            seguimiento.id_mascota_id = mascota_id
            seguimiento.save()
            return redirect('perfil_usuario')
    else:
        seguimiento_form = SeguimientoForm()

    return render(request, 'crear_seguimiento.html', {'seguimiento_form': seguimiento_form, 'mascota_id': mascota_id})

def lista_seguimientos(request, mascota_id):
    seguimientos = Seguimiento.objects.filter(id_mascota=mascota_id)
    for seguimiento in seguimientos:
        seguimiento.vacunas = Vacuna.objects.filter(id_seguimiento=seguimiento)
    return render(request, 'lista_seguimientos.html', {'seguimientos': seguimientos})

@login_required
def crear_vacuna(request, mascota_id):
    if request.method == 'POST':
        vacuna_form = VacunaForm(request.POST, mascota_id=mascota_id)
        if vacuna_form.is_valid():
            vacuna = vacuna_form.save(commit=False)
            vacuna.id_mascota_id = mascota_id
            vacuna.id_seguimiento = vacuna_form.cleaned_data['seguimiento']
            vacuna.save()
            return redirect('perfil_usuario')
    else:
        vacuna_form = VacunaForm(mascota_id=mascota_id)

    return render(request, 'crear_vacuna.html', {'vacuna_form': vacuna_form})

def lista_vacunas(request, seguimiento_id):
    vacunas = Vacuna.objects.filter(id_seguimiento=seguimiento_id)
    return render(request, 'lista_vacunas.html', {'vacunas': vacunas})