from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as ErrorValidacion

from accounts.models import User
from residents.forms import validate_photo

from .models import IntegracionIA


class UsuarioForm(forms.ModelForm):
    """Edición de usuarios desde Configuración (solo admin).

    Replica el formulario de alta/edición de las demás secciones:
    los mismos campos que muestra la tabla más la foto, con los
    estilos compartidos de `formularios.css`.
    """

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'document', 'avatar',
            'phone', 'email', 'role', 'status', 'is_active',
        ]
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'document': 'Cédula',
            'avatar': 'Foto de perfil',
            'phone': 'Teléfono',
            'email': 'Correo electrónico',
            'role': 'Rol',
            'status': 'Estado',
            'is_active': 'Activo',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Nombre'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Apellido'}),
            'document': forms.TextInput(attrs={'placeholder': '000-0000000-0', 'maxlength': '13', 'data-mascara': 'cedula'}),
            'phone': forms.TextInput(attrs={
                'placeholder': '(000)-000-0000',
                'maxlength': '14',
                'data-mascara': 'telefono',
            }),
            'email': forms.EmailInput(attrs={'placeholder': 'Correo electrónico'}),
            'role': forms.Select(attrs={'class': 'campo-seleccion'}),
            'status': forms.Select(attrs={'class': 'campo-seleccion'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'entrada-interruptor'}),
        }

    avatar = forms.ImageField(
        required=False,
        label='Foto de perfil',
        validators=[validate_photo],
        widget=forms.FileInput(attrs={
            'accept': 'image/jpeg,image/png,image/webp',
            'data-perfil-foto': '',
        }),
    )

    def clean_email(self):
        email = self.cleaned_data['email']
        duplicados = User.objects.filter(email=email).exclude(pk=self.instance.pk)
        if duplicados.exists():
            raise forms.ValidationError('Ya existe una cuenta con ese correo electrónico.')
        return email

    def clean_document(self):
        documento = self.cleaned_data.get('document') or None
        if documento:
            duplicados = User.objects.filter(document=documento).exclude(pk=self.instance.pk)
            if duplicados.exists():
                raise forms.ValidationError('Esa cédula ya está registrada en otra cuenta.')
        return documento


class UsuarioCreateForm(UsuarioForm):
    """Alta de usuarios desde Configuración (solo admin).

    Igual que la edición más el apartado de contraseña temporal:
    el admin define la clave inicial con la que el usuario entrará
    (mínimo 8 caracteres); se guarda hasheada, nunca en claro.
    """

    password = forms.CharField(
        label='Contraseña temporal',
        min_length=8,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'placeholder': 'Mínimo 8 caracteres',
        }),
    )
    password_confirmation = forms.CharField(
        label='Confirmar contraseña temporal',
        min_length=8,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'placeholder': 'Repite la contraseña',
        }),
    )

    def clean(self):
        datos = super().clean()
        password = datos.get('password')
        confirmacion = datos.get('password_confirmation')

        if password and not confirmacion:
            self.add_error('password_confirmation', 'Confirma la contraseña temporal.')
        elif confirmacion and not password:
            self.add_error('password', 'Escribe la contraseña temporal.')
        elif password and confirmacion:
            if password != confirmacion:
                self.add_error('password_confirmation', 'Las contraseñas no coinciden.')
            else:
                nombre = f"{datos.get('first_name', '')} {datos.get('last_name', '')}".strip()
                partes = nombre.split()
                try:
                    validate_password(password, user=User(
                        email=datos.get('email', ''),
                        first_name=partes[0] if partes else '',
                        last_name=' '.join(partes[1:]),
                    ))
                except ErrorValidacion as error:
                    self.add_error('password', ' '.join(error.messages))
        return datos

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.set_password(self.cleaned_data['password'])
        if commit:
            usuario.save()
            self.save_m2m()
        return usuario


class IntegracionIAForm(forms.ModelForm):
    """Proveedor AI, modelo dentro del proveedor y su API Key.

    El select de modelos depende del proveedor elegido (lo llena el JS con
    los datos del HTML); la clave es input de contraseña y en blanco
    significa conservar la guardada.
    """

    class Meta:
        model = IntegracionIA
        fields = ['proveedor', 'modelo', 'api_key']
        labels = {
            'proveedor': 'Proveedor',
            'modelo': 'Modelo',
            'api_key': 'API Key',
        }
        widgets = {
            'proveedor': forms.Select(attrs={'class': 'campo-seleccion'}),
            # Texto libre con sugerencias (datalist): los IDs cambian con
            # frecuencia y así nunca queda desactualizado.
            'modelo': forms.TextInput(attrs={
                'class': 'campo-entrada',
                'placeholder': 'Ej.: gpt-4o',
                'list': 'lista-modelos',
                'autocomplete': 'off',
            }),
            'api_key': forms.PasswordInput(attrs={
                'autocomplete': 'new-password',
                'placeholder': 'Pega aquí la API Key',
            }, render_value=True),
        }
        error_messages = {
            'modelo': {'required': 'Escribe el ID del modelo.'},
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['api_key'].required = False
        datos = getattr(self, 'data', None)
        if datos:
            proveedor = datos.get('proveedor', 'gpt')
        elif self.instance and self.instance.pk:
            proveedor = self.instance.proveedor
        else:
            proveedor = 'gpt'
        self.fields['modelo'].required = bool(IntegracionIA.modelos_de(proveedor))
