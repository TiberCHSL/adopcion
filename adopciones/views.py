
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from .models import Mascota, Imagen, TipoMascota, Comuna, SedeOrganizacion, Colecta, DatosPagoUsuario, Usuario, Seguimiento, Pagos, Vacuna, Verificacion, Colecta
from .forms import BusquedaMascotaForm, RegistroUsuarioForm, LoginForm, DatosPagoUsuarioForm, UsuarioForm, SeguimientoForm, VacunaForm, MascotaForm, ImagenForm
from .forms import EditMascotaForm, AssignOwnerForm, VerificacionForm, ColectaForm
from django.forms import formset_factory
from django.views.decorators.csrf import csrf_exempt

def index(request):
    mascotas = Mascota.objects.select_related('sede_org__comuna__region').all()[:4]

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
            mascotas = mascotas.filter(sede_org__comuna__region=region)
            
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

    def get_success_url(self):
        user = self.request.user
        if user.usuario.role == 'A':  # Adoptante
            return redirect('index').url  # replace with the actual view name
        elif user.usuario.role == 'O':  # Organizacion
            return redirect('organizacion_index_view').url  # replace with the actual view name
        else:
            return super().get_success_url()  # default to the original behavior

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

@login_required
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

@login_required
def lista_vacunas(request, seguimiento_id):
    vacunas = Vacuna.objects.filter(id_seguimiento=seguimiento_id)
    return render(request, 'lista_vacunas.html', {'vacunas': vacunas})

@login_required
def organizacion_index(request):
    # Get the logged-in user's organization
    user_org = request.user.usuario.nombre_org

    # Get the SedeOrganizacion instances associated with the user's organization
    sedes = SedeOrganizacion.objects.filter(nombre_org=user_org)

    # Get the Mascota instances associated with the user's organization's sedes
    mascotas = Mascota.objects.select_related('sede_org__comuna__region').filter(sede_org__in=sedes)

    for mascota in mascotas:
        mascota.imagen = Imagen.objects.filter(id_mascota=mascota.id).first()
    logo_url = user_org.logo_org.url

    return render(request, 'index_org.html', {'mascotas': mascotas, 'logo_url': logo_url})

@login_required
def sedes_organizacion(request):
    # Get the logged-in user's organization
    user_org = request.user.usuario.nombre_org

    # Get the SedeOrganizacion instances associated with the user's organization
    sedes = SedeOrganizacion.objects.filter(nombre_org=user_org)

    return render(request, 'sedes_organizacion.html', {'sedes': sedes})

def mascotas_sede(request, sede_id):
   # Get the SedeOrganizacion instance
   sede = SedeOrganizacion.objects.get(nombre_sede=sede_id)

   # Get the Mascota instances associated with the SedeOrganizacion
   mascotas_no_adopcion = Mascota.objects.filter(sede_org=sede, estado_adopcion=False)
   mascotas_adopcion = Mascota.objects.filter(sede_org=sede, estado_adopcion=True)

   return render(request, 'mascotas_sede.html', {'mascotas_no_adopcion': mascotas_no_adopcion, 'mascotas_adopcion': mascotas_adopcion})

@login_required
def agregar_mascota(request, sede_id):
    # Get the SedeOrganizacion instance
    sede = SedeOrganizacion.objects.get(nombre_sede=sede_id)

    ImagenFormSet = formset_factory(ImagenForm, extra=3)
    if request.method == 'POST':
        form = MascotaForm(request.POST)
        imagen_formset = ImagenFormSet(request.POST, request.FILES, prefix='imagenes')
        if form.is_valid() and imagen_formset.is_valid():
            mascota = form.save(commit=False)
            mascota.sede_org = sede  # Set the sede_org field
            mascota.save()
            for imagen_form in imagen_formset:
                imagen = imagen_form.save(commit=False)
                imagen.id_mascota = mascota
                imagen.save()
            return redirect('mascotas_sede_view', sede_id=mascota.sede_org.nombre_sede)
    else:
        form = MascotaForm()
        imagen_formset = ImagenFormSet(prefix='imagenes')
    return render(request, 'agregar_mascota.html', {'form': form, 'imagen_formset': imagen_formset})

@login_required
def edit_mascota(request, pk):
   mascota = get_object_or_404(Mascota, pk=pk)

   if request.method == 'POST':
       form = EditMascotaForm(request.POST, instance=mascota)
       if form.is_valid():
           form.save()
           return redirect('mascotas_sede_view', sede_id=mascota.sede_org.nombre_sede)
   else:
       form = EditMascotaForm(instance=mascota)

   return render(request, 'edit_mascota.html', {'form': form})

