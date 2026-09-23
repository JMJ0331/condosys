"""
Context processor: expone al template los módulos habilitados para el rol del
usuario autenticado (se usa en el aside del menú lateral). Ocultado 100%
server-side: los módulos no permitidos ni siquiera llegan al HTML.
"""

from accounts.permissions import ROLES_GESTION, ROLES_SEGURIDAD, ROLES_RESIDENTE, ROLES_TODOS

# Roles que pueden crear/editar/eliminar en cada módulo (mirror de los
# decoradores @role_required de las vistas de función).
ROL_CREADOR = {
    'inicio': (),
    'departamentos': ROLES_GESTION,
    'residentes': ROLES_GESTION,
    'propietarios': ROLES_GESTION,
    'pagos': ROLES_GESTION,
    'mantenimientos': ROLES_GESTION,
    'incidencias': ROLES_RESIDENTE,
    'solicitudes': ROLES_GESTION,
    'visitantes': ROLES_SEGURIDAD,
    'areas_comunes': ROLES_GESTION,
    'reservas': ROLES_RESIDENTE,
    'comunicados': ROLES_GESTION,
    'reportes': ROLES_GESTION,
    'residencial': ROLES_GESTION,
}
ROL_EDITOR = {
    'inicio': (),
    'departamentos': ROLES_GESTION,
    'residentes': ROLES_GESTION,
    'propietarios': ROLES_GESTION,
    'pagos': ROLES_GESTION,
    'mantenimientos': ROLES_GESTION,
    'incidencias': ROLES_GESTION,
    'solicitudes': ROLES_GESTION,
    'visitantes': ROLES_SEGURIDAD,
    'areas_comunes': ROLES_GESTION,
'reservas': ROLES_RESIDENTE,
    'comunicados': ROLES_GESTION,
    'reportes': ROLES_GESTION,
    'residencial': ('admin',),
}
ROL_ELIMINADOR = {
    'inicio': (),
    'departamentos': ROLES_GESTION,
    'residentes': ROLES_GESTION,
    'propietarios': ROLES_GESTION,
    'pagos': ROLES_GESTION,
    'mantenimientos': ROLES_GESTION,
    'incidencias': ROLES_GESTION,
    'solicitudes': ROLES_GESTION,
    'visitantes': ROLES_SEGURIDAD,
    'areas_comunes': ROLES_GESTION,
    'reservas': ROLES_GESTION,
    'comunicados': ROLES_GESTION,
    'reportes': ROLES_GESTION,
    'residencial': ('admin',),
}


