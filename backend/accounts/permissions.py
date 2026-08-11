"""
Permission classes para control de acceso basado en roles
"""
from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """Solo administradores"""
    message = "Solo administradores pueden acceder a este recurso."
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'


class IsManager(BasePermission):
    """Administrador o gerente"""
    message = "Se requiere rol de administrador o gerente."
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['admin', 'manager']


class IsResident(BasePermission):
    """Solo residentes"""
    message = "Solo residentes pueden acceder a este recurso."
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'resident'


class IsResidentOrManager(BasePermission):
    """Residentes o gerentes"""
    message = "Se requiere ser residente o gerente."
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['resident', 'manager', 'admin']


class IsMaintenance(BasePermission):
    """Personal de mantenimiento o administrador"""
    message = "Se requiere acceso de mantenimiento."
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['maintenance', 'admin', 'manager']


class IsSecurity(BasePermission):
    """Personal de seguridad o administrador"""
    message = "Se requiere acceso de seguridad."
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['security', 'admin', 'manager']


class CanModifyUser(BasePermission):
    """Usuario solo puede modificar su propio perfil, admins pueden modificar cualquiera"""
    message = "No puedes modificar este usuario."
    
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'admin':
            return True
        return request.user == obj


class CanModifyIncident(BasePermission):
    """
    - Reporter puede ver/modificar su incidente
    - Manager/Admin pueden ver/modificar cualquiera
    - Assigned staff pueden ver el suyo
    """
    def has_object_permission(self, request, view, obj):
        if request.user.role in ['admin', 'manager']:
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
        if request.user.role in ['admin', 'manager']:
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
        if request.user.role in ['admin', 'manager']:
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
    - Resident can access own apartment data
    - Manager/Admin can access any apartment
    """
    def has_object_permission(self, request, view, obj):
        if request.user.role in ['admin', 'manager']:
            return True
        # Resident can access own apartment
        from residents.models import Resident
        try:
            resident = Resident.objects.get(user=request.user, apartment=obj)
            return resident.is_current
        except Resident.DoesNotExist:
            return False