@login_required
def lista_seguimientos_org(request, mascota_id):
    seguimientos = Seguimiento.objects.filter(id_mascota=mascota_id)
    for seguimiento in seguimientos:
        seguimiento.vacunas = Vacuna.objects.filter(id_seguimiento=seguimiento)
    return render(request, 'lista_seguimientos_org.html', {'seguimientos': seguimientos})

@login_required
def lista_vacunas_org(request, seguimiento_id):
    vacunas = Vacuna.objects.filter(id_seguimiento=seguimiento_id)
    return render(request, 'lista_vacunas_org.html', {'vacunas': vacunas})

@login_required
def delete_mascota(request, mascota_id):
   mascota = get_object_or_404(Mascota, id=mascota_id)
   mascota.delete()
   return redirect('mascotas_sede_view', sede_id=mascota.sede_org.nombre_sede)

@login_required
def unadopt_mascota(request, mascota_id):
    mascota = get_object_or_404(Mascota, id=mascota_id)
    mascota.rut = None
    mascota.estado_adopcion = False
    mascota.save()
    return redirect('mascotas_sede_view', sede_id=mascota.sede_org.nombre_sede)


@csrf_exempt
@login_required
def assign_owner(request, mascota_id):
    mascota = get_object_or_404(Mascota, id=mascota_id)
    if request.method == 'POST':
        rut = request.POST.get('rut')
        if rut:
            try:
                usuario = Usuario.objects.get(rut=rut)
                mascota.rut = usuario
                mascota.estado_adopcion = True
                mascota.save()
            except Usuario.DoesNotExist:
                # Handle the case where the entered rut does not exist
                pass
    return redirect('mascotas_sede_view', sede_id=mascota.sede_org.nombre_sede)


@login_required
def add_verificacion(request, mascota_id):
    mascota = get_object_or_404(Mascota, id=mascota_id)
    if request.method == 'POST':
        form = VerificacionForm(request.POST)
        if form.is_valid():
            verificacion = form.save(commit=False)
            verificacion.rut = mascota.rut
            verificacion.id_mascota = mascota
            verificacion.save()
            return redirect('mascotas_sede_view', sede_id=mascota.sede_org.nombre_sede)
    else:
        form = VerificacionForm()
    return render(request, 'add_verificacion.html', {'form': form})

@login_required
def verificaciones_mascota(request, mascota_id):
    verificaciones = Verificacion.objects.filter(id_mascota=mascota_id)
    return render(request, 'verificaciones_mascota.html', {'verificaciones': verificaciones})

@login_required
def verificaciones_mascota_usuario(request, mascota_id):
    verificaciones = Verificacion.objects.filter(id_mascota=mascota_id)
    return render(request, 'verificaciones_mascota_usuario.html', {'verificaciones': verificaciones})

@login_required
def list_colectas(request):
    user_org = request.user.usuario.nombre_org
    colectas = Colecta.objects.filter(nombre_org=user_org)
    return render(request, 'list_colectas.html', {'colectas': colectas})

@login_required
def detail_colecta(request, colecta_id):
    colecta = get_object_or_404(Colecta, id=colecta_id)
    return render(request, 'detail_colecta.html', {'colecta': colecta})

@login_required
def create_colecta(request):
    user_org = request.user.usuario.nombre_org
    if request.method == 'POST':
        form = ColectaForm(request.POST)
        if form.is_valid():
            colecta = form.save(commit=False)
            colecta.nombre_org = user_org
            colecta.save()
            return redirect('list_colectas')
    else:
        form = ColectaForm()
    return render(request, 'create_colecta.html', {'form': form})

@login_required
def edit_colecta(request, colecta_id):
    colecta = get_object_or_404(Colecta, id=colecta_id)
    if request.method == 'POST':
        form = ColectaForm(request.POST, instance=colecta)
        if form.is_valid():
            form.save()
            return redirect('detail_colecta', colecta_id=colecta.id)
    else:
        form = ColectaForm(instance=colecta)
    return render(request, 'edit_colecta.html', {'form': form})

@login_required
def delete_colecta(request, colecta_id):
    colecta = get_object_or_404(Colecta, id=colecta_id)
    colecta.delete()
    return redirect('list_colectas')

@login_required
def perfil_usuario_org(request):
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
    return render(request, 'perfil_usuario_org.html', {'usuario_form': usuario_form, 'datos_pago_form': datos_pago_form, 'mascotas': mascotas, 'datos_pago': datos_pago})

