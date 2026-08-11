# CONDOSYS — FASE 1: ARQUITECTURA Y DISEÑO TÉCNICO

**Documento de aprobación previo a implementación**

---

## A. RESUMEN DEL SISTEMA

**CONDOSYS** es una plataforma web profesional de administración y gestión integral para residenciales de apartamentos. Permite a administradores, residentes y personal de mantenimiento gestionar de forma centralizada:

- Estructura física: Jardines → Edificios → Departamentos
- Residentes y ocupantes
- Pagos y facturación
- Incidencias y solicitudes de servicio
- Visitantes y control de accesos
- Reservas de áreas comunes
- Mantenimiento preventivo y correctivo
- Comunicaciones y notificaciones en tiempo real
- Chat interno para coordinación

El sistema respeta una arquitectura jerárquica clara donde las entidades están relacionadas en una estructura de árbol bien definida.

---

## B. REQUISITOS IDENTIFICADOS DEL DOCUMENTO

### Módulos principales
1. **Autenticación y Autorización** — Login, sesiones, roles, permisos
2. **Gestión de Estructura** — Jardines, edificios, departamentos
3. **Residentes** — Registros, ocupantes, documentación
4. **Pagos** — Facturas, estado de pago, historial
5. **Incidencias** — Reportes, asignación, seguimiento, resolución
6. **Visitantes y Accesos** — Registro de visitantes, control de entrada
7. **Reservas** — Espacios comunes, calendario de disponibilidad
8. **Mantenimiento** — Órdenes de trabajo, ejecución, reportes
9. **Comunicaciones** — Avisos, notificaciones, circular
10. **Chat en Tiempo Real** — Mensajería interna, grupos de comunicación
11. **Dashboard** — Resumen de actividad, métricas, alertas

### Características críticas
- **Workflows con estado**: Incidencias, pagos y mantenimiento siguen procesos definidos con transiciones de estado
- **Notificaciones**: Cambios de estado deben notificarse a actores relevantes
- **Jerarquía de datos**: Relaciones padre-hijo en Garden → Building → Apartment
- **Seguridad**: Autorización en backend, sin confianza en frontend únicamente
- **Tiempo real**: WebSockets para chat, notificaciones y actualizaciones críticas

---

## C. ROLES Y PERMISOS

### Roles principales

#### 1. **Administrador (Admin)**
- Gestión completa del sistema
- Crear/editar/eliminar jardines, edificios, departamentos
- Gestión de usuarios y asignación de roles
- Ver reportes integrales
- Gestión de pagos y facturas
- Resolución final de incidencias
- Permisos: CRUD en todos los módulos

#### 2. **Encargado de Administración (Manager)**
- Gestión de edificios asignados
- Asignación de incidencias
- Seguimiento de pagos
- Comunicación con residentes
- No puede: Crear usuarios, eliminar datos, ver reportes sensibles
- Permisos: Lectura completa, edición limitada

#### 3. **Residente**
- Ver su propio perfil y departamento
- Reportar incidencias
- Ver estado de pagos personales
- Reservar áreas comunes
- Registrar visitantes
- Recibir notificaciones
- Participar en chat
- Permisos: Lectura/escritura de datos propios

#### 4. **Personal de Mantenimiento**
- Ver órdenes de trabajo asignadas
- Actualizar estado de mantenimiento
- Reportar problemas encontrados
- Recibir notificaciones de órdenes
- Permisos: Lectura de órdenes, escritura de actualizaciones

#### 5. **Seguridad/Control de Acceso**
- Registrar visitantes
- Ver registro de accesos
- Alertas de seguridad
- Permisos: Lectura de accesos, escritura de registros

### Matriz de permisos
```
Recurso                  | Admin | Manager | Residente | Mantenimiento | Seguridad
─────────────────────────┼───────┼─────────┼───────────┼───────────────┼──────────
Jardines                 | CRUD  | R       | R         | R             | R
Edificios                | CRUD  | RU*     | R         | R             | R
Departamentos            | CRUD  | RU*     | R(own)    | R             | R
Residentes               | CRUD  | RU*     | R(own)    | R             | R
Pagos                    | CRUD  | R       | R(own)    | —             | —
Incidencias              | CRUD  | CRU*    | CR(own)   | RU(assigned)  | —
Visitantes               | R     | R       | CRU(own)  | —             | CRUD
Reservas                 | R     | R       | CRU(own)  | —             | —
Mantenimiento            | CRUD  | R       | —         | RU(assigned)  | —
Comunicaciones           | CRUD  | RU      | R         | —             | —
Notificaciones           | —     | —       | R         | R             | R
Chat                     | —     | RU      | RU        | RU            | —

* = con restricciones de su ámbito
R = Lectura | C = Crear | U = Actualizar | D = Eliminar
```

---

## D. MÓDULOS FUNCIONALES

### 1. **Módulo de Autenticación**
- Login con email/contraseña
- Recuperación de contraseña
- Sesiones seguras con tokens
- Logout
- Rol detectado automáticamente
- Redirección a dashboard según rol

### 2. **Módulo de Estructura (Jardín-Edificio-Departamento)**
- CRUD de jardines
- CRUD de edificios (filtro dependiente del jardín)
- CRUD de departamentos (filtro dependiente del edificio)
- Estados de departamento: Vacío, Ocupado, En reparación, Bloqueado
- Visualización jerárquica

### 3. **Módulo de Residentes**
- Crear residente vinculado a departamento
- Un departamento puede tener múltiples residentes (ocupantes)
- Documentación: Cédula, contrato, referencias
- Estados: Activo, Inactivo, En verifi­cación
- Historial de residencia

### 4. **Módulo de Pagos**
- Estados de pago: Pendiente, En riego, Vencido, Pagado, Anulado
- Historial de pagos
- Generación de facturas
- Recordatorios automáticos
- Reportes de cobranza
- Integración con métodos de pago (propuesta: Stripe/PayPal — a confirmar)

