"""
Permission classes para control de acceso basado en roles
"""
from rest_framework.permissions import BasePermission, SAFE_METHODS

# ==================================================
# CONJUNTOS DE ROLES
# ==================================================

ROLES_ADMIN = ('admin',)
ROLES_GESTION = ('admin', 'manager')
ROLES_SEGURIDAD = ('admin', 'manager', 'security')
ROLES_RESIDENTE = ('admin', 'manager', 'resident', 'propietario')
ROLES_TODOS = ('admin', 'manager', 'security', 'resident', 'propietario')

# ==================================================
# PERMISOS DE NIVEL DE VISTA (has_permission)
# ==================================================


class IsAdmin(BasePermission):
    """Solo administradores"""
    message = "Solo administradores pueden acceder a este recurso."

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ROLES_ADMIN


class IsManager(BasePermission):
    """Administrador o gerente"""
    message = "Se requiere rol de administrador o gerente."

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ROLES_GESTION


class IsResident(BasePermission):
    """Residentes, propietarios y gestión (usuarios con unidad propia)"""
    message = "No tienes permisos para acceder a este recurso."

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ROLES_RESIDENTE


class IsResidentOnly(BasePermission):
    """Solo residentes (sin propietarios)"""
    message = "Solo residentes pueden acceder a este recurso."

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'resident'


class IsPropietario(BasePermission):
    """Solo propietarios"""
    message = "Solo propietarios pueden acceder a este recurso."

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'propietario'


class IsResidentOrManager(BasePermission):
    """Residentes, propietarios o gerentes"""
    message = "Se requiere ser residente, propietario o gerente."

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ROLES_RESIDENTE


class IsSecurity(BasePermission):
    """Personal de seguridad o administrador"""
    message = "Se requiere acceso de seguridad."

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ROLES_SEGURIDAD


class IsGestionOrSoloLectura(BasePermission):
    """Cualquier autenticado puede leer; solo admin/manager pueden escribir."""
    message = "No tienes permisos para modificar este recurso."

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.method in SAFE_METHODS:
            return True
        return request.user.role in ROLES_GESTION


class CanModifyUser(BasePermission):
    """Usuario solo puede modificar su propio perfil, admins pueden modificar cualquiera"""
    message = "No puedes modificar este usuario."

    def has_object_permission(self, request, view, obj):
        if request.user.role in ROLES_ADMIN:
            return True
        return request.user == obj


class CanModifyIncident(BasePermission):
    """
    - Reporter puede ver/modificar su incidente
    - Manager/Admin pueden ver/modificar cualquiera
    - Assigned staff pueden ver el suyo
    """
    def has_object_permission(self, request, view, obj):
        if request.user.role in ROLES_GESTION:
            return True
        # Reporter can view/edit own incident
        if obj.reported_by == request.user:
            return True
        # Assigned staff can view their assignments
        if obj.assigned_to == request.user and request.method == 'GET':
            return True
        return False


class CanModifyReservation(BasePermission):
    """
    - User can view/modify own reservations
    - Manager/Admin can approve/reject reservations
    """
    def has_object_permission(self, request, view, obj):
        if request.user.role in ROLES_GESTION:
            return True
        # Reserver can view/modify own reservation
        if obj.reserved_by == request.user:
            return True
        return False


class CanModifyVisitor(BasePermission):
    """
    - Resident can register visitors for own apartment
    - Security can authorize/update visitors
    - Manager/Admin have full access
    """
    def has_object_permission(self, request, view, obj):
        if request.user.role in ROLES_GESTION:
            return True
        if request.user.role == 'security':
            return True
        # Resident can view/edit visitors for own apartment
        from residents.models import Resident
        try:
            resident = Resident.objects.get(user=request.user, apartment=obj.apartment)
            return True
        except Resident.DoesNotExist:
            return False


class CanAccessApartment(BasePermission):
    """
    - Resident can access own apartment data (lectura)
    - Manager/Admin can access cualquier apartamento
    """
    def has_object_permission(self, request, view, obj):
        if request.user.role in ROLES_GESTION:
            return True
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            if request.user.role == 'propietario':
                return obj.owner is not None and obj.owner.user == request.user
            from residents.models import Resident
            try:
                resident = Resident.objects.get(user=request.user, apartment=obj)
                return resident.is_current
            except Resident.DoesNotExist:
                return False
        return False