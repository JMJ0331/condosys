# CONDOSYS — Modelo Entidad-Relación

Diagrama generado a partir de los `models.py` de cada app (Django 6.1).
Todas las claves primarias son `UUIDField` salvo donde se indique.
Los nombres están en español; entre paréntesis el modelo/campo real del código.

## Diagrama general

```mermaid
erDiagram
    JARDIN ||--o{ EDIFICIO : "contiene"
    JARDIN ||--o{ AREA_COMUN_GENERAL : "agrupa"
    JARDIN ||--o{ COMUNICADO : "publica"
    JARDIN ||--o{ USUARIO : "filtra jerarquia"

    EDIFICIO ||--o{ APARTAMENTO : "contiene"

    PROPIETARIO ||--o{ APARTAMENTO : "posee"
    USUARIO ||--o{ PROPIETARIO : "perfil"

    APARTAMENTO ||--o{ RESIDENTE : "ocupa"
    USUARIO ||--o{ RESIDENTE : "perfil"

    RESIDENTE ||--o{ PAGO : "paga"
    APARTAMENTO ||--o{ PAGO : "factura"
    USUARIO ||--o{ PAGO : "registra"

    APARTAMENTO ||--o{ CARGO_MANTENIMIENTO : "aplica"

    APARTAMENTO ||--o{ INCIDENCIA : "reporta"
    RESIDENTE ||--o{ INCIDENCIA : "genera"
    USUARIO ||--o{ INCIDENCIA : "reporta_asigna"
    INCIDENCIA ||--o{ IMAGEN_INCIDENCIA : "tiene"
    INCIDENCIA ||--o{ HISTORIAL_INCIDENCIA : "historial"

    APARTAMENTO ||--o{ SOLICITUD : "solicita"
    RESIDENTE ||--o{ SOLICITUD : "genera"

    AREA_COMUN ||--o{ RESERVA : "reservada"
    APARTAMENTO ||--o{ RESERVA : "reserva"
    RESIDENTE ||--o{ RESERVA : "solicita"
    USUARIO ||--o{ RESERVA : "reserva_aprueba"

    APARTAMENTO ||--o{ VISITANTE : "visita"
    USUARIO ||--o{ VISITANTE : "registra_autoriza"

    JARDIN ||--o{ COMUNICADO : "emisor"
    USUARIO ||--o{ COMUNICADO : "envia"

    USUARIO ||--o{ NOTIFICACION : "recibe"

    USUARIO ||--o{ MENSAJE_CHAT : "envia"
    USUARIO ||--o{ MENSAJE_CHAT : "recibe"
    GRUPO_CHAT ||--o{ MENSAJE_CHAT : "agrupa"

    USUARIO ||--o{ TOKEN_RECUPERACION : "solicita"

    USUARIO ||--o{ REGISTRO_AUDITORIA : "genera"
    REGISTRO_AUDITORIA ||--o{ DETALLE_AUDITORIA : "detalla"

    USUARIO {
        uuid id PK
        string correo UK
        string telefono
        string documento UK
        string rol
        string estado
        uuid jardin FK
        datetime creado_en
    }

    JARDIN {
        uuid id PK
        string nombre UK
        string ubicacion
        bool activo
    }

    EDIFICIO {
        uuid id PK
        uuid jardin FK
        string nombre
        string torre
        string bloque
        int numero_pisos
    }

    APARTAMENTO {
        uuid id PK
        uuid edificio FK
        uuid propietario FK
        string nombre
        int piso
        string estado
    }

    PROPIETARIO {
        uuid id PK
        uuid usuario FK
        string nombre_completo
        string cedula UK
        string telefono
        bool activo
    }

    RESIDENTE {
        uuid id PK
        uuid usuario FK
        uuid apartamento FK
        string nombre_completo
        string cedula UK
        string tipo_relacion
        bool activo
    }

    PAGO {
        uuid id PK
        uuid apartamento FK
        uuid residente FK
        uuid registrado_por FK
        decimal monto
        string concepto
        date periodo
        string estado
    }

    CARGO_MANTENIMIENTO {
        uuid id PK
        uuid apartamento FK
        string concepto
        string periodicidad
        decimal monto
        bool activo
    }

    INCIDENCIA {
        uuid id PK
        uuid apartamento FK
        uuid residente FK
        uuid reportado_por FK
        uuid asignado_a FK
        string categoria
        string prioridad
        string estado
    }

    IMAGEN_INCIDENCIA {
        uuid id PK
        uuid incidencia FK
        string url
    }

    HISTORIAL_INCIDENCIA {
        uuid id PK
        uuid incidencia FK
        uuid cambiado_por FK
        string estado_anterior
        string estado_nuevo
    }

    SOLICITUD {
        uuid id PK
        uuid apartamento FK
        uuid residente FK
        string tipo_solicitud
        string estado
    }

    AREA_COMUN {
        uuid id PK
        string nombre
        string tipo_area
        int capacidad
        string estado
    }

    AREA_COMUN_GENERAL {
        uuid id PK
        uuid jardin FK
        string nombre
        int capacidad
        bool activo
    }

    RESERVA {
        uuid id PK
        uuid area_comun FK
        uuid apartamento FK
        uuid residente FK
        uuid reservado_por FK
        uuid aprobado_por FK
        datetime inicio
        datetime fin
        string estado
    }

    VISITANTE {
        uuid id PK
        uuid apartamento FK
        uuid registrado_por FK
        uuid autorizado_por FK
        string nombre
        string documento
        string estado
        datetime entrada_prevista
    }

    COMUNICADO {
        uuid id PK
        uuid jardin FK
        uuid remitente FK
        string titulo
        string categoria
        string tipo_destino
        uuid id_destino
    }

    NOTIFICACION {
        uuid id PK
        uuid usuario FK
        string tipo
        string titulo
        uuid id_relacionado
        bool leida
    }

    GRUPO_CHAT {
        int id PK
        string nombre UK
    }

    MENSAJE_CHAT {
        uuid id PK
        uuid remitente FK
        uuid destinatario FK
        int grupo FK
        string mensaje
    }

    TOKEN_RECUPERACION {
        uuid id PK
        uuid usuario FK
        string token UK
        datetime expira_en
        datetime usado_en
    }

    REGISTRO_AUDITORIA {
        uuid id PK
        uuid usuario FK
        string accion
        string entidad
        uuid id_entidad
    }

    DETALLE_AUDITORIA {
        int id PK
        uuid registro FK
        string clave
        string valor
    }
```