### 5. **Módulo de Incidencias**
Workflow completo:
```
Residente reporta
    ↓
Admin/Manager revisa y asigna
    ↓
Mantenimiento recibe
    ↓
Ejecución
    ↓
Resolución y validación
    ↓
Notificación al residente
```
- Estados: Nueva, Asignada, En progreso, Resuelta, Cerrada, Rechazada
- Categorías: Plomería, Electricidad, Estructural, Limpieza, Otros
- Prioridad: Baja, Normal, Alta, Urgente
- Comentarios y seguimiento
- Tiempo promedio de resolución (métrica)

### 6. **Módulo de Visitantes y Accesos**
- Registro anticipado de visitantes (por residente)
- Validación en entrada (seguridad)
- Horarios de entrada/salida
- Motivo de visita
- Historial de accesos
- Alertas de visitantes rechazados o con incidencias

### 7. **Módulo de Reservas (Áreas Comunes)**
- Listado de áreas disponibles: Salón, Cancha, Parqueadero, Piscina, Gym, etc.
- Calendario de disponibilidad
- Residente puede reservar dentro de políticas
- Cancelación con límite de tiempo
- Confirmación automática
- Recordatorios

### 8. **Módulo de Mantenimiento**
Workflow:
```
Problema identificado (incidencia o preventivo)
    ↓
Orden de trabajo generada
    ↓
Asignado a personal
    ↓
Ejecución
    ↓
Cierre y validación
    ↓
Reporte
```
- Tipos: Preventivo, Correctivo, Emergencia
- Estados: Programado, En proceso, Completado, Cancelado
- Historial de mantenimiento por departamento
- Reportes de frecuencia y costos

### 9. **Módulo de Comunicaciones**
- Avisos generales
- Circulares dirigidas
- Anuncios por edificio
- Avisos de eventos
- Preferencias de notificación por residente
- Archivo de comunicaciones

### 10. **Módulo de Chat en Tiempo Real**
- Chat general (todos los residentes)
- Chats privados (Admin ↔ Residente)
- Chats de grupo (por edificio, por área de mantenimiento)
- Historial de mensajes
- Notificaciones en tiempo real
- Indicadores de escritura (typing...)

### 11. **Dashboard**
Muestra según rol:
- **Admin**: Resumen global, métricas de pagos, incidencias pendientes, ocupación
- **Manager**: Resumen de su edificio, incidencias asignadas, pagos vencidos
- **Residente**: Sus datos, pagos, incidencias reportadas, reservas próximas
- **Mantenimiento**: Órdenes asignadas, próximas tareas
- **Seguridad**: Visitantes esperados, accesos recientes

---

## E. WORKFLOWS PRINCIPALES DERIVADOS DEL DOCUMENTO

### E.1. Workflow: Reportar Incidencia (Residente → Resolución)

```
1. Residente accede a "Incidencias"
2. Click en "Reportar Nueva"
3. Formulario:
   - Categoría (obligatorio)
   - Descripción (obligatorio)
   - Fotos (opcional)
   - Prioridad (por defecto: Normal)
   - Ubicación (su departamento, prellenado)
4. Validación frontend y backend
5. Se crea registro con estado "Nueva"
6. Notificación a Admin/Manager
7. Admin/Manager recibe notificación → Dashboard → Lista de incidencias
8. Manager asigna a personal de mantenimiento
9. Cambio de estado a "Asignada"
10. Notificación a Mantenimiento
11. Mantenimiento recibe en su dashboard
12. Actualiza estado a "En progreso"
13. Realiza trabajo
14. Cierra con estado "Resuelta"
15. Residente recibe notificación y puede validar
16. Si valida: Estado "Cerrada"
17. Si rechaza: vuelve a "Asignada" con comentario
```

**Eventos y notificaciones:**
- Residente reporta → Admin notificado
- Manager asigna → Mantenimiento notificado
- Mantenimiento inicia → Residente notificado
- Mantenimiento resuelve → Residente notificado
- Residente valida → Admin notificado (reporte cerrado)

---

### E.2. Workflow: Gestión de Pagos

```
1. Factura generada mensualmente (automático o manual)
   - Monto: Mantenimiento + servicios + otros
   - Plazo: hasta día X del mes siguiente
   - Estado: Pendiente
2. Notificación automática enviada
3. Residente puede:
   - Ver factura
   - Descargar
   - Pagar en línea (integraciones futuras)
4. Si no paga a tiempo:
   - Cambio a "En riesgo" (5 días antes)
   - Notificación de cortesía
5. Si vence:
   - Cambio a "Vencido"
   - Notificación urgente
6. Admin puede:
   - Registrar pago manualmente
   - Generar recibos
   - Ver histórico
7. Reportes de morosidad
```

---

### E.3. Workflow: Crear Departamento (Jerárquico)

```
1. Admin accede a "Gestión de Estructura"
2. Selecciona "Jardín" → "Edificio"
3. Click en "Crear Departamento"
4. Formulario:
   - Jardín (readonly si viene de un jardín)
   - Edificio (depende de jardín seleccionado)
   - Número (ej: 101, 102)
   - Piso (1, 2, 3...)
   - Área en m² (opcional)
   - Tipo (Apartamento, Casa, Local)
   - Estado (Vacío, Ocupado, etc.)
5. Validación:
   - No puede existir número duplicado en el edificio
   - Edificio debe pertenecer al jardín seleccionado
6. Guardado
7. Registro en auditoría
```

---

### E.4. Workflow: Registrar Residente en Departamento

```
1. Admin/Manager accede a Departamento específico
2. Click "Agregar Residente"
3. Formulario:
   - Email (único a nivel del sistema)
   - Nombre completo
   - Teléfono
   - Documento
   - Rol: Propietario o Ocupante
   - Fecha de inicio
4. Validación:
   - Email único
   - Documento válido
5. Sistema genera contraseña temporal
6. Email de bienvenida enviado
7. Residente puede cambiar contraseña en primer login
8. Estado de residente: "En verificación" → "Activo"
```

