from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as ErrorValidacion
from .models import User


class CuentaUsuarioFormBase(forms.ModelForm):
    """Base abstracta con los campos de contraseña y la creación/edición de
    la cuenta de acceso (User).

    Cada formulario concreto que la hereda define su propio `Meta` (model
    y campos) y `rol_cuenta` ('resident', 'propietario', ...). La contraseña
    solo se recibe del admin, se valida y se guarda hasheada con
    create_user/set_password; nunca se devuelve al frontend (los campos usan
    PasswordInput y los serializers no la incluyen).
    """

    rol_cuenta = None

    class Meta:
        abstract = True

    password = forms.CharField(
        label='Contraseña',
        min_length=8,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )
    password_confirmation = forms.CharField(
        label='Confirmar contraseña',
        min_length=8,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # El login es por correo: el email siempre es obligatorio.
        if 'email' in self.fields:
            self.fields['email'].required = True
        # En alta (sin instancia vinculada) la contraseña es obligatoria;
        # en edición solo si se quiere cambiar (en blanco = conservar).
        # Los modelos usan UUID generado al instanciar, así que no se puede
        # distinguir con instance.pk: se usa la presencia de `instance`.
        alta = kwargs.get('instance') is None
        self.fields['password'].required = alta
        self.fields['password_confirmation'].required = alta

    def clean_email(self):
        email = self.cleaned_data['email']
        duplicadas = User.objects.filter(email=email)
        if self.instance.user_id:
            duplicadas = duplicadas.exclude(pk=self.instance.user_id)
        if duplicadas.exists():
            raise forms.ValidationError('Ya existe una cuenta con ese correo electrónico.')
        return email

    def clean(self):
        datos = super().clean()
        password = datos.get('password')
        confirmacion = datos.get('password_confirmation')

        if password and not confirmacion:
            self.add_error('password_confirmation', 'Confirma la contraseña.')
        elif confirmacion and not password:
            self.add_error('password', 'Escribe la contraseña.')
        elif password and confirmacion:
            if password != confirmacion:
                self.add_error('password_confirmation', 'Las contraseñas no coinciden.')
            else:
                try:
                    validate_password(password, user=self._usuario_de_prueba(datos))
                except ErrorValidacion as error:
                    self.add_error('password', ' '.join(error.messages))
        return datos

    def _usuario_de_prueba(self, datos):
        """Usuario no guardado para validar la contraseña contra los
        atributos (email, nombre) sin tocar la base de datos."""
        nombre = datos.get('full_name') or getattr(self.instance, 'full_name', '') or ''
        partes = nombre.split()
        return User(
            email=datos.get('email') or getattr(self.instance, 'email', '') or '',
            first_name=partes[0] if partes else '',
            last_name=' '.join(partes[1:]),
        )

    def save(self, commit=True):
        persona = super().save(commit=False)
        self._guardar_cuenta(persona)
        if commit:
            persona.save()
            self._save_m2m()
        else:
            self.save_m2m = self._save_m2m
        return persona

    def _guardar_cuenta(self, persona):
        """Crea o actualiza la cuenta User vinculada al residente/propietario."""
        password = self.cleaned_data.get('password')
        cuenta = persona.user

        if cuenta is None:
            if not password:
                return
            persona.user = User.objects.create_user(
                email=persona.email,
                password=password,
                first_name=self._nombre_propio(persona.full_name)[0],
                last_name=self._nombre_propio(persona.full_name)[1],
                role=self.rol_cuenta,
                status='active',
                is_active=persona.is_active,
            )
            return

        primero, resto = self._nombre_propio(persona.full_name)
        cambios = {}
        if cuenta.email != persona.email:
            cambios['email'] = persona.email
        if cuenta.is_active != persona.is_active:
            cambios['is_active'] = persona.is_active
        if cuenta.first_name != primero or cuenta.last_name != resto:
            cambios['first_name'] = primero
            cambios['last_name'] = resto
        if password:
            cuenta.set_password(password)
        if cambios:
            for atributo, valor in cambios.items():
                setattr(cuenta, atributo, valor)
            cuenta.save()
        elif password:
            cuenta.save()

    @staticmethod
    def _nombre_propio(full_name):
        partes = (full_name or '').split()
        return (
            partes[0] if partes else '',
            ' '.join(partes[1:]),
        )


class UserCreateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, min_length=8)
    password_confirmation = forms.CharField(widget=forms.PasswordInput, min_length=8)

    class Meta:
        model = User
        fields = [
            'email', 'first_name', 'last_name', 'phone', 'document',
            'avatar_url', 'role', 'status', 'garden', 'is_active',
        ]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirmation = cleaned_data.get('password_confirmation')
        if password and confirmation and password != confirmation:
            self.add_error('password_confirmation', 'Las contraseñas no coinciden.')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
