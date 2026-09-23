from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from residents.forms import validate_photo
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from .models import User
from .decorators import role_required
from .permissions import ROLES_ADMIN, ROLES_TODOS, IsAdmin, CanModifyUser
from .serializers import UserSerializer, UserCreateSerializer, UserUpdateSerializer, ChangePasswordSerializer
from .forms import UserCreateForm

@role_required(*ROLES_ADMIN)
def app_index(request):
    contexto = {
        'form_user_create': UserCreateForm(),
        'module_name': 'Cuentas'
    }
    return render(request, 'accounts/index.html', contexto)


DESCRIPCIONES_ROL = {
    'admin': 'Administra usuarios, departamentos, pagos y la configuración del residencial.',
    'manager': 'Gestiona pagos, comunicados, reservas y la operación diaria del residencial.',
    'resident': 'Consulta sus pagos, reservas y comunicados del residencial.',
    'propietario': 'Consulta sus unidades, residentes, pagos y mantenimientos.',
    'maintenance': 'Atiende las incidencias y tareas de mantenimiento asignadas.',
    'security': 'Registra visitantes y controla los accesos al residencial.',
}


@role_required(*ROLES_TODOS)
def mi_perfil(request):
    usuario = request.user

    if request.method == 'POST':
        nombre = request.POST.get('full_name', '').strip()
        documento = request.POST.get('document', '').strip() or None
        telefono = request.POST.get('phone', '').strip()
        correo = request.POST.get('email', '').strip()
        estado = request.POST.get('status', 'active')

        if not nombre:
            messages.error(request, 'El nombre completo es obligatorio.')
            return redirect('mi_perfil')

        try:
            validate_email(correo)
        except ValidationError:
            messages.error(request, 'El correo electrónico no es válido.')
            return redirect('mi_perfil')

        if User.objects.filter(email=correo).exclude(pk=usuario.pk).exists():
            messages.error(request, 'Ese correo ya está en uso por otra cuenta.')
            return redirect('mi_perfil')

        if documento and User.objects.filter(document=documento).exclude(pk=usuario.pk).exists():
            messages.error(request, 'Esa cédula ya está registrada en otra cuenta.')
            return redirect('mi_perfil')

        partes = nombre.split()
        usuario.first_name = partes[0]
        usuario.last_name = ' '.join(partes[1:])
        usuario.document = documento
        usuario.phone = telefono
        usuario.email = correo

        avatar = request.FILES.get('avatar')
        if avatar:
            try:
                validate_photo(avatar)
            except ValidationError as err:
                messages.error(request, '; '.join(err.messages))
                return redirect('mi_perfil')
            if usuario.avatar:
                usuario.avatar.delete(save=False)
            usuario.avatar = avatar

        # El rol y la fecha de ingreso no se editan desde aquí (vienen sin
        # name y se ignoran aunque se manipulen). La cuenta propia tampoco
        # se puede desactivar: bloquearía el acceso de quien la edita.
        usuario.status = 'active'
        if estado == 'inactive':
            messages.warning(request, 'No puedes desactivar tu propia cuenta; se mantuvo activa.')

        usuario.save()
        messages.success(request, 'Perfil actualizado correctamente.')
        return redirect('mi_perfil')

    return render(request, 'accounts/perfil.html', {
        'perfil_usuario': usuario,
        'roles': User.ROLE_CHOICES,
        'descripcion_rol': DESCRIPCIONES_ROL.get(usuario.role, ''),
        'module_name': 'Mi perfil',
    })


@role_required(*ROLES_ADMIN)
@require_POST
def crear_usuario_nuevo(request):
    form = UserCreateForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, 'Usuario creado correctamente.')
    else:
        messages.error(request, 'No se pudo crear el usuario. Revisa los datos enviados.')
    return redirect('inicio')


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet para User - CRUD de usuarios"""
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    filter_fields = ['role', 'status', 'is_active']
    search_fields = ['email', 'first_name', 'last_name', 'document']
    ordering_fields = ['created_at', 'email']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action == 'login':
            return [AllowAny()]
        if self.action in ['profile', 'logout']:
            return [IsAuthenticated()]
        if self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), CanModifyUser()]
        return [IsAuthenticated(), IsAdmin()]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.role in ['admin', 'manager']:
            return User.objects.all()
        return User.objects.filter(id=user.id)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        """Endpoint de login: POST /api/users/login/"""
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response(
                {'error': 'Email and password required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(username=email, password=password)
        if user is None:
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        django_login(request, user)
        serializer = UserSerializer(user)
        return Response({
            'message': 'Login successful',
            'user': serializer.data
        })

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def profile(self, request):
        """Endpoint de perfil: GET /api/users/profile/"""
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def change_password(self, request):
        """Endpoint para cambiar contraseña"""
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        old_password = serializer.validated_data['old_password']
        new_password = serializer.validated_data['new_password']
        user = request.user

        if not user.check_password(old_password):
            return Response({'detail': 'La contraseña actual es incorrecta.'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response({'detail': 'Contraseña actualizada correctamente.'})

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def logout(self, request):
        """Endpoint de logout: POST /api/users/logout/"""
        django_logout(request)
        return Response({'message': 'Logout successful'})