---

### E.5. Workflow: Registrar Visitante y Control de Acceso

```
1. Residente accede a "Visitantes"
2. Click "Registrar Visitante"
3. Formulario:
   - Nombre del visitante
   - Documento/Referencia
   - Fecha y hora de entrada
   - Fecha y hora de salida (estimada)
   - Motivo
   - Vehículo (placa, si aplica)
4. Validación:
   - Hora de entrada debe ser futura
   - Hora de salida después de entrada
5. Registro guardado
6. Notificación a Seguridad
7. En acceso, seguridad valida visitante
   - Busca registro
   - Autoriza o rechaza
   - Si autoriza: Registra hora real de entrada
   - Si rechaza: Registra en historial
8. Visitante sale → Registra hora de salida
9. Reportes de visitantes por departamento
```

---

### E.6. Workflow: Reserva de Área Común

```
1. Residente accede a "Reservas"
2. Selecciona área: Salón de eventos, Cancha, etc.
3. Ve calendario de disponibilidad
4. Selecciona fecha y horario
5. Formulario:
   - Motivo (fiesta, reunión, etc.)
   - Número de personas (estimado)
   - Servicios adicionales (sillas, mesas, etc.) — si aplica
   - Aceptación de términos
6. Validación:
   - Hora debe estar disponible
   - Residente no debe tener reservas simultaneas
   - Residente debe estar al día en pagos (opcional, a definir)
7. Confirmación automática
8. Notificación a Residente
9. Recordatorio 24h antes
10. Estado: Confirmada, Completada, Cancelada
```

---

## F. ARQUITECTURA GENERAL

```
┌───────────────────────────────────────────────────────────────────┐
│                              CONDOSYS                             │
├─────────────────────────────┬─────────────────────────────────────┤
│                             │                                     │
│        FRONTEND             │           BACKEND                   │
│                             │                                     │
│  ┌─────────────────────┐   │   ┌──────────────────────────────┐   │
│  │  HTML + CSS + JS    │   │   │  Django                      │   │
│  │  (Vanilla)          │   │   │  ├─ Views/Serializers       │   │
│  │                     │   │   │  ├─ Models                  │   │
│  │  ┌─────────────────┐│   │   │  ├─ URLs                    │   │
│  │  │ Components:     ││   │   │  ├─ Forms                   │   │
│  │  │ - Header        ││   │   │  ├─ Auth                    │   │
│  │  │ - Sidebar       ││   │   │  └─ Permissions             │   │
│  │  │ - Dashboard     ││   │   │                              │   │
│  │  │ - Tables        ││   │   │  ┌──────────────────────────┐   │
│  │  │ - Forms         ││   │   │  │ Django Channels          │   │
│  │  │ - Modals        ││   │   │  │ ├─ Consumers             │   │
│  │  │ - Alerts        ││   │   │  │ ├─ Routing               │   │
│  │  │ - Loading       ││   │   │  │ └─ Groups                │   │
│  │  │ - Cards         ││   │   │  └──────────────────────────┘   │
│  │  └─────────────────┘│   │   │                              │   │
│  │                     │   │   │  WebSockets                  │   │
│  │  API Client:        │   │   │  ├─ Chat                    │   │
│  │  ├─ Fetch API       │   │   │  ├─ Notificaciones          │   │
│  │  └─ WebSocket JS    │   │   │  └─ Actualizaciones RT      │   │
│  └─────────────────────┘   │   └──────────────────────────────┘   │
│                             │                                     │
└─────────────────────────────┴─────────────────────────────────────┘
                                       ↓
                    ┌──────────────────────────────────┐
                    │                                  │
                    │  Supabase + PostgreSQL           │
                    │                                  │
                    │  ┌────────────────────────────┐  │
                    │  │ Tablas relaciones:         │  │
                    │  │ - Gardens                  │  │
                    │  │ - Buildings                │  │
                    │  │ - Apartments               │  │
                    │  │ - Residents                │  │
                    │  │ - Payments                 │  │
                    │  │ - Incidents                │  │
                    │  │ - Visitors                 │  │
                    │  │ - Reservations             │  │
                    │  │ - Maintenance              │  │
                    │  │ - Communications           │  │
                    │  │ - Messages/Chat            │  │
                    │  │ - Notifications            │  │
                    │  └────────────────────────────┘  │
                    │                                  │
                    └──────────────────────────────────┘
```

### Flujo de comunicación

```
1. Usuario interactúa con Frontend (HTML/CSS/JS)
   ↓
2. JavaScript envía petición:
   - HTTP (GET, POST, PUT, DELETE) para operaciones CRUD normales
   - WebSocket para chat, notificaciones, actualizaciones RT
   ↓
3. Django recibe, procesa:
   - Valida token/sesión
   - Verifica permisos
   - Ejecuta lógica de negocio
   - Valida datos
   ↓
4. Se actualiza PostgreSQL/Supabase
   ↓
5. Django responde al cliente:
   - JSON para HTTP
   - Mensaje WebSocket para RT
   ↓
6. Frontend actualiza DOM
   - Muestra datos
   - Notificaciones
   - Estados
```

---

## G. ESTRUCTURA DE CARPETAS