MODULOS = [
    {
        'clave': 'inicio',
        'nombre': 'Inicio',
        'url': 'inicio',
        'activo_en': ['inicio'],
        'icono': 'images/icons/blancos/Container_white.svg',
        'alt': 'home-icon',
        'roles': ROLES_TODOS,
    },
    {
        'clave': 'departamentos',
        'nombre': 'Departamentos',
        'url': 'departamentos_index',
        'activo_en': [
            'departamentos_index',
            'agregar_departamento',
            'actualizar_departamento',
        ],
        'icono': 'images/icons/blancos/city_white.svg',
        'alt': 'city-icon',
        'roles': ROLES_GESTION + ('propietario',),
    },
    {
        'clave': 'residentes',
        'nombre': 'Residentes',
        'url': 'residentes_index',
        'activo_en': [
            'residentes_index',
            'crear_residente',
            'actualizar_residente',
        ],
        'icono': 'images/icons/blancos/group_white.svg',
        'alt': 'group-icon',
        'roles': ROLES_GESTION + ('propietario',),
    },
    {
        'clave': 'propietarios',
        'nombre': 'Propietarios',
        'url': 'propietarios_index',
        'activo_en': [
            'propietarios_index',
            'crear_propietario',
            'actualizar_propietario',
        ],
        'icono': 'images/icons/blancos/home-user_white.svg',
        'alt': 'propietario-icon',
        'roles': ROLES_GESTION,
    },
    {
        'clave': 'pagos',
        'nombre': 'Pagos',
        'url': 'pagos_index',
        'activo_en': [
            'pagos_index',
            'agregar_pago',
            'actualizar_pago',
            'eliminar_pago',
        ],
        'icono': 'images/icons/blancos/lot-of-cash_white.svg',
        'alt': 'waallet-icon',
        'roles': ROLES_RESIDENTE,
    },
    {
        'clave': 'mantenimientos',
        'nombre': 'Mantenimientos',
        'url': 'mantenimientos_index',
        'activo_en': [
            'mantenimientos_index',
            'agregar_mantenimiento',
            'actualizar_mantenimiento',
        ],
        'icono': 'images/icons/blancos/historic-shield-alt_white.svg',
        'alt': 'settings-icon',
        'roles': ROLES_RESIDENTE,
    },
    {
        'clave': 'incidencias',
        'nombre': 'Incidencias',
        'url': 'incidencias_index',
        'activo_en': [
            'incidencias_index',
            'agregar_incidencia',
            'actualizar_incidencia',
        ],
        'icono': 'images/icons/blancos/warning-triangle_white.svg',
        'alt': 'message-icon',
        'roles': ROLES_RESIDENTE + ('security',),
    },
    {
        'clave': 'solicitudes',
        'nombre': 'Solicitudes',
        'url': 'solicitudes_index',
        'activo_en': [
            'solicitudes_index',
            'agregar_solicitud',
            'actualizar_solicitud',
        ],
        'icono': 'images/icons/blancos/page_white.svg',
        'alt': 'area-icon',
        'roles': ROLES_GESTION,
    },
    {
        'clave': 'visitantes',
        'nombre': 'Visitantes',
        'url': 'visitantes_index',
        'activo_en': [
            'visitantes_index',
            'agregar_visitante',
            'actualizar_visitante',
        ],
        'icono': 'images/icons/blancos/community_white.svg',
        'alt': 'community-icon',
        'roles': ROLES_SEGURIDAD,
    },
    {
        'clave': 'areas_comunes',
        'nombre': 'Áreas Comunes',
        'url': 'areas_comunes_index',
        'activo_en': [
            'areas_comunes_index',
            'agregar_area_comun',
            'actualizar_area_comun',
        ],
        'icono': 'images/icons/blancos/leaf_white.svg',
        'alt': 'neigh-icon',
        'roles': ROLES_RESIDENTE,
    },
    {
        'clave': 'reservas',
        'nombre': 'Reservas',
        'url': 'reservas_index',
        'activo_en': [
            'reservas_index',
            'agregar_reserva',
            'actualizar_reserva',
        ],
        'icono': 'images/icons/blancos/google-docs.svg',
        'alt': 'solicitud-icon',
        'roles': ROLES_RESIDENTE + ('security',),
    },
    {
        'clave': 'comunicados',
        'nombre': 'Comunicados',
        'url': 'comunicados_index',
        'activo_en': [
            'comunicados_index',
            'agregar_comunicado',
            'actualizar_comunicado',
        ],
        'icono': 'images/icons/blancos/voice_white.svg',
        'alt': 'chat-icon',
        'roles': ROLES_RESIDENTE + ('security',),
    },
    {
        'clave': 'reportes',
        'nombre': 'Reportes',
        'url': 'reportes_index',
        'activo_en': ['reportes_index'],
        'icono': 'images/icons/blancos/reports_white.svg',
        'alt': 'reports-icon',
        'roles': ROLES_GESTION,
    },
    {
        'clave': 'residencial',
        'nombre': 'Residencial',
        'url': 'residencial_index',
        'activo_en': ['residencial_index'],
        'icono': 'images/icons/blancos/residencial.svg',
        'alt': 'residencial-icon',
        'roles': ('admin',),
        'clase_extra': 'opt-residencial',
    },
]


def modulos_usuario(request):
    """Devuelve los módulos visibles según el rol del usuario autenticado."""
    if not hasattr(request, 'user') or not request.user.is_authenticated:
        return {'modulos_habilitados': MODULOS, 'modulos_acceso': {m['clave']: False for m in MODULOS}}
    role = request.user.role
    habilitados = [modulo for modulo in MODULOS if role in modulo['roles']]
    modulos_acceso = {modulo['clave']: role in modulo['roles'] for modulo in MODULOS}
    return {'modulos_habilitados': habilitados, 'modulos_acceso': modulos_acceso}


def _modulo_actual(request):
    """Clave del módulo de la URL actual, o '' si no corresponde a ninguno."""
    if not hasattr(request, 'resolver_match') or not request.resolver_match:
        return ''
    url_name = request.resolver_match.url_name
    for modulo in MODULOS:
        if url_name in modulo['activo_en']:
            return modulo['clave']
    return ''


def permisos_modulo(request):
    """Expone puede_crear / puede_editar / puede_eliminar según el rol y el
    módulo de la URL actual (server-side, mirror de @role_required), además de
    un mapa permisos_modulos con los permisos por módulo para el rol.""" 
    if not hasattr(request, 'user') or not request.user.is_authenticated:
        return {
            'puede_crear': False, 'puede_editar': False, 'puede_eliminar': False,
            'permisos_modulos': {},
        }
    role = request.user.role
    permisos_modulos = {
        modulo['clave']: {
            'crear': role in ROL_CREADOR.get(modulo['clave'], ()),
            'editar': role in ROL_EDITOR.get(modulo['clave'], ()),
            'eliminar': role in ROL_ELIMINADOR.get(modulo['clave'], ()),
        }
        for modulo in MODULOS
    }
    clave = _modulo_actual(request)
    clave_perms = permisos_modulos.get(clave, {})
    return {
        'puede_crear': clave_perms.get('crear', False),
        'puede_editar': clave_perms.get('editar', False),
        'puede_eliminar': clave_perms.get('eliminar', False),
        'permisos_modulos': permisos_modulos,
    }