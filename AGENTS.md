# AGENTS.md

Sistema de administración residencial **CONDYSOS** (Django 6.1 + DRF + Channels). No hay README; este es el único doc.

## Repo y git

- El **repo Git vive en `tecnico\condosys\`** (un nivel arriba de la carpeta del proyecto). El proyecto Django (con `manage.py`) está en `tecnico\condosys\condosys\`.
- Remoto `origin`: `https://github.com/JMJ0331/condosys.git`. Rama de trabajo: **`desarrollo`** (desarrollar ahí; `main` es estable).
- Mensajes de commit en español con prefijos cortos: `add:`, `fix:`, `update:`, `refactor:`. Los mensajes se escriben **en pretérito indefinido** (ej. "a nivel de código: añadí", "agregué", "integré", "renombré", "arreglé", no en infinitivo ni presente).
- `.gitignore` está dentro de `condosys\.gitignore` (protege `.env`, `db.sqlite3`, `.venv`, `__pycache__`).

## Comandos (Windows)

```
.venv\Scripts\python.exe manage.py runserver     # servidor ASGI vía daphne
.venv\Scripts\python.exe manage.py check          # verificación de settings (0 issues)
.venv\Scripts\python.exe manage.py test           # tests; aún no hay suite real
.venv\Scripts\python.exe manage.py makemigrations / migrate
.venv\Scripts\python.exe -m pip install --upgrade -r requirements.txt   # actualizar deps
```

- Venv local: `.venv` (Python 3.14.6). No hay linter, formatter, CI ni tests reales.
- `requirements.txt` no fija versiones a propósito: `pip install -r` siempre instala la última versión. Actualizado a 2026-09 con `pip install --upgrade --dry-run` (todo "already satisfied").

## Arquitectura