```
condosys/
│
├── .env.example                    # Variables de entorno template
├── .gitignore                      # Archivos a ignorar
├── README.md                       # Documentación del proyecto
├── requirements.txt                # Dependencias Python
│
├── backend/
│   ├── manage.py                   # Comando Django
│   │
│   ├── config/                     # Configuración del proyecto
│   │   ├── settings.py             # Configuración Django
│   │   ├── urls.py                 # URLs principales
│   │   ├── asgi.py                 # ASGI (WebSockets)
│   │   └── wsgi.py                 # WSGI (HTTP)
│   │
│   ├── apps/                       # Aplicaciones Django
│   │   ├── accounts/               # Auth, usuarios, roles
│   │   │   ├── models.py
│   │   │   ├── views.py
│   │   │   ├── urls.py
│   │   │   ├── forms.py
│   │   │   ├── permissions.py
│   │   │   └── ...
│   │   │
│   │   ├── structure/              # Garden, Building, Apartment
│   │   │   ├── models.py
│   │   │   ├── views.py
│   │   │   ├── urls.py
│   │   │   └── ...
│   │   │
│   │   ├── residents/              # Residentes
│   │   │   ├── models.py
│   │   │   ├── views.py
│   │   │   ├── urls.py
│   │   │   └── ...
│   │   │
│   │   ├── payments/               # Pagos y facturas
│   │   │   ├── models.py
│   │   │   ├── views.py
│   │   │   ├── urls.py
│   │   │   ├── services.py         # Lógica de pagos
│   │   │   └── ...
│   │   │
│   │   ├── incidents/              # Incidencias
│   │   │   ├── models.py
│   │   │   ├── views.py
│   │   │   ├── urls.py
│   │   │   ├── services.py         # Workflow de incidencias
│   │   │   └── ...
│   │   │
│   │   ├── visitors/               # Visitantes
│   │   │   ├── models.py
│   │   │   ├── views.py
│   │   │   ├── urls.py
│   │   │   └── ...
│   │   │
│   │   ├── reservations/           # Reservas
│   │   │   ├── models.py
│   │   │   ├── views.py
│   │   │   ├── urls.py
│   │   │   └── ...
│   │   │
│   │   ├── maintenance/            # Mantenimiento
│   │   │   ├── models.py
│   │   │   ├── views.py
│   │   │   ├── urls.py
│   │   │   ├── services.py
│   │   │   └── ...
│   │   │
│   │   ├── communications/         # Avisos y circulares
│   │   │   ├── models.py
│   │   │   ├── views.py
│   │   │   ├── urls.py
│   │   │   └── ...
│   │   │
│   │   ├── notifications/          # Notificaciones
│   │   │   ├── models.py
│   │   │   ├── views.py
│   │   │   ├── services.py         # Envío de notificaciones
│   │   │   └── ...
│   │   │
│   │   └── chat/                   # Chat en tiempo real
│   │       ├── models.py
│   │       ├── consumers.py        # WebSocket consumers
│   │       ├── routing.py          # WebSocket routing
│   │       ├── views.py
│   │       ├── urls.py
│   │       └── ...
│   │
│   ├── utils/                      # Utilidades compartidas
│   │   ├── decorators.py           # Decoradores (permisos, etc)
│   │   ├── helpers.py              # Funciones auxiliares
│   │   └── ...
│   │
│   └── static/                     # CSS/JS estáticos (si aplica)
│
├── frontend/
│   │
│   ├── pages/                      # Páginas HTML
│   │   ├── index.html              # Login
│   │   ├── dashboard.html          # Dashboard general
│   │   ├── structure.html          # Gestión de estructura
│   │   ├── residents.html
│   │   ├── payments.html
│   │   ├── incidents.html
│   │   ├── visitors.html
│   │   ├── reservations.html
│   │   ├── maintenance.html
│   │   ├── communications.html
│   │   ├── chat.html
│   │   └── profile.html
│   │
│   ├── src/
│   │   │
│   │   ├── css/
│   │   │   ├── base/
│   │   │   │   ├── reset.css       # Reset/normalize
│   │   │   │   ├── variables.css   # Variables CSS (colores, fuentes)
│   │   │   │   └── typography.css  # Tipografía
│   │   │   │
│   │   │   ├── components/
│   │   │   │   ├── header.css
│   │   │   │   ├── sidebar.css
│   │   │   │   ├── button.css
│   │   │   │   ├── form.css
│   │   │   │   ├── table.css
│   │   │   │   ├── card.css
│   │   │   │   ├── modal.css
│   │   │   │   ├── alert.css
│   │   │   │   ├── badge.css
│   │   │   │   └── ...
│   │   │   │
│   │   │   ├── layouts/
│   │   │   │   ├── dashboard-layout.css
│   │   │   │   └── auth-layout.css
│   │   │   │
│   │   │   ├── pages/
│   │   │   │   ├── dashboard.css
│   │   │   │   ├── structure.css
│   │   │   │   ├── residents.css
│   │   │   │   └── ...
│   │   │   │
│   │   │   ├── utilities/
│   │   │   │   ├── spacing.css     # Padding, margin utilities
│   │   │   │   ├── display.css     # Display utilities
│   │   │   │   ├── media-queries.css
│   │   │   │   └── animations.css
│   │   │   │
│   │   │   └── main.css            # Archivo principal que importa todo
│   │   │
│   │   ├── js/
│   │   │   │
│   │   │   ├── core/
│   │   │   │   ├── api-client.js   # Cliente HTTP/WebSocket
│   │   │   │   ├── auth.js         # Manejo de autenticación
│   │   │   │   ├── router.js       # Enrutamiento de páginas
│   │   │   │   ├── storage.js      # LocalStorage/SessionStorage
│   │   │   │   └── utils.js        # Utilidades globales
│   │   │   │
│   │   │   ├── components/
│   │   │   │   ├── header.js
│   │   │   │   ├── sidebar.js
│   │   │   │   ├── form-handler.js
│   │   │   │   ├── table.js
│   │   │   │   ├── modal.js
│   │   │   │   ├── alert.js
│   │   │   │   ├── notification.js  # Mostrar notificaciones
│   │   │   │   └── ...
│   │   │   │
│   │   │   ├── pages/
│   │   │   │   ├── dashboard.js
│   │   │   │   ├── structure.js
│   │   │   │   ├── residents.js
│   │   │   │   ├── payments.js
│   │   │   │   ├── incidents.js
│   │   │   │   ├── visitors.js
│   │   │   │   ├── reservations.js
│   │   │   │   ├── maintenance.js
│   │   │   │   ├── communications.js
│   │   │   │   ├── chat.js         # Chat con WebSockets
│   │   │   │   └── ...
│   │   │   │
│   │   │   └── main.js             # Punto de entrada principal
│   │   │
│   │   └── images/
│   │       ├── icons/              # SVG de iconos
│   │       ├── logo/               # Logo CONDOSYS
│   │       └── ...
│   │
│   └── index.html                  # HTML principal (template base)
│
├── docs/                           # Documentación del proyecto
│   ├── API.md                      # Documentación de endpoints
│   ├── DATABASE.md                 # Diagrama y esquema de BD
│   ├── WORKFLOWS.md                # Workflows detallados
│   └── ...
│
└── tests/                          # Tests automatizados
    ├── unit/
    ├── integration/
    └── ...
```

