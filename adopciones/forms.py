# En forms.py
from django import forms
from .models import TipoMascota, Region, Usuario, Comuna, User, DatosPagoUsuario, Seguimiento, Vacuna
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class BusquedaMascotaForm(forms.Form):
    tamano_choices = [('', 'Todos'),('S', 'Pequeño'), ('L', 'Grande'), ('M', 'Mediano')]
    tipo_mascota_choices = [('', 'Todos')] + [(tipo.tipo_nombre, tipo.get_tipo_nombre_display()) for tipo in TipoMascota.objects.all()]
    region_choices = Region.objects.values_list('nombre', 'nombre')

    tamano = forms.ChoiceField(choices=tamano_choices, required=False)
    tipo_mascota = forms.ChoiceField(choices=tipo_mascota_choices, required=False)
    region = forms.ModelChoiceField(queryset=Region.objects.all(), required=False)

class RegistroUsuarioForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, label="Nombres")
    last_name = forms.CharField(max_length=30, label="Apellidos")
    email = forms.EmailField(max_length=254, help_text='Requerido. Ingrese una dirección de correo electrónico válida.')
    phone = forms.CharField(max_length=20, label="Teléfono")
    rut = forms.CharField(max_length=12, label="RUT")
    birth_date = forms.DateField(label="Fecha de Nacimiento", required=False)
    gender = forms.ChoiceField(choices=[('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')], label="Género")
    comuna = forms.ModelChoiceField(queryset=Comuna.objects.all(), label="Comuna de Residencia")

    username = forms.CharField(
        label="Nombre de usuario",
        help_text="Requerido. 150 caracteres o menos. Letras, dígitos y @/./+/-/_ solamente.",
        error_messages={'unique': "Ya existe un usuario con ese nombre."},
    )
    password1 = forms.CharField(
        label="Contraseña",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text="Su contraseña no puede ser demasiado similar a otras información personal. Su contraseña debe contener al menos 8 caracteres. Su contraseña no puede ser una contraseña común.",
    )
    password2 = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text="Ingrese la misma contraseña que antes, para verificación.",
    )
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'phone', 'rut', 'birth_date', 'gender', 'comuna']

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': True}), label="Username")


class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['phone', 'gender', 'comuna']

class DatosPagoUsuarioForm(forms.ModelForm):
    class Meta:
        model = DatosPagoUsuario
        fields = ['banco', 'acc_type', 'num_cuenta']


class VacunaForm(forms.ModelForm):
    seguimiento = forms.ModelChoiceField(
        queryset=Seguimiento.objects.none(),  # Empty queryset
        to_field_name="fecha",
        label="Fecha del seguimiento",
        required=True
    )

    class Meta:
        model = Vacuna
        fields = ['fecha', 'tipo_vacuna', 'vigencia', 'seguimiento']

    def __init__(self, *args, **kwargs):
        mascota_id = kwargs.pop('mascota_id', None)
        super(VacunaForm, self).__init__(*args, **kwargs)
        if mascota_id:
            self.fields['seguimiento'].queryset = Seguimiento.objects.filter(id_mascota=mascota_id)


class SeguimientoForm(forms.ModelForm):
    class Meta:
        model = Seguimiento
        fields = ['fecha', 'centro_veterinario', 'medico_veterinario', 'diagnostico', 'receta']

    class Meta:
        model = Seguimiento
        fields = ['fecha', 'centro_veterinario', 'medico_veterinario', 'diagnostico', 'receta']