## Equivalencia con el código

| Entidad (diagrama) | Modelo (código) | App |
|---|---|---|
| `USUARIO` | `User` | `accounts` |
| `JARDIN` | `Garden` | `structure` |
| `EDIFICIO` | `Building` | `structure` |
| `APARTAMENTO` | `Apartment` | `structure` |
| `PROPIETARIO` | `Propietario` | `propietarios` |
| `RESIDENTE` | `Resident` | `residents` |
| `PAGO` | `Payment` | `payments` |
| `CARGO_MANTENIMIENTO` | `MaintenanceCharge` | `maintenance` |
| `INCIDENCIA` | `Incident` | `incidents` |
| `IMAGEN_INCIDENCIA` | `IncidentImage` | `incidents` |
| `HISTORIAL_INCIDENCIA` | `IncidentHistory` | `incidents` |
| `SOLICITUD` | `Solicitud` | `solicitudes` |
| `AREA_COMUN` | `AreaComun` | `areas_comunes` |
| `AREA_COMUN_GENERAL` | `CommonArea` | `reservations` |
| `RESERVA` | `Reservation` | `reservations` |
| `VISITANTE` | `Visitor` | `visitors` |
| `COMUNICADO` | `Communication` | `communications` |
| `NOTIFICACION` | `Notification` | `notifications` |
| `GRUPO_CHAT` | `ChatGroup` | `chat` |
| `MENSAJE_CHAT` | `ChatMessage` | `chat` |
| `TOKEN_RECUPERACION` | `PasswordResetToken` | `login` |
| `REGISTRO_AUDITORIA` | `AuditLog` | `reports` |
| `DETALLE_AUDITORIA` | `AuditLogDetail` | `reports` |

## Entidades independientes (registro único / configuración)

Estos modelos no tienen claves foráneas a otras entidades del flujo principal:

| Entidad | App | Descripción |
|---|---|---|
| `Residencial` | `residencial` | Datos del residencial (registro único, `obtener_unico()`). |
| `IntegracionIA` | `configuracion` | Configuración del proveedor/modelo de IA (`obtener_unica()`). |

## Relaciones destacadas

- **Jerarquía física**: `JARDIN → EDIFICIO → APARTAMENTO` (`CASCADE`).
- **Usuario ↔ perfil**: `USUARIO` se vincula opcionalmente a un `RESIDENTE` (`resident_profiles`) o a un `PROPIETARIO` (`propietario_profiles`).
- **Propiedad vs ocupación**: `Apartamento.owner` apunta a `PROPIETARIO` (`SET_NULL`); los ocupantes se modelan como `RESIDENTE` apuntando al `APARTAMENTO`.
- **Pagos**: `PAGO` referencia `APARTAMENTO` + `RESIDENTE` (`PROTECT`) y guarda `registrado_por` (`USUARIO`, `SET_NULL`).
- **Incidencias**: `INCIDENCIA` cuelga de `APARTAMENTO` (`CASCADE`), con `reportado_por`/`asignado_a` (`USUARIO`), más `IMAGEN_INCIDENCIA` e `HISTORIAL_INCIDENCIA`.
- **Reservas**: `RESERVA` cruza `AREA_COMUN`, `APARTAMENTO`, `RESIDENTE` y `USUARIO` (quien reserva/aprueba).
- **Visitantes**: `VISITANTE` cuelga de `APARTAMENTO` con `registrado_por`/`autorizado_por` (`USUARIO`).
- **Mensajería**: `MENSAJE_CHAT` usa `remitente`, `destinatario` opcional (privado) y `grupo` opcional (grupal).

## Notas de implementación

- `reservations.CommonArea` (`AREA_COMUN_GENERAL`, FK a `JARDIN`) y `areas_comunes.AreaComun` (`AREA_COMUN`, independiente) coexisten; `Reservation.common_area` apunta a **`areas_comunes.AreaComun`**.
- `Communication.target_id` (`id_destino`) y `Notification.related_id` (`id_relacionado`) son `UUIDField` **sin FK** (referencias polimórficas por `target_type`/`type`).
- `User.garden` (`jardin`, `SET_NULL`) se usa solo para filtrar por jerarquía.