---

## H. MODELO DE DATOS

### Jerarquía principal: Garden → Building → Apartment

```sql
-- Garden (Jardín)
CREATE TABLE garden (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    location VARCHAR(255),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- Building (Edificio)
CREATE TABLE building (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    garden_id UUID NOT NULL REFERENCES garden(id),
    name VARCHAR(50) NOT NULL,
    number_of_floors INTEGER,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    UNIQUE(garden_id, name)
);

-- Apartment (Departamento)
CREATE TABLE apartment (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    building_id UUID NOT NULL REFERENCES building(id),
    number VARCHAR(20) NOT NULL,
    floor INTEGER,
    area_m2 DECIMAL(8, 2),
    type VARCHAR(30) NOT NULL, -- 'Apartamento', 'Casa', 'Local'
    status VARCHAR(30) NOT NULL DEFAULT 'Vacío', -- Estados: Vacío, Ocupado, En reparación, Bloqueado
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    UNIQUE(building_id, number)
);
```

### Usuarios y Autenticación

```sql
-- User (base para todos los usuarios)
CREATE TABLE user (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    phone VARCHAR(20),
    document VARCHAR(50),
    avatar_url VARCHAR(255),
    role VARCHAR(30) NOT NULL, -- 'admin', 'manager', 'resident', 'maintenance', 'security'
    garden_id UUID REFERENCES garden(id), -- Scope de usuario (qué jardín ve)
    status VARCHAR(20) DEFAULT 'Activo', -- 'Activo', 'Inactivo', 'En verificación'
    last_login TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- Resident (extensión para residentes)
CREATE TABLE resident (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL UNIQUE REFERENCES user(id) ON DELETE CASCADE,
    apartment_id UUID NOT NULL REFERENCES apartment(id),
    role_in_apartment VARCHAR(30) DEFAULT 'Ocupante', -- 'Propietario', 'Ocupante'
    move_in_date DATE,
    move_out_date DATE,
    emergency_contact VARCHAR(100),
    emergency_phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Pagos

```sql
CREATE TABLE payment (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    apartment_id UUID NOT NULL REFERENCES apartment(id),
    amount DECIMAL(10, 2) NOT NULL,
    description VARCHAR(255),
    invoice_date DATE NOT NULL,
    due_date DATE NOT NULL,
    payment_date DATE,
    status VARCHAR(20) NOT NULL DEFAULT 'Pendiente', -- 'Pendiente', 'En riesgo', 'Vencido', 'Pagado', 'Anulado'
    payment_method VARCHAR(50), -- 'Efectivo', 'Transferencia', 'Tarjeta', etc
    reference_number VARCHAR(100),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Incidencias

```sql
CREATE TABLE incident (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    apartment_id UUID NOT NULL REFERENCES apartment(id),
    reported_by UUID NOT NULL REFERENCES user(id),
    assigned_to UUID REFERENCES user(id), -- Personal de mantenimiento
    category VARCHAR(50) NOT NULL, -- 'Plomería', 'Electricidad', 'Estructural', 'Limpieza', 'Otros'
    priority VARCHAR(20) NOT NULL DEFAULT 'Normal', -- 'Baja', 'Normal', 'Alta', 'Urgente'
    title VARCHAR(200) NOT NULL,
    description TEXT,
    status VARCHAR(30) NOT NULL DEFAULT 'Nueva', -- Estados del workflow
    resolution_notes TEXT,
    image_urls TEXT[], -- Array de URLs de imágenes
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP
);

-- Audit trail para incidencias
CREATE TABLE incident_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    incident_id UUID NOT NULL REFERENCES incident(id) ON DELETE CASCADE,
    status_from VARCHAR(30),
    status_to VARCHAR(30),
    changed_by UUID NOT NULL REFERENCES user(id),
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Visitantes

```sql
CREATE TABLE visitor (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    apartment_id UUID NOT NULL REFERENCES apartment(id),
    registered_by UUID NOT NULL REFERENCES user(id),
    name VARCHAR(100) NOT NULL,
    document VARCHAR(50),
    phone VARCHAR(20),
    reason VARCHAR(100),
    vehicle_plate VARCHAR(20),
    scheduled_entry TIMESTAMP NOT NULL,
    scheduled_exit TIMESTAMP,
    actual_entry TIMESTAMP,
    actual_exit TIMESTAMP,
    status VARCHAR(20) DEFAULT 'Esperando', -- 'Esperando', 'Autorizado', 'Rechazado', 'Completado', 'Cancelado'
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Reservas

```sql
CREATE TABLE common_area (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    garden_id UUID NOT NULL REFERENCES garden(id),
    name VARCHAR(100) NOT NULL,
    description TEXT,
    capacity INTEGER,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE reservation (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    common_area_id UUID NOT NULL REFERENCES common_area(id),
    reserved_by UUID NOT NULL REFERENCES user(id),
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    reason VARCHAR(200),
    expected_guests INTEGER,
    status VARCHAR(20) DEFAULT 'Confirmada', -- 'Confirmada', 'Completada', 'Cancelada'
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(common_area_id, start_time, end_time)
);
```

### Mantenimiento

```sql
CREATE TABLE maintenance_order (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    incident_id UUID REFERENCES incident(id), -- Puede venir de incidencia
    apartment_id UUID REFERENCES apartment(id),
    assigned_to UUID NOT NULL REFERENCES user(id),
    type VARCHAR(30) NOT NULL, -- 'Preventivo', 'Correctivo', 'Emergencia'
    description TEXT,
    status VARCHAR(30) NOT NULL DEFAULT 'Programado', -- 'Programado', 'En proceso', 'Completado', 'Cancelado'
    scheduled_date DATE,
    completion_date DATE,
    estimated_cost DECIMAL(10, 2),
    actual_cost DECIMAL(10, 2),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Comunicaciones y Chat

```sql
CREATE TABLE communication (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    garden_id UUID NOT NULL REFERENCES garden(id),
    sender_id UUID NOT NULL REFERENCES user(id),
    title VARCHAR(200) NOT NULL,
    body TEXT NOT NULL,
    target_type VARCHAR(30) NOT NULL, -- 'General', 'Por edificio', 'Por residente'
    target_id UUID, -- building_id o user_id según target_type
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE chat_message (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sender_id UUID NOT NULL REFERENCES user(id),
    receiver_id UUID REFERENCES user(id), -- NULL si es grupo
    group_name VARCHAR(100), -- NULL si es privado
    message TEXT NOT NULL,
    read_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Notificaciones

```sql
CREATE TABLE notification (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES user(id) ON DELETE CASCADE,
    type VARCHAR(50) NOT NULL, -- 'Incident_Assigned', 'Payment_Due', 'Message', etc
    title VARCHAR(200),
    message TEXT,
    related_id UUID, -- incident_id, payment_id, etc
    read_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Índices recomendados

```sql
CREATE INDEX idx_building_garden_id ON building(garden_id);
CREATE INDEX idx_apartment_building_id ON apartment(building_id);
CREATE INDEX idx_apartment_status ON apartment(status);
CREATE INDEX idx_resident_apartment_id ON resident(apartment_id);
CREATE INDEX idx_resident_user_id ON resident(user_id);
CREATE INDEX idx_user_email ON user(email);
CREATE INDEX idx_user_role ON user(role);
CREATE INDEX idx_payment_apartment_id ON payment(apartment_id);
CREATE INDEX idx_payment_status ON payment(status);
CREATE INDEX idx_payment_due_date ON payment(due_date);
CREATE INDEX idx_incident_apartment_id ON incident(apartment_id);
CREATE INDEX idx_incident_status ON incident(status);
CREATE INDEX idx_incident_assigned_to ON incident(assigned_to);
CREATE INDEX idx_visitor_apartment_id ON visitor(apartment_id);
CREATE INDEX idx_visitor_actual_entry ON visitor(actual_entry);
CREATE INDEX idx_reservation_common_area_id ON reservation(common_area_id);
CREATE INDEX idx_reservation_start_time ON reservation(start_time);
CREATE INDEX idx_maintenance_order_assigned_to ON maintenance_order(assigned_to);
CREATE INDEX idx_maintenance_order_status ON maintenance_order(status);
CREATE INDEX idx_notification_user_id ON notification(user_id);
CREATE INDEX idx_notification_read_at ON notification(read_at);
CREATE INDEX idx_chat_message_sender_id ON chat_message(sender_id);
CREATE INDEX idx_chat_message_created_at ON chat_message(created_at);
```

---

## I. DISEÑO UX/UI

### Paleta de colores

```css
:root {
    /* Primarios */
    --color-primary-green: #10b981;      /* Verde principal — botones, elementos activos */
    --color-primary-light: #d1fae5;      /* Verde muy claro — backgrounds */
    
    /* Grises */
    --color-white: #ffffff;
    --color-gray-50: #f9fafb;
    --color-gray-100: #f3f4f6;
    --color-gray-200: #e5e7eb;
    --color-gray-300: #d1d5db;
    --color-gray-400: #9ca3af;
    --color-gray-500: #6b7280;
    --color-gray-600: #4b5563;
    --color-gray-700: #374151;
    --color-gray-800: #1f2937;
    --color-gray-900: #111827;
    
    /* Estados */
    --color-success: #059669;
    --color-warning: #d97706;
    --color-error: #dc2626;
    --color-info: #0ea5e9;
    
    /* Bordes */
    --color-border: #e5e7eb;
    
    /* Sombras */
    --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}
```

### Tipografía

```css
:root {
    /* Tipografía */
    --font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    --font-size-xs: 12px;
    --font-size-sm: 14px;
    --font-size-base: 16px;
    --font-size-lg: 18px;
    --font-size-xl: 20px;
    --font-size-2xl: 24px;
    --font-size-3xl: 30px;
    
    --line-height-tight: 1.25;
    --line-height-normal: 1.5;
    --line-height-relaxed: 1.625;
    
    --font-weight-normal: 400;
    --font-weight-medium: 500;
    --font-weight-semibold: 600;
    --font-weight-bold: 700;
}
```

### Componentes principales

#### Header
```
┌─────────────────────────────────────────────────┐
│ Logo    Dashboard             🔔  👤  ▼         │
└─────────────────────────────────────────────────┘
```
- Logo a la izquierda
- Título de página al centro
- Notificaciones, usuario, menú desplegable a la derecha
- Fondo blanco con borde inferior sutil

#### Sidebar
```
┌──────────────────┐
│  🏠 Inicio       │
│  🏢 Departamentos│
│  👥 Residentes   │
│  💳 Pagos        │
│  🔧 Incidencias  │
│  👤 Visitantes   │
│  📅 Reservas     │
│  🔨 Mantenimiento│
│  📢 Comunicación │
│  💬 Chat         │
└──────────────────┘
```
- Ancho fijo: 250px (desktop) o colapsable en móvil
- Fondo gris muy claro (gray-50)
- Items con hover en gris más oscuro
- Item activo en verde
- Iconos SVG + texto

#### Cards
- Fondo blanco
- Borde sutil (gray-200)
- Sombra ligera
- Padding: 20px
- Border-radius: 8px
- Hover: sombra más pronunciada

#### Botones
```
[Primario verde]  [Secundario gris]  [Peligroso rojo]
```
- Primario: Verde, texto blanco
- Secundario: Gris, texto gris oscuro
- Peligroso: Rojo, texto blanco
- Padding: 10px 16px
- Border-radius: 6px
- Transición suave en hover
- Disabled: opacity 50%

#### Tablas
- Encabezado gris claro (gray-100)
- Filas con alternancia gris (row hover)
- Bordes sutiles
- Paginación abajo

#### Formularios
- Labels: gris oscuro, fuente pequeña
- Inputs: borde gris, padding interior
- Focus: borde verde, sombra verde muy suave
- Validación: rojo para errores
- Helper text: gris pequeño

#### Modals
- Fondo oscuro semi-transparente (overlay)
- Modal centrado, blanco
- Máx ancho: 600px
- Sombra pronunciada
- Botones al pie: Cancelar (gris) | Confirmar (verde)

#### Notificaciones
- Toast en la esquina inferior derecha
- Tipos: éxito (verde), error (rojo), info (azul), warning (amarillo)
- Auto-cierre en 5s
- Puede cerrarse manualmente

#### Badges/Estados
```
[✓ Pagado]  [⏰ Pendiente]  [⚠ Vencido]  [🔧 En Proceso]
```
- Verde para positivo
- Amarillo para pendiente
- Rojo para negativo/error
- Azul para información

### Responsividad

```
Desktop (>1200px):  Sidebar siempre visible + contenido ancho
Tablet (768-1200px): Sidebar colapsable + contenido adaptado
Móvil (<768px):     Sidebar como menú hamburguesa
                    Full width content
                    Fuentes adaptadas
```

---

## J. SEGURIDAD

### Estrategia de autenticación

1. **Login**
   - Email + contraseña
   - Backend valida credenciales contra hash BCrypt
   - Si es correcto: Django genera sesión (token)
   - Token almacenado en cookie segura (HTTP-only, Secure, SameSite)
   - Redirect a dashboard según rol

2. **Autorización por rol**
   - Cada endpoint verifica rol y permisos
   - Decoradores Django para proteger vistas
   - Permisos verificados siempre en backend, nunca en frontend
   - Ejemplo: `@require_permission('can_create_apartment')`

3. **Protección de rutas frontend**
   - Verificar token en localStorage/sessionStorage
   - Si no existe o es inválido: redirigir a login
   - No confiar únicamente en esto; backend es la fuente de verdad

### Medidas específicas

#### CSRF
- Django middleware CSRF habilitado
- Token CSRF en formularios y peticiones POST
- Validación en backend

#### Contraseñas
- Hashing con BCrypt (Django)
- Mínimo 8 caracteres
- Validación en backend
- Nunca en plaintext

#### Validación
- Frontend: validación de UX
- Backend: validación obligatoria de todos los inputs
- Escape de strings en templates
- Parametrized queries (Django ORM maneja esto)

#### Endpoints
- Todos requieren autenticación (token válido)
- Verificación de permisos
- Rate limiting (para login, cambio de contraseña)
- Log de accesos fallidos

#### Datos sensibles
- Variables en `.env` (contraseña BD, claves secretas, etc)
- Nunca en código fuente
- `.env` NO se commitea a git

#### Sesiones
- Timeout de sesión: 24 horas (configurable)
- Logout claro sesión
- Prevención de session fixation

---

## K. INTEGRACIÓN SUPABASE/PostgreSQL

### Setup inicial

1. Crear proyecto en Supabase (https://supabase.com)
2. Obtener:
   - Database URL (PostgreSQL)
   - Anonymous/Service key (si aplica)
   - Project URL
3. Guardar en `.env`:
   ```
   DATABASE_URL=postgresql://user:password@host:5432/db_name
   SUPABASE_URL=https://xxxxx.supabase.co
   SUPABASE_KEY=xxxxx
   ```

### Configuración Django

```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DATABASE_NAME'),
        'USER': env('DATABASE_USER'),
        'PASSWORD': env('DATABASE_PASSWORD'),
        'HOST': env('DATABASE_HOST'),
        'PORT': env('DATABASE_PORT', default=5432),
    }
}
```

### Migraciones
- Django Migrations manejan el schema
- `python manage.py makemigrations`
- `python manage.py migrate`
- Supabase proporciona una interfaz web para ver esquema

### Conexión desde Django a PostgreSQL
- Django ORM (models) → PostgreSQL automáticamente
- No necesita configuración adicional de Supabase si se usa solo PostgreSQL
- Si se usan APIs de Supabase (Auth, Storage): necesita configuración adicional

---

## L. ARQUITECTURA DJANGO CHANNELS / WEBSOCKETS

### Cuándo usar WebSockets

**Sí usar para:**
- Chat (mensajería en tiempo real)
- Notificaciones push en tiempo real
- Actualizaciones de estado críticas (ej: incidencia asignada)
- Indicadores de disponibilidad (usuario online)

**NO usar para:**
- CRUD normales (peticiones HTTP son suficientes)
- Datos que se cargan una sola vez
- Operaciones que no necesitan actualización inmediata

### Setup de Django Channels

```python
# settings.py
INSTALLED_APPS = [
    # ...
    'channels',
]

ASGI_APPLICATION = 'config.asgi.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],  # o variable env
        },
    },
}
```

### Estructura de WebSockets

```python
# chat/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Usuario conecta
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        
        # Unir grupo
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Usuario desconecta
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Recibe mensaje del cliente
        data = json.loads(text_data)
        message = data['message']
        
        # Guardar en BD
        # ...
        
        # Enviar a grupo
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat.message',
                'message': message,
                'sender': str(self.scope['user'])
            }
        )

    async def chat_message(self, event):
        # Envía a este usuario
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender']
        }))