- Config: `condosys\` (settings, urls). Raíz `''` → login; `inicio`, `admin/` y una ruta por app (ver `condosys\urls.py`).
- **Cada app** (`accounts`, `residents`, `payments`, ...) sigue el mismo patrón: vista de función `@login_required` que renderiza un template + `ModelViewSet` DRF, `urls.py` con `DefaultRouter` registrado en `r''`, y sus propios `templates/` y `static/`.
- Templates globales: `templates\base.html` y `templates\componentes\`. Estaticos del proyecto en `static\`.
- DB: SQLite (`db.sqlite3` poblado) con `ATOMIC_REQUESTS=True`. PostgreSQL queda comentado en `settings.py` (~línea 121) para producción.
- Config por `.env` vía `python-dotenv`: `DJANGO_DEBUG`, `DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS`.

## Modelo de usuario y roles (crítico)

- `AUTH_USER_MODEL = 'accounts.User'`: **sin `username`**, login con email (`USERNAME_FIELD='email'`), PK UUID.
- Roles en `user.role`: `admin`, `manager`, `resident`, `maintenance`, `security`. Estados en `user.status`: `active`, `inactive`, `pending`. El login manual (`login\views.py`) rechaza a quien no tenga `status == 'active'`.
- Los permisos DRF por rol viven en `accounts\permissions.py` (`IsManager`, `IsResident`, ...). Úsalos en los ViewSets en lugar de repetir chequeos de rol.

## Permisos por rol de usuario

### **1. Administrador**
**Lo que podrá hacer:**

* Gestionar todo el sistema con acceso completo.
* Autorizar el registro de nuevos usuarios.
* Gestionar roles y permisos del sistema.
* Registrar, editar, consultar y asociar apartamentos a propietarios o residentes.
* Definir y cambiar el estado del apartamento (ocupado, vacío, alquilado, en mantenimiento).
* Registrar y gestionar datos de propietarios, inquilinos y residentes (activar/desactivar, consultar historial).
* Registrar cuotas de mantenimiento, pagos realizados, mora y otros cargos (parqueo, basura, seguridad, penalidades).
* Consultar y filtrar pagos pendientes o vencidos, y generar comprobantes de pago.
* Asignar estado, agregar comentarios, hacer seguimiento y ver el historial de incidencias.
* Gestionar visitantes, accesos y reservas de áreas comunes.
* Generar reportes administrativos.

**Lo que NO podrá hacer:**

* No tiene restricciones explícitas dentro del sistema (posee acceso completo a todos los módulos).

### **2. Personal Administrativo**
**Lo que podrá hacer:**

* Registrar cuotas de mantenimiento, pagos recibidos y otros cargos aplicables.
* Consultar y filtrar estados de pago (pendientes, vencidos) y emitir comprobantes.
* Registrar y actualizar la información de propietarios, inquilinos y residentes.
* Consultar e interactuar con el módulo de incidencias (seguimiento y comentarios).
* Realizar consultas generales en los módulos del sistema.

**Lo que NO podrá hacer:**

* No puede autorizar el registro de usuarios en el sistema ni gestionar roles/permisos globales.
* No tiene acceso a la administración total o configuración estructural del sistema (reservado para Administrador).

### **3. Seguridad / Portería**
**Lo que podrá hacer:**

* Registrar la entrada y salida de visitantes con fecha y hora.
* Registrar y controlar los accesos al residencial.

**Lo que NO podrá hacer:**

* No puede registrar ni gestionar pagos, cuotas ni cobros.
* No puede crear, modificar ni eliminar información de residentes o propietarios.
* No puede cambiar estados de incidencias, administrar reservas de áreas comunes ni ver reportes financieros/administrativos.
* No puede autorizar ni gestionar usuarios en la plataforma.

### **4. Residente / Propietario**
**Lo que podrá hacer:**

* Iniciar sesión, cerrar sesión y cambiar o recuperar su contraseña.
* Consultar sus pagos realizados, pagos pendientes y comprobantes de mantenimiento u otros cargos.
* Reportar incidencias o reclamos clasificándolas por tipo (electricidad, agua, seguridad, limpieza, ruido, infraestructura, otros).
* Consultar el historial y seguimiento de sus incidencias reportadas.
* Reservar áreas comunes.

**Lo que NO podrá hacer:**

* No puede registrar o modificar información de otros apartamentos ni de otros residentes.
* No puede autorizar o validar sus propios pagos directamente en el sistema.
* No puede cambiar el estado de las incidencias (solo puede crearlas y comentar/dar seguimiento).
* No puede registrar visitantes desde el módulo de seguridad ni controlar accesos.
* No tiene acceso a reportes globales ni a la administración del sistema.

## Gotchas verificados

- **WebSockets no arrancan**: existe `chat\routing.py` + `chat\consumers.py` y `ASGI_APPLICATION = 'condosys.asgi.application'`, pero `condosys\asgi.py` solo llama a `get_asgi_application()` sin `ProtocolTypeRouter`. Cualquier trabajo en chat/notificaciones requiere cablear el routing en `asgi.py` antes.
- **`login_view` está definida 2 veces** en `login\views.py` (líneas 4 y 24); la segunda sobreescribe a la primera y **no valida credenciales**. Elimina/une la duplicada al tocar login.
- `debug_toolbar` y `django-extensions` están en requirements pero **NO en `INSTALLED_APPS`**.
- Cuidado con `settings.py`: duplica el bloque `REST_FRAMEWORK` (líneas 60 y 201); el segundo bloque define la auth/paginación reales.
- Los `tests.py` de cada app son plantillas vacías; no asumas tests existentes.
- Español en templates/comentarios; `LANGUAGE_CODE='es-es'`, `TIME_ZONE='America/Bogota'`.

## Reglas de refactor frontend (obligatorias)

1. **Nada de `<script>` inline ni estilos `style=` en HTML.** El único `<script>` permitido es `<script src="...">` para conectar el HTML con su JS. Los manejadores (`onchange`, `onclick`, ...) van dentro del archivo JS externo.
2. **Estilos/JS compartidos entre apps viven en `static\css\` / `static\js\` del proyecto** (ej. `static\css\formularios.css`, `acciones.css`, `dialogos.css`, `paginacion.css`, `static\js\pagos.js`, `dialogos.js`). Lo específico de un módulo queda en su `static\` propio.
3. **El HTML principal de cada módulo se llama siempre `index.html`**; los demás archivos se nombran por su contenido.
4. **CSS en español, nombres claros y concisos**, tanto en archivos como en clases:
   - `payments.css` → `pagos.css`; `structure.css` → `departamentos.css`; `inicio\static\css\index.css` → `inicio.css`; `residents.css` y `login.css` ya están en español.
   - Mapeo de clases: `form-section`→`seccion-formulario`, `form-row`→`fila-formulario`, `form-field`→`campo-formulario`, `select-field`→`campo-seleccion`, `input-field`→`campo-entrada`, `form-switch-row`→`fila-interruptor`, `switch-label`→`etiqueta-interruptor`, `switch`→`interruptor`, `switch-slider`→`deslizador-interruptor`, `switch-input`→`entrada-interruptor`, `dialog-footer`→`pie-formulario`, `dialog-header`→`cabecera-dialogo`, `dialog-close`→`boton-cerrar`, `btn-generar-comprobante`→`btn-comprobante`, `Acciones-dashboard`→`panel-acciones`, `container-acciones`→`contenedor-acciones`, `pag-btn`→`boton-pagina`, `pag-num`→`numero-pagina`, `paginacion-numeros`→`numeros-paginacion`.
   - El JS externo no puede usar etiquetas de plantilla Django (`{% url %}`, `{{ var }}`); el HTML le pasa esos valores con atributos `data-*` (ej. `data-url-comprobante`, `data-pago-apartamento`, `data-departamento`).
   - Mantener la responsividad: los estilos compartidos incluyen media queries (breakpoints 560px/900px) usados por los formularios y las grid de acciones.
5. **Los estilos salen de `static\css\variables.css`** (el archivo de variables del proyecto, en la carpeta static principal):
   - Colores, sombras, bordes, radios, márgenes, paddings y espacios se toman de las variables de esa hoja (ej. `--green-500`, `--red-400`, `--borderR-8`, `--shadow-200`, `--padding-16`, `--space-8`), nunca como valores literales repetidos.
   - **La única unidad `px` permitida es para bordes y sombras** (incluido el radio de borde, que ya tiene sus variables en px: `--border-*`, `--borderR-*`, `--shadow-*`). Cualquier otra medida (margen, padding, espacio, tamaño, tipografía, ancho, alto) se escribe en `rem`; con `font-size: 62.5%` en `:root`, `1rem = 10px`.
   - Las variables token de `variables.css` se usan **tal cual** aunque algunas estén en px (`--margin-*`, `--shadow-*`, `--borderR-*`), porque ese archivo es la fuente canónica. Las media queries mantienen sus breakpoints en px (práctica estándar).
   - `variables.css` se importa desde `style.css` (base), `dashboard.css`, `inicio.css` y `login.css`; quien use variables debe asegurarse de que la hoja que escribe importe `variables.css` antes.