```

```python
# chat/routing.py
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
]

# config/asgi.py
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from chat.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
```

### Cliente JavaScript (WebSocket)

```javascript
// Conectar
const socket = new WebSocket('ws://localhost:8000/ws/chat/room1/');

socket.onopen = function(e) {
    console.log('Conectado');
};

socket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    console.log('Mensaje recibido:', data.message);
};

socket.onerror = function(e) {
    console.error('Error:', e);
};

// Enviar
socket.send(JSON.stringify({
    'message': 'Hola mundo'
}));

socket.close();
```

### Autenticación en WebSockets

```python
# Middleware para verificar usuario
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections
import jwt

class JWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        headers = dict(scope['headers'])
        token = headers.get(b'authorization', b'').decode()
        
        # Validar token
        # ...
        
        await super().__call__(scope, receive, send)
```

---

## M. DECISIONES TÉCNICAS

### 1. **Por qué Django y no FastAPI/Flask**
- FastAPI: más moderno, pero menos batteries included
- Flask: muy flexible pero menos seguridad integrada
- **Django**: ORM robusto, autenticación/permisos integrados, Admin panel, documentación extensa
- **Decisión**: Django es mejor para un proyecto de administración con permisos complejos

### 2. **Por qué Supabase + PostgreSQL y no MongoDB**
- MongoDB: schema-less, pero requiere normalización manual
- PostgreSQL: ACID, relaciones fuertes, constraints
- **Decisión**: La estructura Garden → Building → Apartment necesita integridad relacional

### 3. **Por qué Django Channels y no Socket.io/Pusher**
- Socket.io: requiere Node.js
- Pusher: SaaS, costo adicional
- **Decisión**: Django Channels integrado con Django, sin costos, control total

### 4. **Vanila JavaScript y no React/Vue**
- React/Vue: overhead inicial, build process
- Vanilla: más control, sin dependencias, ideal para proyecto pequeño/mediano
- **Decisión**: Mantener stack sencillo, escalable después si crece

### 5. **API RESTful o GraphQL**
- GraphQL: flexible pero más complejo
- **Decisión**: REST es suficiente, más simple de documentar y debuggear

---

## N. RIESGOS Y AMBIGÜEDADES

### Riesgos identificados

1. **Escalabilidad de Chat**
   - Si muchos usuarios simultáneamente en chat: Redis puede ser cuello de botella
   - **Mitigación**: Monitoring de conexiones, posible switch a Kafka si crece

2. **Concurrencia en Pagos**
   - Múltiples pagos simultáneos en mismo apartamento
   - **Mitigación**: Database locks, transacciones ACID

3. **Validación de Workflows**
   - Estados de incidencia, pagos, etc. pueden tener flujos complejos
   - **Mitigación**: State machines, tests exhaustivos

4. **Notificaciones en tiempo real**
   - Si muchas notificaciones simultáneas: posible sobrecarga
   - **Mitigación**: Queue de tareas (Celery + Redis) para notificaciones no críticas

### Ambigüedades del documento

1. **Métodos de pago**: El PDF no especifica cómo se procesan pagos. 
   - **Propuesta**: Inicialmente, pago manual (admin registra). Después integrar Stripe/PayPal.

2. **Notificaciones por correo**: ¿Deben enviarse mails automáticos?
   - **Propuesta**: Sí, para pagos vencidos, incidencias asignadas. Usar Django-mail + Celery.

3. **Auditoría completa**: ¿Todos los cambios deben registrarse?
   - **Propuesta**: Sí, crear tabla `audit_log` que registre qué usuario cambió qué, cuándo.

4. **Documentos de residentes**: ¿Dónde se almacenan archivos (cédula, contrato)?
   - **Propuesta**: En Supabase Storage o AWS S3. Inicialmente: almacenamiento en servidor.

5. **Permisos granulares**: Algunos usuarios (Manager) solo ven edificios asignados.
   - **Propuesta**: Campo `assigned_buildings` en modelo Manager, filtrar queries por eso.

---

## O. PRÓXIMOS PASOS DESPUÉS DE APROBACIÓN

Una vez aprobada esta arquitectura:

### Fase 2: Configuración Base
1. Inicializar proyecto Django
2. Configurar Supabase/PostgreSQL
3. Setup de Django Channels
4. Estructura de carpetas

### Fase 3: Modelos
1. Crear todas las tablas
2. Migraciones
3. Validaciones a nivel DB

### Fase 4: Autenticación
1. Login/Logout
2. Roles y permisos
3. Protección de endpoints

### Fase 5: Módulos en orden lógico
1. Estructura (Garden → Building → Apartment)
2. Residentes
3. Pagos
4. Incidencias
5. ... (resto según prioridad)

### Fase 6: Frontend
1. Layout base
2. Componentes
3. Integración con APIs

### Fase 7: WebSockets y Tiempo Real
1. Chat
2. Notificaciones

### Fase 8: Testing y refinamiento

---

## P. CONCLUSIÓN

Esta arquitectura proporciona:

✅ **Claridad**: Estructura bien definida, roles obvios, flujos explícitos  
✅ **Escalabilidad**: Django + PostgreSQL soporta crecimiento  
✅ **Seguridad**: Autenticación robusta, autorización en backend  
✅ **Mantenibilidad**: Código organizado, apps separadas por responsabilidad  
✅ **Profesionalismo**: Stack moderno, patrones probados, documentación clara  

**Solicitamos tu aprobación para proceder con la implementación.**

---

**Documento preparado por:** GitHub Copilot  
**Fecha:** 2026-08-11  
**Estado:** Pendiente de aprobación
