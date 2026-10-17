# Manual TÃ©cnico â€” CONDOSYS

| Documento | Manual TÃ©cnico |
|---|---|
| Sistema | CONDOSYS â€” administraciÃ³n residencial |
| Stack | Django 6.1 + Django REST Framework + Channels |
| VersiÃ³n | 1.0 |
| Fecha | Octubre 2026 |
| Repositorio | https://github.com/JMJ0331/condosys |
| Rama de trabajo | desarrollo |
| Licencia | Proyecto acadÃ©mico / uso interno |

Documento generado a partir del cÃ³digo fuente del proyecto. Resumen de arquitectura, modelos de datos, API REST, permisos, frontend y procedimientos de operaciÃ³n.

## Ãndice

<!--INDICE-->

## 1. IntroducciÃ³n

### 1.1 PropÃ³sito del documento

Este manual describe el sistema CONDOSYS desde el punto de vista tÃ©cnico: quÃ© hace, cÃ³mo estÃ¡ construido, quÃ© decisiones tÃ©cnicas lo sostienen y cÃ³mo instalarlo, operarlo y extenderlo. Todo el contenido se derivÃ³ directamente del cÃ³digo fuente del repositorio, de modo que el documento y el sistema evolucionan juntos.

El manual estÃ¡ dirigido a las personas que desarrollarÃ¡n, darÃ¡n soporte o administrarÃ¡n el sistema: perfil de desarrollo backend, perfil de desarrollo frontend y perfil de operador.

### 1.2 QuÃ© es CONDOSYS

CONDOSYS es un sistema web de administraciÃ³n y gestiÃ³n para residenciales verticales u horizontales. Centraliza la informaciÃ³n de apartamentos, residentes, propietarios, cuotas, pagos, incidencias y control de accesos, reemplazando los cuadernos manuales y las hojas de cÃ¡lculo dispersas que normalmente se usan en la operaciÃ³n de una administraciÃ³n.

El sistema responde a un problema concreto: la administraciÃ³n de un residencial maneja datos sensibles (personas, documentos, pagos/saldo) y tareas recurrentes con plazos (cuotas, mantenimiento, permisos). Sin un sistema Ãºnico, cada tarea se resuelve por canales distintos y se pierde trazabilidad.

### 1.3 Alcance funcional

El alcance funcional se organiza en los siguientes mÃ³dulos, cada uno desplegado como una aplicaciÃ³n Django independiente pero integrada en un Ãºnico proyecto:

| MÃ³dulo | FunciÃ³n principal | Usuarios principales |
|---|---|---|
| Inicio (dashboard) | Resumen de estado: departamentos, incidencias abiertas, pagos por vencer, actividad reciente | Todos |
| Residencial | Ficha Ãºnica del residencial: nombre, RNC, direcciÃ³n, provincia/municipio y distribuciÃ³n | Administrador |
| Departamentos | JerarquÃ­a JardÃ­n â†’ Edificio â†’ Apartamento, con estado y propietario | Todos (lectura), GestiÃ³n (escritura) |
| Propietarios | Registro de propietarios y asociaciÃ³n con apartamentos | GestiÃ³n |
| Residentes | Ocupantes por apartamento: relaciÃ³n, fecha de ingreso, mascotas | GestiÃ³n, Propietario (lectura) |
| Pagos | Registro de cuotas y pagos, estados de mora, descarga de comprobante en PDF | Todos (lectura), GestiÃ³n (escritura) |
| Mantenimientos | CatÃ¡logo de cargos y cuotas recurrentes por periodicidad | Todos (lectura), GestiÃ³n (escritura) |
| Incidencias | Reporte, clasificaciÃ³n, asignaciÃ³n, seguimiento e historial de cambios de estado | Todos (reportar), GestiÃ³n (gestionar) |
| Solicitudes | Certificados, permisos, instalaciones y trÃ¡mites documentales | GestiÃ³n |
| Visitantes | Registro, autorizaciÃ³n y control de entrada/salida | Seguridad, GestiÃ³n |
| Ãreas comunes | CatÃ¡logo de Ã¡reas comunes con tipo, capacidad, horario y estado | Todos (lectura), GestiÃ³n (escritura) |
| Reservas | Solicitud y aprobaciÃ³n de reservas de Ã¡reas comunes | Todos |
| Comunicados | Avisos, eventos y mantenimiento de comunicados del residencial | Todos (lectura), GestiÃ³n (escritura) |
| Notificaciones | Avisos dirigidos a usuarios concretos | GestiÃ³n |
| Reportes | Reportes administrativos, ocupaciÃ³n, pagos y bitÃ¡cora de auditorÃ­a (CSV) | GestiÃ³n |
| Chat | MensajerÃ­a persistida entre usuarios y grupos | Todos |
| Cuentas | Alta, ediciÃ³n, activaciÃ³n y roles de usuarios; perfil propio | Administrador |

*Tabla 1.1 - MÃ³dulos funcionales de CONDOSYS y su acceso por rol.*

### 1.4 Perfiles de usuario

El sistema define cinco roles, almacenados en el campo role del modelo de usuario. Cada rol habilita un conjunto de mÃ³dulos y un conjunto de acciones (crear, editar, eliminar):

- Administrador (admin): acceso total. Es el Ãºnico rol que autoriza el registro de nuevos usuarios y gestiona roles.
- Encargado de AdministraciÃ³n (manager): opera la operaciÃ³n diaria (pagos, solicitudes, residentes, reportes) pero no administra usuarios ni estructura del sistema.
- Residente (resident): consulta sus datos, reporta incidencias y reserva Ã¡reas comunes.
- Propietario (propietario): consulta informaciÃ³n de los apartamentos que posee.
- Seguridad / PorterÃ­a (security): opera el control de visitantes y accesos; sin acceso financiero ni a datos de residentes.

> **NOTA** â€” El detalle normativo de permisos por rol estÃ¡ en el capÃ­tulo 5. La matriz completa (quÃ© puede y quÃ© no puede hacer cada rol) se documenta en AGENTS.md y se resume aquÃ­ en el capÃ­tulo 5.

### 1.5 Convenciones del documento

- Los nombres de archivo, clases y funciones aparecen en tipo monoespaciado.
- Los bloques de cÃ³digo son extractos literales del repositorio.
- Las cajas ATENCIÃ“N seÃ±alan riesgo de operaciÃ³n; las cajas PENDIENTE / BUG seÃ±alan defectos conocidos del cÃ³digo actual.
- Las rutas se expresan siempre relativas a la raÃ­z del proyecto Django.

## 2. Stack tecnolÃ³gico y dependencias

### 2.1 Lenguaje y runtime

| Elemento | Valor | Comentario |
|---|---|---|
| Lenguaje | Python 3.13+ | Entorno de desarrollo verificado con 3.13.6 |
| Entorno virtual | venv/ (Windows: venv\Scripts\python.exe) | Nunca se instalan paquetes en el Python del sistema |
| GestiÃ³n de dependencias | pip + requirements.txt | El archivo no fija versiones a propÃ³sito |

> **ATENCIÃ“N** â€” requirements.txt no fija versiones. El archivo de dependencias usa comparadores >= sin versiones exactas. pip install -r requirements.txt instala siempre la Ãºltima versiÃ³n compatible. Consecuencia: una instalaciÃ³n nueva puede diferir de la que se probÃ³. Para reproducibilidad conviene congelar versiones con pip freeze en el momento de una publicaciÃ³n. ActualizaciÃ³n controlada: pip install --upgrade --dry-run -r requirements.txt para ver quÃ© cambios sin aplicar nada.

### 2.2 Dependencias del proyecto

| Grupo | Paquete | VersiÃ³n min. | Uso en CONDOSYS |
|---|---|---|---|
| Core | django | 6.1.1 | Framework base: ORM, vistas, plantillas, admin, auth |
| API | djangorestframework | 3.18.1 | ViewSets, serializers, permisos y paginaciÃ³n de la API |
| API | django-filter | 26.1 | DjangoFilterBackend para filtrar y ordenar listados |
| Seguridad web | django-cors-headers | 4.9.0 | Middleware CORS para consumos desde otros orÃ­genes |
| Datos | psycopg | 3.3.6 | Driver PostgreSQL para el despliegue de producciÃ³n |
| Real-time | channels | 4.3.2 | Infraestructura ASGI para WebSockets |
| Real-time | channels-redis | 4.3.0 | Channel layer distribuido sobre Redis |
| Real-time | daphne | 4.2.3 | Servidor ASGI; es el que ejecuta runserver |
| UtilerÃ­as | python-dotenv | 1.2.3 | Carga del archivo .env en settings |
| UtilerÃ­as | celery | 5.6.3 | Cola de tareas asÃ­ncronas (configurado, sin uso activo) |
| UtilerÃ­as | redis | 8.1.0 | Cliente Redis |
| UtilerÃ­as | Pillow | 12.3.0 | Procesamiento de imÃ¡genes (avatars, fotos) |
| Documentos | reportlab | 5.0.1 | GeneraciÃ³n del comprobante de pago en PDF |
| ProducciÃ³n | gunicorn | 26.2.0 | Servidor WSGI para producciÃ³n |
| ProducciÃ³n | whitenoise | 6.12.0 | Servido de archivos estÃ¡ticos sin servidor extra |
| Desarrollo | django-extensions | 4.1 | Comandos de gestiÃ³n adicionales |
| Desarrollo | django-debug-toolbar | 8.0.0 | Panel de depuraciÃ³n (no activado) |

*Tabla 2.1 - Dependencias declaradas en requirements.txt.*

### 2.3 Componentes principales

| Componente | TecnologÃ­a | Responsabilidad en el sistema |
|---|---|---|
| Backend web | Django 6.1 | MVT: URLs, vistas, plantillas, ORM y administraciÃ³n |
| API REST | Django REST Framework | ViewSets por mÃ³dulo con permisos, filtros y paginaciÃ³n |
| Base de datos | SQLite (dev) / PostgreSQL (prod) | Persistencia relacional de 25 modelos |
| Plantillas | Django Template Language | HTML renderizado en el servidor |
| Estilos | CSS con variables + media queries | Sistema de diseÃ±o compartido entre mÃ³dulos |
| Interactividad | JavaScript nativo (sin framework) | Formularios, diÃ¡logos, filtros y acciones asÃ­ncronas |
| PDF | ReportLab | Comprobante de pago descargable |
| Tiempo real | Daphne + Channels + Redis | WebSockets de chat y notificaciones (pendiente de cablear) |
| Tareas asÃ­ncronas | Celery + Redis | Configurado en settings, sin app Celery implementada |
| Despliegue | Gunicorn + WhiteNoise | Servidor de producciÃ³n previsto |

*Tabla 2.2 - Componentes tecnolÃ³gicos y su papel en la arquitectura.*

### 2.4 Dependencias declaradas pero no activas

Los siguientes paquetes aparecen en requirements.txt y/o en settings.py pero no estÃ¡n integrados en INSTALLED_APPS ni en el flujo de ejecuciÃ³n. No son errores, pero conviene saberlo antes de planificar trabajo sobre ellos:

| Paquete / config | Estado real | QuÃ© faltarÃ­a |
|---|---|---|
| channels | No estÃ¡ en INSTALLED_APPS | Registrar la app y cablear el ProtocolTypeRouter en condosys/asgi.py |
| chat/routing.py + consumers.py | Existe pero es cÃ³digo muerto | Registrar las rutas WebSocket en asgi.py con AuthMiddlewareStack |
| CHANNEL_LAYERS | Configurado con RedisChannelLayer | Solo se usa si se cablea el routing ASGI |
| celery | Configurado (broker, serializers, timezone) | Crear celery.py, el initializer de la app y registrar tareas |
| django-extensions | No estÃ¡ en INSTALLED_APPS | AÃ±adir la app para habilitar sus comandos |
| django-debug-toolbar | No estÃ¡ en INSTALLED_APPS | AÃ±adir app + middleware solo en desarrollo |
| corsheaders | Middleware activo pero la app no estÃ¡ instalada | AÃ±adir 'corsheaders' a INSTALLED_APPS si se consume desde otro origen |
| gunicorn + whitenoise | Solo dependencias | Crear el servicio de producciÃ³n y servir los estÃ¡ticos con WhiteNoise |
| psycopg | Driver instalado | Descomentar el bloque PostgreSQL de settings.py |

*Tabla 2.3 - Capacidades preparadas pero no habilitadas.*

> **ATENCIÃ“N** â€” El frontend no usa ningÃºn framework de JavaScript. Todo el comportamiento dinÃ¡mico estÃ¡ escrito en JavaScript nativo repartido en 29 archivos .js. No hay build step, ni bundler, ni node_modules, ni transpilador. Ventaja: no hay cadena de herramientas que mantener. Riesgo: el JavaScript del proyecto crece de forma lineal con los mÃ³dulos y no tiene pruebas ni linting automÃ¡tico.

## 3. Arquitectura del proyecto

### 3.1 VisiÃ³n general

CONDOSYS sigue el patrÃ³n clÃ¡sico de Django: un Ãºnico proyecto de settings y URLs que agrega mÃºltiples aplicaciones. Cada aplicaciÃ³n es autÃ³noma en cuanto a modelos, vistas, serializers, plantillas y estÃ¡ticos, pero comparte el proyecto, la base de datos, el sistema de autenticaciÃ³n y los permisos definidos en la aplicaciÃ³n accounts.

**Flujo de una peticiÃ³n en CONDOSYS**

```
Navegador
    |
[Daphne (ASGI)]
    |
+-------------------+--------------------+
|                   |                    |
[Vistas HTML]   [API REST (DRF)]        |
|                   |                    |
+--------------+-------------------------+
                |
            [Capa comÃºn]
         accounts.permissions
           (IsAdmin, IsManager,
            IsResident, ...)
         accounts.decorators
           (@role_required)
                |
             [ORM Django]
                |
        [SQLite (dev) / PostgreSQL (prod)]
```

Contexto transversal: Jinja-free Django Templates, static/css (variables.css como fuente Ãºnica de tokens), static/js (mÃ³dulos sin framework).

### 3.2 Estructura de directorios

El repositorio tiene dos niveles: el proyecto Django y, dentro de Ã©l, las aplicaciones. La raÃ­z del proyecto es el directorio que contiene manage.py.

**Estructura del repositorio**

```text
condosys/
|-- manage.py           # utilidad de lÃ­nea de comandos de Django
|-- requirements.txt    # dependencias del proyecto
|-- .gitignore          # protege .env, db.sqlite3, .venv, __pycache__
|-- venv/               # entorno virtual (no versionado)
|-- db.sqlite3          # base de datos de desarrollo (no versionada)
|
|-- condosys/           # CONFIGURACIÃ“N del proyecto
|   |-- settings.py     # settings Ãºnicos (contiene duplicados, ver cap. 11)
|   |-- urls.py         # ROOT_URLCONF: incluye los urls de cada app
|   |-- asgi.py         # punto de entrada ASGI (sin ProtocolTypeRouter)
|   |-- wsgi.py         # punto de entrada WSGI
|   `-- accounts/       # sub-paquete auxiliar interno
|
|-- templates/          # plantillas GLOBALES
|   |-- base.html       # esqueleto comÃºn a toda la interfaz
|   `-- componentes/    # header, aside, modal, paginaciÃ³n, botones, ...
|
|-- static/             # estÃ¡ticos COMPARTIDOS del proyecto
|   |-- css/
|   |   |-- variables.css     # FUENTE ÃšNICA de tokens de diseÃ±o
|   |   |-- style.css         # estilos base (importa variables.css)
|   |   |-- formularios.css   # formularios compartidos
|   |   |-- tablas.css        # tablas de datos
|   |   |-- paginacion.css    # controles de paginaciÃ³n
|   |   |-- dialogos.css      # modales y diÃ¡logos
|   |   |-- acciones.css      # paneles de acciones del dashboard
|   |   |-- entradas.css      # inputs
|   |   `-- mediaquerys.css   # breakpoints comunes
|   |-- js/
|   |   |-- dialogos.js       # gestiÃ³n de <dialog>
|   |   |-- pagos.js          # lÃ³gica compartida de pagos
|   |   `-- mascaras.js, contadores.js, menu-movil.js, ...
|   `-- images/icons/         # iconografÃ­a
|
`-- <app>/              # 18 aplicaciones Django
    |-- models.py       # modelos de datos
    |-- views.py        # vistas HTML + ViewSets DRF
    |-- serializers.py  # serializers de la API
    |-- forms.py        # formularios de las vistas HTML
    |-- urls.py         # rutas + DefaultRouter
    |-- admin.py        # registro en el admin de Django
    |-- tests.py        # plantilla vacÃ­a (no hay suite real)
    |-- migrations/     # migraciones de esquema
    |-- templates/<app>/# plantillas de la app
    `-- static/css, static/js # estilos y scripts especÃ­ficos del mÃ³dulo
```

### 3.3 El patrÃ³n por aplicaciÃ³n

Todas las apps de dominio siguen el mismo esqueleto. Cuando agregue un mÃ³dulo nuevo, copie este patrÃ³n:

| Archivo | Contenido esperado | Existe en |
|---|---|---|
| models.py | Modelos de dominio con claves UUID y related_name explÃ­citos | Todas salvo login e inicio |
| views.py | app_index() con @role_required + ViewSets DRF | Todas |
| serializers.py | Serializers de lectura (y de detalle cuando aplica) | Todas salvo inicio |
| urls.py | Rutas HTML + DefaultRouter registrado en su prefijo | Todas |
| forms.py | Formularios ModelForm para las vistas HTML | MayorÃ­a |
| admin.py | Registro de modelos en el admin de Django | Todas |
| permissions.py | Permisos DRF especÃ­ficos | Solo accounts (ver cap. 5) |
| migrations/ | Migraciones de esquema | Todas salvo inicio y login |
| templates/ | index.html como pÃ¡gina principal del mÃ³dulo | Todas |
| static/ | CSS y JS propios del mÃ³dulo | Todas salvo inicio (parcial) |
| tests.py | Plantilla vacÃ­a generada por startapp | Todas |

*Tabla 3.1 - Archivos esperados en cada aplicaciÃ³n de dominio.*

> **NOTA** â€” ConvenciÃ³n de nombres del frontend. La pÃ¡gina principal de cada mÃ³dulo se llama siempre index.html; los demÃ¡s archivos se nombran por su contenido (agregar.html, nuevo.html, perfil.html). Los estilos y scripts compartidos viven en static/css y static/js del proyecto; lo especÃ­fico de un mÃ³dulo queda en el static de su propia app.

### 3.4 Capa de presentaciÃ³n: dos superficies en la misma app

Cada mÃ³dulo expone dos superficies complementarias:

- **Superficie HTML** - vista de funciÃ³n app_index que renderiza la plantilla index.html con paginaciÃ³n server-side, filtros por query string y formularios. Es la experiencia principal del usuario.
- **Superficie API** - ViewSet de DRF registrado en el router que expone listado, detalle, creaciÃ³n, actualizaciÃ³n y borrado en JSON, con filtros, bÃºsqueda, ordenamiento y paginaciÃ³n por ?page=. La vista HTML aplica el permiso con el decorador @role_required(...); la API lo aplica con permission_classes. Los listados HTML tienen paginaciÃ³n de 15 elementos por pÃ¡gina; la API usa PageNumberPagination con 20.

### 3.5 Patrones de implementaciÃ³n recurrentes

#### Visibilidad por usuario en los listados

Los listados HTML aplican un filtro de visibilidad para que un residente solo vea lo que le corresponde. El patrÃ³n es una funciÃ³n helper _<entidad>_visibles(user) en views.py, reutilizada por la vista y por el get_queryset() del ViewSet:

```python
# Patron real (payments/views.py, estructura logica)
def _pagos_visibles(user):
    qs = Payment.objects.all()
    if user.role in ('admin', 'manager'):
        return qs
    # El residente ve los pagos de sus apartamentos y sus propios registros
    return qs.filter(Q(resident__user=user) | Q(apartment__residents__user=user)) \
        .distinct()

# El ViewSet lo reutiliza para no duplicar la regla
def get_queryset(self):
    qs = _pagos_visibles(self.request.user)
    ... # filtros opcionales por query string
    return qs.distinct()
```

#### Serializers diferenciados para listado y detalle

Cuando el detalle expone mÃ¡s campos que el listado, el ViewSet elige el serializer segÃºn la acciÃ³n mediante get_serializer_class():

```python
def get_serializer_class(self):
    if self.action == 'retrieve':
        return ApartmentDetailSerializer # incluye datos anidados del edificio
    return ApartmentListSerializer # vista compacta para listados

# Uso en accounts: el serializer de creacion y el de actualizacion
# exigen campos distintos, asi que tambien se selecciona por accion.
def get_serializer_class(self):
    if self.action == 'create':
        return UserCreateSerializer # incluye password (write_only)
    if self.action in ('update', 'partial_update'):
        return UserUpdateSerializer # no expone role ni status
    return UserSerializer
```

#### Cambios de estado auditados

El mÃ³dulo de incidencias registra cada transiciÃ³n de estado en una bitÃ¡cora de historial. Se hace sobrescribiendo perform_update() en el ViewSet:

```python
# incidents/views.py - perform_update
def perform_update(self, serializer):
    estado_previo = serializer.instance.status
    instancia = serializer.save()

    # Si cambian el estado o la asignacion, deja rastro en el historial
    if (estado_previo != instancia.status) or \
       (instancia.assigned_to_id != self._asignacion_previa()):
        IncidentHistory.objects.create(
            incident=instancia,
            status_from=estado_previo,
            status_to=instancia.status,
            comment=self.request.data.get('history_comment', ''),
            changed_by=self.request.user,
        )
```

#### Comprobante en PDF

El comprobante de pago se genera en el servidor con ReportLab y se devuelve como respuesta HTTP en lugar de renderizar una plantilla:

```python
# payments/views.py - generar_comprobante
buffer = BytesIO()
doc = SimpleDocTemplate(buffer, pagesize=letter, ...)
doc.build([...]) # elementos del PDF
buffer.seek(0)

respuesta = HttpResponse(buffer.getvalue(), content_type='application/pdf')
respuesta['Content-Disposition'] = 'inline; filename="comprobante_pago.pdf"'
return respuesta
```

Los parÃ¡metros viajan por query string (?pago_id=...&departamento=...) porque el JS externo no puede usar etiquetas de plantilla Django; los valores viajan en atributos data-* del HTML.

## 4. InstalaciÃ³n, ejecuciÃ³n y operaciÃ³n

### 4.1 Requisitos previos

| Requisito | Detalle | CÃ³mo verificarlo |
|---|---|---|
| Python | 3.13 o superior (probado en 3.13.6) | python --version |
| pip | incluido con Python | python -m pip --version |
| Acceso al repositorio | git clone del remoto origin | git remote -v |
| Redis (opcional) | Solo si se activan Channels o Celery | redis-cli ping |
| PostgreSQL (opcional) | Solo para el despliegue de producciÃ³n | psql --version |

### 4.2 InstalaciÃ³n desde cero

Todos los comandos se ejecutan desde la raÃ­z del proyecto, el directorio que contiene manage.py. En Windows, los comandos usan la ruta relativa del intÃ©rprete del entorno virtual.

#### Paso 1 - Clonar el repositorio

```bash
git clone https://github.com/JMJ0331/condosys.git
cd condosys
git checkout desarrollo # rama de trabajo; main es la estable
```

#### Paso 2 - Crear el entorno virtual

```bash
# Windows (PowerShell / CMD)
python -m venv venv
venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate

# VerificaciÃ³n
python --version # debe responder 3.13.x
```

A partir de aquÃ­, este manual usa la forma Windows venv\Scripts\python.exe porque es el entorno verificado. En Linux/macOS se sustituye por python.

#### Paso 3 - Instalar dependencias

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# VerificaciÃ³n: la suite de comprobaciÃ³n debe reportar 0 problemas
python manage.py check
```

#### Paso 4 - Configurar el archivo .env

El proyecto lee su configuraciÃ³n sensible desde un archivo .env en la raÃ­z, cargado por python-dotenv. El archivo estÃ¡ en .gitignore y nunca debe versionarse.

**.env - variables disponibles**

```env
# .env (copiar de .env.example si existe; si no, crearlo a mano)
DJANGO_DEBUG=True
DJANGO_SECRET_KEY=<clave-larga-aleatoria>
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# Opcionales: solo si el despliegue los requiere
CORS_ALLOWED_ORIGINS=https://app.ejemplo.do
CSRF_TRUSTED_ORIGINS=https://app.ejemplo.do
REDIS_HOST=localhost
REDIS_PORT=6379
DATABASE_ENGINE=django.db.backends.postgresql
DATABASE_NAME=condosys_db
DATABASE_USER=postgres
DATABASE_PASSWORD=<clave>
DATABASE_HOST=localhost
DATABASE_PORT=5432
```

> **PENDIENTE / BUG** â€” SECRET_KEY no tiene valor por defecto. settings.py lee SECRET_KEY = os.getenv('DJANGO_SECRET_KEY') sin fallback. Si la variable falta, Django lanza ImproperlyConfigured y el proyecto no arranca. Implica que .env es obligatorio: no se puede levantar el proyecto sin Ã©l.

#### Paso 5 - Aplicar migraciones

```bash
python manage.py makemigrations # solo si modificaste modelos
python manage.py migrate
```

#### Paso 6 - Cargar datos de ejemplo (opcional)

El proyecto incluye un comando de gestiÃ³n idempotente que siembra registros de prueba en todas las secciones. Es la vÃ­a recomendada para levantar un entorno de demostraciÃ³n o para verificar permisos con los distintos roles.

**Carga de datos de demostraciÃ³n**

```bash
python manage.py poblar_datos

# Crea 7 usuarios base; las contraseÃ±as de los reciÃ©n creados son: Condosys123*
# admin@condosys.do rol admin
# gestion@condosys.do rol manager
# residente1..5@condosys.do rol resident
# Ejecutarlo de nuevo no duplica registros (update_or_create + transaction.atomic).
```

> **ATENCIÃ“N** â€” No use datos de ejemplo en producciÃ³n. El comando poblar_datos crea usuarios con contraseÃ±a conocida y datos personales ficticios. ElimÃ­nelos antes de exponer el sistema a usuarios reales.

#### Paso 7 - Arrancar el servidor de desarrollo

```bash
python manage.py runserver
# http://127.0.0.1:8000/
```

Aunque el comando se llama runserver, el servidor real es Daphne: la cadena daphne aparece primera en INSTALLED_APPS y Django delega en ella cuando estÃ¡ disponible.

### 4.3 Comandos de uso frecuente

| Comando | Para quÃ© sirve |
|---|---|
| manage.py runserver | Levanta el servidor ASGI de desarrollo |
| manage.py check | Verifica la configuraciÃ³n; debe dar 0 problemas |
| manage.py migrate | Aplica las migraciones pendientes |
| manage.py makemigrations | Genera migraciones tras cambiar modelos |
| manage.py sqlmigrate <app> <n> | Muestra el SQL de una migraciÃ³n |
| manage.py showmigrations | Lista el estado de las migraciones de cada app |
| manage.py createsuperuser | Crea el administrador inicial (pide email, no username) |
| manage.py shell | Consola interactiva de Python con el ORM cargado |
| manage.py dbshell | Consola directa de la base de datos |
| manage.py collectstatic | ReÃºne los estÃ¡ticos en STATIC_ROOT para producciÃ³n |
| manage.py test | Ejecuta la suite de pruebas (hoy vacÃ­a) |
| manage.py poblar_datos | Carga datos de demostraciÃ³n (idempotente) |

*Tabla 4.1 - Comandos de gestiÃ³n de Django usados en el proyecto.*

### 4.4 Flujo de trabajo con git

| Concepto | ConvenciÃ³n del proyecto |
|---|---|
| Rama de trabajo | desarrollo - aquÃ­ se desarrolla |
| Rama estable | main - versiones estables |
| Remoto | origin -> https://github.com/JMJ0331/condosys.git |
| Prefijos de commit | add:, fix:, update:, refactor: |
| Tiempo verbal | PretÃ©rito indefinido: 'agreguÃ©', 'integrÃ©', 'arreglÃ©' |
| Idioma | EspaÃ±ol, incluidos los mensajes de commit |

**Ejemplo**

```bash
fix: corregÃ­ la validaciÃ³n del rol en el login
git status # revisar antes de commitear
git add <archivos-especÃ­ficos> # nunca commitear .env ni db.sqlite3
git commit -m "add: agreguÃ© mÃ³dulo de reservas"
git push origin desarrollo
```

### 4.5 Rutas principales del sistema

| Ruta | MÃ³dulo | Acceso |
|---|---|---|
| / | Inicio de sesiÃ³n | PÃºblico |
| /salir/ | Cierre de sesiÃ³n (POST) | Autenticado |
| /inicio/ | Dashboard | Todos |
| /mi-perfil/ | Perfil del usuario | Todos |
| /residencial/ | Ficha del residencial | Administrador |
| /cuentas/ | Usuarios y roles | Administrador |
| /departamentos/ | Jardines, edificios y apartamentos | Todos |
| /propietarios/ | Propietarios | GestiÃ³n |
| /residentes/ | Residentes y ocupantes | GestiÃ³n, Propietario |
| /pagos/ | Pagos y cuotas | Todos (GestiÃ³n escribe) |
| /pagos/comprobante/ | Comprobante en PDF | Todos |
| /mantenimientos/ | Cargos de mantenimiento | Todos (GestiÃ³n escribe) |
| /incidencias/ | Incidencias | Todos |
| /solicitudes/ | Solicitudes y trÃ¡mites | GestiÃ³n |
| /visitantes/ | Control de visitantes | Seguridad, GestiÃ³n |
| /areas-comunes/ | Ãreas comunes | Todos |
| /reservas/ | Reservas | Todos |
| /comunicados/ | Comunicados | Todos |
| /notificaciones/ | Notificaciones | GestiÃ³n |
| /reportes/ | Reportes y bitÃ¡cora | GestiÃ³n |
| /chat/ | MensajerÃ­a | Todos |
| /configuracion/ | ConfiguraciÃ³n (usuarios e integraciÃ³n IA) | Administrador |
| /recuperar-clave/ | Solicitar recuperaciÃ³n de contraseÃ±a | PÃºblico |
| /restablecer-clave/ | Restablecer contraseÃ±a con token | PÃºblico |
| /visitantes/buscar-cedula/ | Lectura de cÃ©dula con IA (POST) | Seguridad, GestiÃ³n |
| /admin/ | AdministraciÃ³n de Django | Staff |

*Tabla 4.2 - Rutas HTML por mÃ³dulo.*

#### Manual tÃ©cnico CONDOSYS â€” Fragmento (capÃ­tulos 5 y 6)

## 5. Usuarios, roles y permisos

### 5.1 Modelo de usuario

El sistema no usa el modelo de usuario por defecto de Django. `accounts.User` extiende `AbstractUser` con dos cambios de fondo:

| Cambio | Detalle | Consecuencia |
| --- | --- | --- |
| Clave primaria UUID | `id = UUIDField(default=uuid.uuid4)` | Los identificadores no son enumerables; se pueden exponer en la API |
| Sin username | `username = None`; `USERNAME_FIELD = 'email'` | El login, el admin y createsuperuser piden email |
| Campo role | `admin \| manager \| resident \| propietario \| security` | El permiso se decide por rol, no por grupos |
| Campo status | `active \| inactive \| pending` | El login manual rechaza a quien no tenga `'active'` |
| TelÃ©fono y documento | `phone`, `document` (Ãºnicos) | IdentificaciÃ³n operativa del residente |
| Avatar | `avatar` (ImageField) y `avatar_url` (URLField) | Permite imagen local o remota |
| VÃ­nculo a jardÃ­n | `garden = FK a structure.Garden (SET_NULL)` | Encuadre del usuario dentro del residencial |

*Tabla 5.1 - Diferencias del modelo de usuario frente al de Django.*

### 5.2 Estados de la cuenta

| Estado | Significado | Puede iniciar sesiÃ³n |
| --- | --- | --- |
| `active` | Cuenta habilitada | SÃ­ |
| `pending` | En verificaciÃ³n, pendiente de autorizaciÃ³n | No |
| `inactive` | Cuenta desactivada | No |

El campo `is_active` (heredado de Django) convive con `status`. La vista de login exige las dos condiciones: `user.is_active and user.status == 'active'`. Mantenga ambas sincronizadas.

### 5.3 Conjuntos de roles

```python
# accounts/permissions.py
ROLES_ADMIN = ('admin',)
ROLES_GESTION = ('admin', 'manager')
ROLES_SEGURIDAD = ('admin', 'manager', 'security')
ROLES_RESIDENTE = ('admin', 'manager', 'resident', 'propietario')
ROLES_TODOS = ('admin', 'manager', 'security', 'resident', 'propietario')
```

Usar siempre estas constantes en vez de escribir las tuplas a mano: si un rol se agrega despuÃ©s, basta con actualizar la constante.

### 5.4 Mecanismo de control de acceso

El sistema aplica permisos en tres capas. Todas se apoyan en el campo `role`.

#### Capa 1 - Decorador para vistas HTML

```python
accounts/decorators.py
from accounts.decorators import role_required
from accounts.permissions import ROLES_GESTION

@login_required
@role_required(*ROLES_GESTION)
def agregar_pago(request):
    ... # renderiza el formulario
```

Si el usuario no tiene el rol, el decorador muestra un mensaje de error y redirige: a `visitantes_index` para seguridad (su Ãºnico mÃ³dulo) y a `inicio` en cualquier otro caso.

#### Capa 2 - Permisos de clase para la API

| Clase | Regla | Se aplica en |
| --- | --- | --- |
| `IsAdmin` | `role in ROLES_ADMIN` | UserViewSet (listar, crear), ResidencialViewSet |
| `IsManager` | `role in ROLES_GESTION` | Propietario, Solicitud, AuditLog, Report |
| `IsAdminOrGestionLectura` | lectura: `ROLES_GESTION`; escritura: solo admin | Garden, Block, Building |
| `IsResident` | `role in ROLES_RESIDENTE` | CommonAreaViewSet, ReservationViewSet |
| `IsGestionOrSoloLectura` | Autenticado y (mÃ©todo seguro o `role in ROLES_GESTION`) | Resident, Payment, MaintenanceCharge, AreaComun, Communication, Notification |
| `CanModifyUser` | admin, o el propio usuario | UserViewSet (detalle, editar, borrar) |
| `CanModifyIncident` | GestiÃ³n; o el que reporta; o el asignado (solo lectura) | IncidentViewSet |
| `CanModifyVisitor` | GestiÃ³n; o security; o residente del apartamento | VisitorViewSet |
| `CanAccessApartment` | GestiÃ³n; o propietario del apartamento; o residente actual | ApartmentViewSet |

*Tabla 5.2 - Permisos DRF personalizados definidos en accounts/permissions.py.*

#### Capa 3 - Contexto de plantilla

Los context processors `modulos_usuario` y `permisos_modulo` publican en los HTML los mÃ³dulos visibles y los permisos de crear, editar y eliminar de cada mÃ³dulo. Es lo que permite ocultar botones segÃºn el rol sin duplicar lÃ³gica en el template.

#### Nombres de los context processors

```python
# accounts/context_processors.py - idea central
MODULOS = [
    {'nombre': 'pagos', 'url': 'pagos_index', 'activo_en': [...]},
    {'nombre': 'incidencias', 'url': 'incidencias_index', 'activo_en': [...]},
    ... # 14 modulos en total
]
ROL_CREADOR, ROL_EDITOR, ROL_ELIMINADOR = ... # tabla de roles por modulo

# Salida al template
{
    'modulos_habilitados': [...], # que ver en el menu
    'modulos_acceso': [...],
    'puede_crear': True,
    'puede_editar': True,
    'puede_eliminar': False,
    'permisos_modulos': {...},
}
```

### 5.5 Matriz de permisos por rol

La tabla siguiente resume el alcance funcional de cada rol. Es la referencia para responder preguntas de soporte y para validar requisitos antes de implementar.

| Capacidad | Admin | GestiÃ³n | Seguridad | Residente | Propietario |
| --- | --- | --- | --- | --- | --- |
| Autorizar registro de usuarios | SÃ­ | No | No | No | No |
| Gestionar roles y permisos | SÃ­ | No | No | No | No |
| Configurar ficha del residencial | SÃ­ | No | No | No | No |
| Registrar y editar departamentos | SÃ­ | SÃ­ | No | No | No |
| Registrar propietarios | SÃ­ | SÃ­ | No | No | No |
| Registrar residentes | SÃ­ | SÃ­ | No | No | No |
| Registrar pagos y cuotas | SÃ­ | SÃ­ | No | No | No |
| Emitir comprobantes de pago | SÃ­ | SÃ­ | No | SÃ­ | SÃ­ |
| Consultar pagos | SÃ­ | SÃ­ | No | Solo los suyos | Solo los suyos |
| Consultar pagos pendientes y vencidos | SÃ­ | SÃ­ | No | No | No |
| Registrar cargos de mantenimiento | SÃ­ | SÃ­ | No | No | No |
| Reportar incidencias | SÃ­ | SÃ­ | No | SÃ­ | SÃ­ |
| Cambiar estado de incidencias | SÃ­ | SÃ­ | No | No | No |
| Ver historial de incidencias | SÃ­ | SÃ­ | No | SÃ­ | SÃ­ |
| Gestionar solicitudes | SÃ­ | SÃ­ | No | No | No |
| Registrar visitantes | SÃ­ | SÃ­ | SÃ­ | No | No |
| Autorizar y controlar accesos | SÃ­ | SÃ­ | SÃ­ | No | No |
| Administrar Ã¡reas comunes | SÃ­ | SÃ­ | No | No | No |
| Reservar Ã¡reas comunes | SÃ­ | SÃ­ | No | SÃ­ | SÃ­ |
| Publicar comunicados | SÃ­ | SÃ­ | No | No | No |
| Ver comunicados | SÃ­ | SÃ­ | SÃ­ | SÃ­ | SÃ­ |
| Ver reportes administrativos | SÃ­ | SÃ­ | No | No | No |
| Usar la bitÃ¡cora de auditorÃ­a | SÃ­ | SÃ­ | No | No | No |
| Acceder al panel /admin/ | SÃ­ | No | No | No | No |

*Tabla 5.3 - Alcance funcional por rol.*

### 5.6 Matriz de acceso por mÃ³dulo

Equivalente a la anterior, pero por mÃ³dulo y por acciÃ³n, que es como el cÃ³digo opera realmente.

| MÃ³dulo | Ver | Crear / editar | Eliminar | Permiso DRF |
| --- | --- | --- | --- | --- |
| Inicio | Todos | - | - | `role_required` |
| Residencial | Admin | Admin | Admin | `IsAdmin` |
| Cuentas | Admin | Admin | Admin | `IsAdmin` / `CanModifyUser` |
| Departamentos | Todos | GestiÃ³n | GestiÃ³n | `IsManager` / `CanAccessApartment` |
| Propietarios | GestiÃ³n | GestiÃ³n | GestiÃ³n | `IsManager` |
| Residentes | GestiÃ³n + propietario | GestiÃ³n | GestiÃ³n | `IsGestionOrSoloLectura` |
| Pagos | Todos | GestiÃ³n | GestiÃ³n | `IsGestionOrSoloLectura` |
| Mantenimientos | Todos | GestiÃ³n | GestiÃ³n | `IsGestionOrSoloLectura` |
| Incidencias | Todos | Todos (crear); GestiÃ³n (editar) | GestiÃ³n | `CanModifyIncident` |
| Solicitudes | GestiÃ³n | GestiÃ³n | GestiÃ³n | `IsManager` |
| Visitantes | Todos | Seguridad + GestiÃ³n | GestiÃ³n | `CanModifyVisitor` |
| Ãreas comunes | Todos | GestiÃ³n | GestiÃ³n | `IsGestionOrSoloLectura` |
| Reservas | Todos | Todos | GestiÃ³n | `IsResident` |
| Comunicados | Todos | GestiÃ³n | GestiÃ³n | `IsGestionOrSoloLectura` |
| Notificaciones | GestiÃ³n | GestiÃ³n | GestiÃ³n | `IsGestionOrSoloLectura` |
| Reportes | GestiÃ³n | GestiÃ³n | - | `IsManager` |
| Chat | Todos | Todos | Todos | `IsAuthenticated` |

*Tabla 5.4 - Acceso por mÃ³dulo y acciÃ³n.*

### 5.7 SesiÃ³n y autenticaciÃ³n

- Login por email. `settings.py` define `LOGIN_URL = '/'`, `LOGIN_REDIRECT_URL = '/inicio'` y `LOGOUT_REDIRECT_URL = '/'`.
- RedirecciÃ³n por rol tras entrar. Seguridad aterriza en `visitantes_index`; admin y gestor sin residencial configurado, en `residencial_index`; el resto, en `inicio`.
- SesiÃ³n en base de datos con duraciÃ³n de 24 horas, expiraciÃ³n al cerrar el navegador, cookie HttpOnly y SameSite=Lax.
- CSRF con cookie HttpOnly y orÃ­genes de confianza configurables.
- API por sesiÃ³n: SessionAuthentication es la Ãºnica clase de autenticaciÃ³n global, y el permiso por defecto es IsAuthenticated.
- ValidaciÃ³n de contraseÃ±as: longitud mÃ­nima de 8, similitud con los datos del usuario, contraseÃ±as comunes y sin solo dÃ­gitos.

> **ADVERTENCIA** â€” El logout exige POST
>
> `cerrar_sesion` solo ejecuta `django_logout` cuando el mÃ©todo es POST. Enlazarlo con un enlace `<a href>` no cierra la sesiÃ³n; use un formulario con botÃ³n o JavaScript.

## 6. Modelo de datos

### 6.1 Convenciones del modelo de datos

- Clave primaria UUID en casi todos los modelos (`id = UUIDField(default=uuid.uuid4, editable=False)`). ExcepciÃ³n: `chat.ChatGroup`, `incidents.IncidentImage` y `reports.AuditLogDetail` usan AutoField implÃ­cito.
- `related_name` explÃ­cito en todas las relaciones inversas. No hay relaciones de tipo ManyToMany propias ni OneToOne en todo el proyecto.
- `on_delete` explÃ­cito en cada ForeignKey. Se usan los cuatro valores con significado distinto: CASCADE, PROTECT, SET_NULL y (en un caso) SET_DEFAULT.
- Ãndices declarados en los campos por los que se filtra o se agrupa (estado, periodo, fechas), y en los compuestos de las consultas frecuentes.
- `unique_together` en las entidades que pertenecen a un padre: un edificio no repite nombre dentro de un jardÃ­n, un apartamento no repite nombre dentro de un edificio.
- Sin lÃ³gica de negocio en `save()` salvo el caso Ãºnico de `residencial.Residencial`, que documenta su excepciÃ³n (ver 6.7).

### 6.2 Mapa relacional

#### Diagrama de relaciones (resumido)

```text
accounts.User --SET_NULL--> structure.Garden (users)
|
+-- es referenciado por casi todos los modulos

structure.Garden --PROTECT--> structure.Block --PROTECT--> structure.Building --PROTECT--> structure.Apartment
|
+---------------------------------------------------------------------+
| SET_NULL (owner) CASCADE PROTECT                                     |
v                 v                v                    v
propietarios      residents.Resident payments.Payment   structure.Apartment
.Propietario      |                  |                    |
|                 | CASCADE          | CASCADE            | registered_by   | SET_NULL
v                 v                  \--SET_NULL--> accounts.User
accounts.User     structure.Apartment

incidents.Incident --CASCADE--> Apartment
+----CASCADE/SET_NULL--> Resident
+----PROTECT--> User (reported_by)
+----SET_NULL--> User (assigned_to)
+-> IncidentImage (CASCADE, related_name='images')
\-> IncidentHistory (CASCADE, related_name='history',
                     changed_by PROTECT sin related_name)

solicitudes.Solicitud --CASCADE--> Apartment; SET_NULL--> Resident
visitors.Visitor --CASCADE--> Apartment; PROTECT--> User (registered_by);
SET_NULL--> User (authorized_by)
maintenance.MaintenanceCharge --SET_NULL--> Apartment (NULL = aplica a todos)
communications.Communication --CASCADE--> Garden; PROTECT--> User (sender)
reservations.Reservation --CASCADE--> areas_comunes.AreaComun
SET_NULL--> Apartment / Resident
CASCADE/SET_NULL--> User (reserved_by / approved_by)
notifications.Notification --CASCADE--> User
chat.ChatMessage --CASCADE--> User (sender / receiver);
SET_NULL--> chat.ChatGroup
reports.AuditLog --CASCADE--> User
\--> AuditLogDetail (CASCADE, related_name='details')

residencial.Residencial <- modelo aislado, sin ninguna FK
```

### 6.3 Estructura fÃ­sica: Jardines, edificios y apartamentos

El nÃºcleo espacial del sistema es una jerarquÃ­a de tres niveles que determina la organizaciÃ³n de casi todos los demÃ¡s mÃ³dulos: los pagos cuelgan de un apartamento, los residentes de un apartamento, las incidencias de un apartamento.

| Modelo | App | Campos principales | Relaciones |
| --- | --- | --- | --- |
| Garden | structure | name (Ãºnico), location, description, is_active | blocks, buildings, users, common_areas, communications |
| Block | structure | name, description, is_active | garden (PROTECT, related_name='blocks'); unique_together (garden, name) |
| Building | structure | name (edificio = torre), number_of_floors, description, is_active | block (PROTECT, related_name='buildings'); garden (PROTECT, se sincroniza con el del bloque en `save()`) |
| Apartment | structure | name, floor, status, photo, is_active | building (CASCADE), owner (SET_NULL -> Propietario) |

*Tabla 6.1 - JerarquÃ­a espacial.*

#### Estados de un departamento

| Valor | Etiqueta | Significado |
| --- | --- | --- |
| `empty` | VacÃ­o | Disponible, sinmogador asignado |
| `occupied` | Ocupado | Alquilado o en uso |
| `maintenance` | En reparaciÃ³n | No disponible temporalmente |
| `blocked` | Bloqueado | Inhabilitado por la administraciÃ³n |

El estado por defecto de un apartamento nuevo es `empty`. El estado se filtra en la vista HTML mediante el parÃ¡metro `?estado=` y en la API mediante `?status=`.

### 6.4 Personas: propietarios y residentes

El sistema distingue dos figuras jurÃ­dicas distintas y las modela por separado:

| Aspecto | propietarios.Propietario | residents.Resident |
| --- | --- | --- |
| QuÃ© representa | El dueÃ±o del inmueble | La persona que ocupa el apartamento |
| Clave de negocio | cedula (Ãºnica) | cedula (Ãºnica) |
| RelaciÃ³n con el apartamento | Apartment.owner (SET_NULL) | Resident.apartment (CASCADE, obligatorio) |
| RelaciÃ³n con el usuario | user (CASCADE, opcional) | user (CASCADE, opcional) |
| Datos de contacto | phone, email, emergency_contact | phone, email, emergency_contact |
| Estado civil | marital_status (5 opciones) | marital_status (5 opciones, duplicadas) |
| Datos adicionales | photo | photo, tipo_relacion, fecha_ingreso, mascotas |
| Orden por defecto | full_name | apartment, full_name |

*Tabla 6.2 - Propietario frente a residente.*

CÃ³mo leerlo: un apartamento puede tener un propietario y N residentes. El propietario no necesita estar, registrado como usuario; el residente puede ser un ocupante sin cuenta. Ambos pueden vincularse a un `accounts.User` opcional para que pueda iniciar sesiÃ³n y ver su informaciÃ³n.

#### Tipo de relaciÃ³n del residente

| Valor | Etiqueta | ImplicaciÃ³n |
| --- | --- | --- |
| `propietario` | Propietario | El residente es tambiÃ©n el dueÃ±o |
| `inquilino` | Inquilino | Ocupa en alquiler |
| `familiar` | Familiar | Pariente del titular |
| `ocupante` | Ocupante | Sin relaciÃ³n contractual (por defecto) |

### 6.5 Dinero: cargos de mantenimiento y pagos

El mÃ³dulo financiero separa el concepto de lo que se cobra del hecho de pago. Es la Ãºnica forma de tener un catÃ¡logo de tarifas independiente de los movimientos reales.

| | maintenance.MaintenanceCharge | payments.Payment |
| --- | --- | --- |
| **QuÃ© es** | El cargo o cuota a cobrar | El pago efectivamente realizado |
| **Campos clave** | concept, periodicity, amount, effective_date, payment_methods | amount, concept, period, payment_date, payment_method, status, receipt_image |
| **Periodicidad** | monthly, quarterly, semiannual, annual | No aplica (se registra por periodo) |
| **Apartamento** | Opcional. NULL significa 'aplica a todos' | Obligatorio (PROTECT) |
| **Residente** | - | Obligatorio (PROTECT) |
| **Estado** | is_active (activo/inactivo) | pending, at_risk, overdue, paid, cancelled |
| **Orden por defecto** | -effective_date | -period |
| **ValidaciÃ³n cruzada** | - | clean(): el residente debe pertenecer al apartamento elegido |

*Tabla 6.3 - CatÃ¡logo de cargos frente a registro de pagos.*

#### Conceptos de pago

| Valor | Etiqueta | Tipo de obligaciÃ³n |
| --- | --- | --- |
| `maintenance` | Mantenimiento | Cuota ordinaria |
| `extraordinary` | Cuota extraordinaria | Cargo adicional puntual |
| `reservation` | Reserva | Cargo por uso de Ã¡rea comÃºn |
| `parking` | Parqueo | Cargo fijo |
| `services` | Servicios | Consumo (agua, luz) |
| `other` | Otro | Cualquier otro concepto |

#### Estados de pago y morosidad

| Estado | Etiqueta | Significado operativo |
| --- | --- | --- |
| `pending` | Pendiente | Registrado, aÃºn no pagado, sin retraso |
| `at_risk` | En riesgo | PrÃ³ximo a vencer; aparece en el panel de pagos por vencer |
| `overdue` | Vencido | VenciÃ³ su periodo sin pago; entra en el reporte de morosidad |
| `paid` | Pagado | Cancelado |
| `cancelled` | Anulado | Registro invalidado, no cuenta para balances |

> **NOTA** â€” CÃ³mo se modela el periodo
>
> El campo `period` es un DateField que representa el PRIMER dÃ­a del mes que se cobra (por ejemplo 2026-09-01 para septiembre de 2026).
>
> Los filtros de la vista HTML (mes, aÃ±o) y de la API (month, year) operan sobre ese campo; las funciones de los reportes calculan el rango de meses con esa misma convenciÃ³n.

### 6.6 Incidencias y su ciclo de vida

El mÃ³dulo de incidencias es el mÃ¡s rico del sistema: maneja clasificaciÃ³n, prioridad, asignaciÃ³n, evidencia, notas de resoluciÃ³n e historial.

#### Ciclo de estados

#### Flujo de trabajo de una incidencia

```text
[ new ] -> [ assigned ] -> [ in_progress ] -> [ resolved ] -> [ closed ]
Nueva   Asignada        En progreso          Resuelta        Cerrada

[ rejected ] (Rechazada) - salida alternativa desde new/assigned
[ resolved ] -> [ in_progress ] (reapertura)
```

| Campo | Opciones | Uso |
| --- | --- | --- |
| `category` | plumbing, electricity, structural, cleaning, security, noise, water, other | ClasificaciÃ³n del reporte |
| `priority` | low, normal, high, urgent | Prioridad de atenciÃ³n |
| `status` | new, assigned, in_progress, resolved, closed, rejected | Estado del flujo |
| `evidence` | FileField (upload a incidentes/evidencia/) | Archivo adjunto principal |
| `resolution_notes` | TextField | DescripciÃ³n de la soluciÃ³n |
| `resolved_at` | DateTimeField | Momento de la resoluciÃ³n |

*Tabla 6.4 - Campos de clasificaciÃ³n y seguimiento de una incidencia.*

#### Tablas Satellite

| Modelo | Para quÃ© sirve | RelaciÃ³n |
| --- | --- | --- |
| IncidentImage | Adjuntar imÃ¡genes mediante URLs externas a la incidencia | incident (CASCADE, related_name='images') |
| IncidentHistory | BitÃ¡cora de cada transiciÃ³n de estado, con autor y comentario | incident (CASCADE, related_name='history') |

> **ADVERTENCIA** â€” Dos mecanismos de adjuntos coexisten
>
> `Incident.evidence` (FileField, subida de archivo) e `IncidentImage` (tabla de URLs) cumplen la misma funciÃ³n. Antes de implementar, decida cuÃ¡l usar y evite generar adjuntos en ambos.

### 6.7 Ficha del residencial

`residencial.Residencial` es un modelo conceptualmente singular: describe el residencial al que pertenece el sistema. No tiene ninguna relaciÃ³n con el resto de modelos.

| Grupo de campos | Contenido |
| --- | --- |
| IdentificaciÃ³n | nombre, rnc |
| DirecciÃ³n | nombre_via, numero_edificacion, sector, codigo_postal, municipio, provincia |
| Estructura | distribucion (torres \| edificios), cantidad_edificios, cantidad_pisos |
| Contacto | telefono, correo |


| Grupo de campos | Contenido | Otros |
| --- | --- | --- |
| | | mapa_iframe (TextField para incrustar un mapa) |

> **NOTA** â€” La distribuciÃ³n es inmutable
>
> Residencial.save() consulta el valor original de distribuciÃ³n y lo restaura si se intenta cambiar. La razÃ³n: una vez definida la estructura del residencial, cambiarla invalidarÃ­a los datos ya cargados. La UI muestra el campo como bloqueado. Consecuencia prÃ¡ctica: si necesita cambiar la distribuciÃ³n, actualice la fila directamente en la base de datos, no desde la aplicaciÃ³n.

### 6.8 Inventario de modelos por aplicaciÃ³n

Resumen de los 25 modelos del sistema, agrupados por aplicaciÃ³n.

| App | Modelos | Cantidad |
| --- | --- | --- |
| accounts | User (AbstractUser con PK UUID, login por email) | 1 |
| configuracion | IntegracionIA (configuraciÃ³n de IA, registro Ãºnico) | 1 |
| login | PasswordResetToken (token de recuperaciÃ³n de contraseÃ±a) | 1 |
| residencial | Residencial (modelo de configuraciÃ³n singular) | 1 |
| structure | Garden, Block, Building, Apartment | 4 |
| propietarios | Propietario | 1 |
| residents | Resident | 1 |
| payments | Payment | 1 |
| maintenance | MaintenanceCharge | 1 |
| incidents | Incident, IncidentImage, IncidentHistory | 3 |
| solicitudes | Solicitud | 1 |
| visitors | Visitor | 1 |
| reservations | Reservation, CommonArea (obsoleto) | 2 |
| areas_comunes | AreaComun | 1 |
| communications | Communication | 1 |
| notifications | Notification | 1 |
| reports | AuditLog, AuditLogDetail | 2 |
| chat | ChatGroup, ChatMessage | 2 |
| inicio | (sin modelos) | 0 |

*Tabla 6.5 - Modelos por aplicaciÃ³n (25 en total).*

### 6.9 Decisiones de diseÃ±o del modelo

#### PROTECT en los vÃ­nculos con el usuario que registra

Varias relaciones usan on_delete=PROTECT para el usuario que creÃ³ el registro: incidencias (reported_by), visitantes (registered_by), comunicados (sender), pagos registrados y el historial de incidencias. La razÃ³n es de trazabilidad: no se debe poder eliminar un usuario que ha generado movimientos o cuya firma aparece en un documento.

#### SET_NULL donde la relaciÃ³n es contextual

Los vÃ­nculos que enriquecen pero no definen el registro usan SET_NULL: el propietario de un apartamento, el cargo que aplica a todos, el garden de un usuario, la asignaciÃ³n de una incidencia, la aprobaciÃ³n de una reserva.

#### CASCADE donde la dependencia es fuerte

Un apartamento que se elimina arrastra sus residentes, pagos, incidencias, solicitudes, visitantes y reservas. Un jardÃ­n arrastra sus edificios y, en cascada, sus apartamentos.

#### Restricciones de integridad a nivel de base de datos

| RestricciÃ³n | Modelo | Efecto |
| --- | --- | --- |
| unique_together (block, name) | Building | No se repiten nombres de edificio dentro de un bloque |
| unique_together (building, name) | Apartment | No se repiten nombres de apartamento dentro de un edificio |
| unique_together (garden, name) | reservations.CommonArea | No se repiten Ã¡reas dentro de un jardÃ­n |
| UniqueConstraint (common_area, start_time, end_time) | Reservation | Bloquea reservas exactamente duplicadas |
| UniqueConstraint (incident, url) | IncidentImage | No se repite la misma URL en una incidencia |
| UniqueConstraint (audit_log, key) | AuditLogDetail | No se repite una clave de detalle en una bitÃ¡cora |
| unique=True | User.email, User.document, Propietario.cedula, Resident.cedula, Garden.name, ChatGroup.name | Claves de negocio Ãºnicas |

*Tabla 6.6 - Restricciones declaradas a nivel de modelo.*

> **ADVERTENCIA** â€” La reserva no valida solapamientos parciales
>
> La UniqueConstraint de Reservation solo impide duplicados exactos de (common_area, start_time, end_time). Dos reservas de 10:00 a 12:00 y de 11:00 a 13:00 en la misma Ã¡rea pasan la validaciÃ³n de base de datos y colisionan. Los horarios de disponibilidad del AreaComun (available_from / available_until / available_days) tampoco se aplican a nivel de modelo: solo se validan en el cÃ³digo del serializer o de la vista.

### 6.10 Claves forÃ¡neas polimÃ³rficas manuales

Dos modelos usan un UUIDField suelto en lugar de una ForeignKey para apuntar a entidades de naturaleza variable. Esto evita una tabla puente, a costa de perder la integridad referencial:

| Modelo | Campo | Apunta a | Riesgo |
| --- | --- | --- | --- |
| communications.Communication | target_id (UUID) + target_type | building_id o user_id, segÃºn target_type | Puede apuntar a un registro ya borrado |
| notifications.Notification | related_id (UUID) | incident_id, payment_id, etc. | Puede apuntar a un registro ya borrado |

*Tabla 6.7 - Referencias sin integridad referencial.*

Si necesita integridad garantizada para estos vÃ­nculos, el camino es un patrÃ³n de referencia genÃ©rica (content_type + object_id) o un modelo puente por tipo.

## 7. API REST

### 7.1 ConfiguraciÃ³n global de DRF

```python
# settings.py (bloque REST_FRAMEWORK que manda)
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS':
        'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
}
```

| Ajuste | Valor | ImplicaciÃ³n |
| --- | --- | --- |
| AutenticaciÃ³n | SessionAuthentication | La API usa la cookie de sesiÃ³n; no hay tokens |
| Permiso por defecto | IsAuthenticated | Cualquier endpoint sin permiso explÃ­cito exige sesiÃ³n |
| PaginaciÃ³n | PageNumberPagination, 20 por pÃ¡gina | Respuesta con count / next / previous / results |
| Filtro | DjangoFilterBackend | Campos declarados en filterset_fields |
| BÃºsqueda | SearchFilter | Campos declarados en search_fields |
| Orden | OrderingFilter | Campos declarados en ordering_fields |

### 7.2 PatrÃ³n de los ViewSets

Los 21 ViewSets del sistema siguen el mismo esqueleto: queryset base filtrado por visibilidad, serializer (a veces elegido por acciÃ³n), permiso de clase, y tres backends de filtro con sus campos declarados.

#### AnatomÃ­a de un ViewSet tÃ­pico

```python
class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsGestionOrSoloLectura]

    # Filtro por query string sobre campos del modelo
    filterset_fields = ['apartment', 'resident', 'status',
                        'payment_method', 'concept']
    # BÃºsqueda de texto libre
    search_fields = ['resident__full_name', 'apartment__number',
                     'resident__cedula']
    # Campos por los que se puede ordenar
    ordering_fields = ['period', 'payment_date', 'status']

    def get_queryset(self):
        # El listado se restringe a lo que le corresponde al usuario
        qs = _pagos_visibles(self.request.user)
        return qs.distinct()
```

### 7.3 Inventario de endpoints

Cada aplicaciÃ³n monta su propio DefaultRouter. No existe un prefijo global /api/: los endpoints cuelgan del prefijo de la app.

| App | Prefijo | ViewSet | Acciones propias |
| --- | --- | --- | --- |
| accounts | /cuentas/ | UserViewSet | login, profile, change_password, logout |
| residencial | /residencial/residencial/ | ResidencialViewSet | - |
| structure | /departamentos/jardines/ | GardenViewSet | IsAdminOrGestionLectura |
| structure | /departamentos/bloques/ | BlockViewSet | IsAdminOrGestionLectura |
| structure | /departamentos/edificios/ | BuildingViewSet | IsAdminOrGestionLectura |
| structure | /departamentos/departamentos/ | ApartmentViewSet | - |
| propietarios | /propietarios/ | PropietarioViewSet | - |
| residents | /residentes/ | ResidentViewSet | - |
| payments | /pagos/registros/ | PaymentViewSet | - |
| maintenance | /mantenimientos/ | MaintenanceChargeViewSet | - |
| incidents | /incidencias/incidencias/ | IncidentViewSet | - |
| incidents | /incidencias/historial/ | IncidentHistoryViewSet (solo lectura) | - |
| solicitudes | /solicitudes/ | SolicitudViewSet | - |
| visitors | /visitantes/registros/ | VisitorViewSet | authorize, reject, check_in, check_out |
| reservations | /reservas/areas-comunes/ | CommonAreaViewSet | - |
| reservations | /reservas/ | ReservationViewSet | - |
| areas_comunes | /areas-comunes/api/ | AreaComunViewSet | - |
| communications | /comunicados/ | CommunicationViewSet | - |
| notifications | /notificaciones/ | NotificationViewSet | - |
| chat | /chat/ | ChatMessageViewSet | - |
| reports | /reportes/bitacoras/ | AuditLogViewSet (solo lectura) | - |
| reports | /reportes/{resumen,pagos,ocupacion}/ | ReportViewSet (acciones) | summary, payments, occupancy |

*Tabla 7.1 - Endpoints registrados por router.*

### 7.4 Operaciones CRUD generadas por el router

Cada ModelViewSet expone automÃ¡ticamente las operaciones estÃ¡ndar. El nombre de la URL aparece en el campo name de cada ruta del router:

| OperaciÃ³n | MÃ©todo HTTP | Ruta | Nombre en el router |
| --- | --- | --- | --- |
| Listar | GET | /prefijo/ | `<basename>-list` |
| Crear | POST | /prefijo/ | `<basename>-list` |
| Detalle | GET | /prefijo/`<pk>`/ | `<basename>-detail` |
| Actualizar | PUT / PATCH | /prefijo/`<pk>`/ | `<basename>-detail` |
| Borrar | DELETE | /prefijo/`<pk>`/ | `<basename>-detail` |
| RaÃ­z de la API | GET | /prefijo/ | `<basename>-root` (navegador) |

El `<pk>` es el UUID del objeto. Las operaciones de creaciÃ³n, actualizaciÃ³n y borrado solo funcionan si el permiso asignado a la acciÃ³n lo permite.

### 7.5 Acciones personalizadas

#### AutenticaciÃ³n y perfil (accounts)

| AcciÃ³n | MÃ©todo | Ruta | Permiso | QuÃ© hace |
| --- | --- | --- | --- | --- |
| login | POST | /cuentas/login/ | AllowAny | Autentica por email y contraseÃ±a |
| profile | GET | /cuentas/profile/ | IsAuthenticated | Devuelve el perfil del usuario autenticado |
| change_password | POST | /cuentas/change_password/ | IsAuthenticated | Cambia la contraseÃ±a validando la actual |
| logout | POST | /cuentas/logout/ | IsAuthenticated | Cierra la sesiÃ³n |

#### Ciclo de vida de un visitante (visitors)

El control de acceso de porterÃ­a se implementa como acciones de detalle. Todas exigen POST y devuelven 403 si el usuario no es de seguridad o gestiÃ³n.

| AcciÃ³n | Ruta | Estado requerido | Resultado |
| --- | --- | --- | --- |
| authorize | POST /visitantes/registros/`<pk>`/authorize/ | pending | Pasa a authorized y registra authorized_by |
| reject | POST /visitantes/registros/`<pk>`/reject/ | pending | Pasa a rejected |
| check_in | POST /visitantes/registros/`<pk>`/check_in/ | authorized | Registra actual_entry y pasa a completed |
| check_out | POST /visitantes/registros/`<pk>`/check_out/ | actual_entry no nula | Registra actual_exit y pasa a completed |

*Tabla 7.2 - Transiciones de estado de un visitante.*

> **NOTA** â€” Estados del visitante
>
> Flujo normal: pending (esperando) -> authorized (autorizado) -> check_in registra la entrada real y check_out la salida. En cualquier momento antes de la entrada se puede rechazar.

#### Reportes (reports)

| AcciÃ³n | Ruta | QuÃ© devuelve |
| --- | --- | --- |
| summary | GET /reportes/resumen/ | 14 mÃ©tricas: totales de apartamentos, ocupados, residentes activos, pagos, incidencias, visitantes, reservas e ingresos mensuales |
| payments | GET /reportes/pagos/ | Conteo e importes por estado de pago; acepta `<apartment>`, `<status>`, `<month>`, `<year>` |
| occupancy | GET /reportes/ocupacion/ | Conteo de apartamentos por estado (vacÃ­o, ocupado, etc.) |

*Tabla 7.3 - Reportes accesibles por API.*

### 7.6 Filtros, bÃºsqueda y ordenamiento

Los tres backends conviven en la misma respuesta. Se combinan en un Ãºnico query string:

#### Combinando filtros en una consulta

```
GET /pagos/registros/
?apartment=<uuid> DjangoFilterBackend (filtro exacto)
&status=overdue DjangoFilterBackend (filtro exacto)
&search=juan SearchFilter (bÃºsqueda en search_fields)
&ordering=-period OrderingFilter (campo en ordering_fields)
&page=2 PageNumberPagination (20 por pÃ¡gina)
```

Los search_fields se pueden recorrer en relaciones (resident__full_name significa buscar en el nombre del residente del pago). Los ordering_fields controlan quÃ© campos se pueden ordenar vÃ­a query string; un campo no listado allÃ­ no es ordenable.

### 7.7 Visibilidad en la API

Los ViewSets no se limitan al permiso de clase: ademÃ¡s recortan el queryset para que un usuario no pueda ver mÃ¡s de lo que le corresponde, aunque tenga permiso de lectura. El recorte se hace en get_queryset() con un filtro por usuario.

#### Recorte de queryset por usuario

```python
def get_queryset(self):
    user = self.request.user
    if user.role in ('admin', 'manager'):
        return Model.objects.all()  # gestiÃ³n ve todo
    return Model.objects.filter(<lo que le toca>).distinct()
```

### 7.8 Formato de las respuestas

Una peticiÃ³n de listado devuelve la estructura de PageNumberPagination:

#### Estructura de una respuesta paginada

```json
{
    "count": 137,               // total de registros que cumplen el filtro
    "next": "http://...page=2", // URL de la siguiente pÃ¡gina (null si es la Ãºltima)
    "previous": null,           // URL de la anterior (null si es la primera)
    "results": [                // la pÃ¡gina actual de resultados
        { "id": "...", "...": "..." },
        ...
    ]
}
```

Los errores de validaciÃ³n devuelven el detalle por campo; los errores de permiso devuelven 403; los de autenticaciÃ³n, 401 (o 403 con sesiÃ³n).

## 8. Frontend: plantillas, CSS y JavaScript

### 8.1 Arquitectura del frontend

El frontend es un servidor renderizado clÃ¡sico, sin framework de JavaScript. Cada pÃ¡gina se renderiza en el
servidor con plantillas de Django, y el JavaScript externo solo aÃ±ade interactividad (diÃ¡logos, filtros asÃ­ncronos,
confirmaciones, mÃ¡scaras de entrada). No hay paso de build, ni bundler, ni npm.

### 8.2 Plantillas

#### Plantilla base y componentes

Toda la interfaz se apoya en `templates/base.html`, que incluye los componentes reutilizables del directorio
`templates/componentes/`:

| Componente | FunciÃ³n |
| --- | --- |
| `base.html` | Esqueleto comÃºn: head, estilos, barra superior, menÃº lateral y bloque de contenido |
| `header.html` | Cabecera superior con el logotipo y el menÃº de usuario |
| `aside.html` | MenÃº lateral de navegaciÃ³n entre mÃ³dulos (respeta los permisos del usuario) |
| `menu_usuario.html` | Desplegable del perfil con opciÃ³n de cerrar sesiÃ³n y editar perfil |
| `modal.html` | Estructura base de los diÃ¡logos (modales) |
| `botones.html` | Botones de acciÃ³n reutilizables (guardar, cancelar, eliminar) |
| `mini_card.html` | Tarjeta compacta para el dashboard |
| `paginacion_tabla.html` | Controles de paginaciÃ³n reutilizables |
| `login.html` | Estructura de la pantalla de inicio de sesiÃ³n |

*Tabla 8.1 - Componentes globales de plantilla.*

#### Plantillas por mÃ³dulo

Cada mÃ³dulo de dominio aporta sus propias plantillas en `<app>/templates/<app>/`. La pestaÃ±a principal de cada
mÃ³dulo se llama siempre `index.html`; los formularios suelen estar en `agregar.html` o `nuevo.html`.

| Vista | Plantilla | Contexto tÃ­pico |
| --- | --- | --- |
| Listado | `index.html` | `page_obj` (paginaciÃ³n), objeto, filtros, `puede_crear/editar/eliminar` |
| Formulario nuevo | `agregar.html` / `nuevo.html` | `form` (ModelForm), `titulo`, `accion` |
| Formulario editar | `agregar.html` / `nuevo.html` | `form`, `instancia`, `editing=True` |
| Perfil | `perfil.html` | `form` de datos personales |

### 8.3 Sistema de diseÃ±o: variables.css

Los estilos se organizan en torno a un archivo de variables que es la fuente Ãºnica de verdad del diseÃ±o.
`static/css/variables.css` define todos los tokens (colores, sombras, bordes, radios, espaciados) y se importa
desde las hojas base.

#### Paleta de colores

El sistema usa una paleta de verdes como color de marca, mÃ¡s una escala de grises para superficies y texto, y una
escala de azules para elementos informativos. Los nombres siguen el patrÃ³n `--<familia>-<tono>`.

| Familia | Ejemplo de variables | Uso |
| --- | --- | --- |
| Verdes (marca) | `--green-500`, `--green-700`, `--green-900` | Color primario, enlaces, acciones, estados activos |
| Blancos (superficies) | `--white-50` a `--white-900` | Fondos de pÃ¡gina, tarjetas, superficies elevadas |
| Negros (texto) | `--black-300`, `--black-500`, `--black-900` | Texto principal, texto secundario, texto deshabilitado |
| Azules (informativo) | `--blue-500`, `--blue-600` | Mensajes informativos, enlaces, foco |

*Tabla 8.2 - Familias de color del sistema de diseÃ±o.*

#### Reglas de uso de las variables

- Todo color, sombra, borde, radio, margen y padding se escribe con una variable, nunca como valor literal
  repetido.
- La Ãºnica unidad px permitida es para bordes y sombras (los tokens `--border-*`, `--borderR-*` y `--shadow-*` ya
  estÃ¡n en px).
- Cualquier otra medida (margen, padding, tamaÃ±o, tipografÃ­a, ancho, alto) se escribe en rem. Con `font-size:
  62.5%` en `:root`, 1rem equivale a 10px.
- Los breakpoints de las media queries se mantienen en px (560px y 900px), que es la prÃ¡ctica estÃ¡ndar.
- Quien use variables debe asegurar que su hoja las importe antes (directamente o vÃ­a `style.css`).

> **BUENA PRACTICA** â€” *Por quÃ© importa*
>
> Centralizar el diseÃ±o en variables permite cambiar la identidad visual completa del sistema editando un solo archivo, y
> garantiza coherencia entre mÃ³dulos. Es la diferencia entre un sistema mantenible y veinte pÃ¡ginas que se parecen pero
> no encajan.

### 8.4 OrganizaciÃ³n de los estilos

| Archivo | Ãmbito | Contenido |
| --- | --- | --- |
| `static/css/variables.css` | Global | Tokens de diseÃ±o (fuente Ãºnica) |
| `static/css/style.css` | Global | Estilos base; importa `variables.css` |
| `static/css/formularios.css` | Global | Secciones, filas, campos, interruptores de los formularios |
| `static/css/tablas.css` | Global | Estilo de las tablas de datos |
| `static/css/paginacion.css` | Global | Controles de paginaciÃ³n |
| `static/css/dialogos.css` | Global | Modales y diÃ¡logos |
| `static/css/acciones.css` | Global | Paneles de acciones del dashboard |
| `static/css/entradas.css` | Global | Campos de entrada |
| `static/css/mediaquerys.css` | Global | Breakpoints comunes |
| `<app>/static/css/*.css` | MÃ³dulo | Estilos especÃ­ficos del mÃ³dulo |

*Tabla 8.3 - OrganizaciÃ³n de las hojas de estilo.*

La separaciÃ³n es deliberada: lo que comparten dos o mÃ¡s mÃ³dulos vive en `static/css/` del proyecto; lo que solo
usa un mÃ³dulo, en su propia carpeta `static/`.

### 8.5 Convenciones de nombres en CSS

Toda la nomenclatura de clases estÃ¡ en espaÃ±ol, con nombres claros y concisos. El proyecto mantiene un mapeo
canÃ³nico desde los nombres genÃ©ricos originales a los nombres en espaÃ±ol:

| Nombre original | Nombre canÃ³nico en el proyecto |
| --- | --- |
| `form-section` | `seccion-formulario` |
| `form-row` | `fila-formulario` |
| `form-field` | `campo-formulario` |
| `select-field` | `campo-seleccion` |
| `input-field` | `campo-entrada` |
| `form-switch-row` | `fila-interruptor` |
| `switch-label` | `etiqueta-interruptor` |
| `switch` / `switch-slider` | `interruptor` / `deslizador-interruptor` |
| `switch-input` | `entrada-interruptor` |
| `dialog-header` | `cabecera-dialogo` |
| `dialog-footer` | `pie-formulario` |
| `dialog-close` | `boton-cerrar` |
| `btn-generar-comprobante` | `btn-comprobante` |
| `Acciones-dashboard` | `panel-acciones` |
| `container-acciones` | `contenedor-acciones` |
| `pag-btn` | `boton-pagina` |
| `pag-num` | `numero-pagina` |
| `paginacion-numeros` | `numeros-paginacion` |

*Tabla 8.4 - Mapeo de nombres de clase.*

Los nombres de archivo siguen la misma lÃ­nea: los estilos especÃ­ficos se llaman como el mÃ³dulo y en espaÃ±ol
(`pagos.css`, `departamentos.css`, `incidencias.css`, `visitantes.css`).

### 8.6 Reglas obligatorias del frontend

> **PENDIENTE / BUG** â€” Reglas de refactor frontend (obligatorias)
>
> 1. Nada de `<script>` inline ni estilos `style=` en el HTML. El Ãºnico `<script>` permitido es `<script src='...'>` para conectar el
>    HTML con su JS. Los manejadores (`onchange`, `onclick`, ...) van dentro del archivo JS externo.
> 2. Estilos y JS compartidos entre apps viven en `static/css/` y `static/js/` del proyecto. Lo especÃ­fico de un mÃ³dulo queda en
>    su `static/` propio.
> 3. El HTML principal de cada mÃ³dulo se llama siempre `index.html`; los demÃ¡s archivos se nombran por su contenido.
> 4. CSS en espaÃ±ol, con nombres claros y concisos. Los valores salen de `variables.css`; px solo para bordes y sombras;
>    rem para todo lo demÃ¡s.
> 5. El JS externo no puede usar etiquetas de plantilla Django. El HTML le pasa los valores con atributos `data-*`
>    (`data-url-comprobante`, `data-pago-apartamento`, `data-departamento`).
> 6. Mantener la responsividad: los estilos compartidos incluyen media queries (breakpoints 560px / 900px) usados por
>    formularios y por la rejilla de acciones.

### 8.7 JavaScript

#### OrganizaciÃ³n

| Archivo | Ãmbito | Responsabilidad |
| --- | --- | --- |
| `static/js/dialogos.js` | Global | Apertura, cierre y control de los modales |
| `static/js/pagos.js` | Global | LÃ³gica compartida del mÃ³dulo de pagos |
| `static/js/mascaras.js` | Global | MÃ¡scaras de entrada (telÃ©fono, cÃ©dula, montants) |
| `static/js/contadores.js` | Global | Contadores animados del dashboard |
| `static/js/menu-movil.js` | Global | Comportamiento del menÃº en mÃ³vil |
| `static/js/usuario-menu.js` | Global | Desplegable del menÃº de usuario |
| `static/js/encabezado-acciones.js` | Global | Barra de acciones superior |
| `<app>/static/js/*.js` | MÃ³dulo | Comportamiento especÃ­fico del mÃ³dulo |

#### CÃ³mo el JS recibe datos del HTML

El punto de fricciÃ³n clÃ¡sico entre plantillas Django y JavaScript son las URLs y los identificadores. La soluciÃ³n del
proyecto es pasar los valores del servidor al script mediante atributos `data-*`, de modo que el JS nunca tenga que
interpretar una etiqueta de plantilla:

#### Puente HTML -> JavaScript con data-*

```html
<!-- HTML: el servidor pasa los valores al navegador por data-* -->
<button data-url-comprobante="{% url 'generar_comprobante' %}"
        data-pago-apartamento="{{ pago.apartment.id }}"
        data-departamento="{{ pago.apartment.name }}">
  Generar comprobante
</button>
```

```js
// JS externo: lee de los data-* (sin etiquetas de plantilla)
document.querySelectorAll('[data-url-comprobante]').forEach(function (btn) {
  btn.addEventListener('click', function () {
    var url = btn.dataset.urlComprobante + '?pago_id=' + btn.dataset.pagoApartamento;
    window.open(url, '_blank');
  });
});
```

> **ATENCION** â€” *Por quÃ© esta regla existe*
>
> Si el JS contuviera `{% url %}` o `{{ var }}`, Django lo renderizarÃ­a como texto literal dentro del archivo `.js` y el script fallarÃ­a en
> tiempo de ejecuciÃ³n. Los `data-*` evitan por completo ese problema y mantienen el JS reutilizable entre pÃ¡ginas.

### 8.8 Accesibilidad y experiencia de usuario

El proyecto aplica varias prÃ¡cticas de usabilidad de forma consistente:

- ConfirmaciÃ³n antes de acciones destructivas (eliminar) mediante diÃ¡logos.
- Mensajes de Ã©xito y de error mediante el sistema de mensajes de Django, renderizados como notificaciones.
- Tablas ordenables y paginadas para manejar volumen de datos.
- Formularios con validaciÃ³n en servidor (ModelForm) y mÃ¡scaras de entrada en el cliente.
- Estados vacÃ­os y de carga considerados en los listados.
- MenÃº lateral que se adapta a mÃ³vil mediante JavaScript y media queries.
- DiseÃ±o responsivo con dos breakpoints principales (560px y 900px).

## 9. Servidor ASGI, tiempo real y tareas asÃ­ncronas

### 9.1 Modelo de despliegue previsto

CONDOSYS estÃ¡ diseÃ±ado para correr sobre una pila ASGI con Daphne como servidor principal. La entrada es
`condosys/asgi.py`.

### 9.2 Estado actual de ASGI

El punto de entrada ASGI es deliberadamente mÃ­nimo: solo expone la aplicaciÃ³n Django como callable, sin enrutar
websockets. Ese es el Ãºnico motivo por el que los websockets no funcionan, aunque el cÃ³digo de channels estÃ©
escrito.

#### condosys/asgi.py

```python
# condosys/asgi.py (completo)
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'condosys.settings')

application = get_asgi_application()
# ^ Solo Django. No hay ProtocolTypeRouter.
```

Existe un mÃ³dulo de routing completo en `chat/routing.py`, y los consumers estÃ¡n implementados en
`chat/consumers.py`. Las rutas definidas son:

```python
# chat/routing.py
websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<user_id>[\w-]+)/$',
            consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/group/(?P<group_name>[\w-]+)/$',
            consumers.GroupChatConsumer.as_asgi()),
    re_path(r'ws/notifications/(?P<user_id>[\w-]+)/$',
            consumers.NotificationConsumer.as_asgi()),
]
```

### 9.3 QuÃ© falta para activar el tiempo real

| Paso | QuÃ© hacer | Archivo |
| --- | --- | --- |
| 1 | AÃ±adir `'channels'` a `INSTALLED_APPS` | `settings.py` |
| 2 | Envolver la aplicaciÃ³n en un `ProtocolTypeRouter` con `'http'` y `'websocket'`, usando `AuthMiddlewareStack` | `condosys/asgi.py` |
| 3 | Incluir las rutas de websocket (`AuthMiddlewareStack(URLRouter(...))`) | `condosys/asgi.py` |
| 4 | Verificar que el channel layer (Redis) estÃ© accesible | `settings.py` `CHANNEL_LAYERS` |
| 5 | Probar el handshake del websocket desde el cliente JS | cliente |

*Tabla 9.1 - Pasos para activar los WebSockets.*

#### Estructura objetivo (referencia)

```python
# Estructura objetivo de asgi.py
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from chat import routing as chat_routing

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    'http': django_asgi_app,
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(chat_routing.websocket_urlpatterns)
        )
    ),
})
```

> **PENDIENTE / BUG** â€” *Punto ciego de seguridad*
>
> Los consumers existentes usan `self.scope['user']`, que solo existe si la conexiÃ³n pasa por `AuthMiddlewareStack`. Sin ese
> middleware, el usuario no se puede resolver y el consumer fallarÃ­a al autenticar.
>
> El `AllowedHostsOriginValidator` es igualmente necesario en producciÃ³n para evitar conexiones websocket desde
> orÃ­genes no autorizados.

### 9.4 Tareas asÃ­ncronas (Celery)

Celery estÃ¡ configurado en settings (broker y backend Redis, serializaciÃ³n JSON, zona horaria America/Bogota)
pero no hay aplicaciÃ³n Celery implementada: no existe el archivo `celery.py` ni el inicializador de la app. Los casos
de uso naturales si se quisiera activar son: envÃ­o de notificaciones por correo, avisos de pago por vencer y limpieza
de sesiones.

## 10. Despliegue en producciÃ³n

### 10.1 Requisitos de producciÃ³n

| Componente | Papel en producciÃ³n |
| --- | --- |
| Gunicorn | Servidor WSGI de aplicaciÃ³n |
| Daphne (ASGI) | Servidor para el tiempo real (cuando se cablee) |
| WhiteNoise | Servidor de archivos estÃ¡ticos desde el propio proceso |
| PostgreSQL | Base de datos de producciÃ³n |
| Nginx / reverse proxy | TerminaciÃ³n TLS y proxy hacia Gunicorn |
| Redis | Channel layer y broker de Celery |

### 10.2 Checklist de despliegue

| # | Paso | Comando / acciÃ³n |
| --- | --- | --- |
| 1 | Rama estable | `git checkout main && git pull` |
| 2 | Entorno virtual | `python -m venv venv && venv\Scripts\activate` |
| 3 | Dependencias | `python -m pip install -r requirements.txt` |
| 4 | Archivo `.env` de producciÃ³n | Configurar `DEBUG=False`, `SECRET_KEY` fuerte, `ALLOWED_HOSTS` del dominio, CORS y CSRF |
| 5 | Migraciones | `python manage.py migrate` |
| 6 | Base de datos | Cambiar `DATABASES` a PostgreSQL y descomentar el bloque |
| 7 | EstÃ¡ticos | `python manage.py collectstatic --noinput` |
| 8 | VerificaciÃ³n | `python manage.py check --deploy` |
| 9 | Superusuario | `python manage.py createsuperuser` |
| 10 | Arranque | `gunicorn condosys.wsgi:application` (con Daphne si hay websockets) |

*Tabla 10.1 - Secuencia de despliegue.*

> **ATENCION** â€” *No olvide collectstatic*
>
> En DEBUG, Django sirve los estÃ¡ticos desde las carpetas de cada app. En producciÃ³n, con `DEBUG=False`, Django no
> los sirve: si no ejecuta `collectstatic`, la aplicaciÃ³n arranca pero aparece sin estilos ni JavaScript.

### 10.3 Conmutar a PostgreSQL

El bloque de PostgreSQL estÃ¡ listo y comentado en `settings.py`. Para activarlo sustituya el bloque de SQLite por el
bloque de PostgreSQL y configure las variables en `.env`.

```python
# settings.py - activar el bloque de PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': os.getenv('DATABASE_ENGINE',
                            'django.db.backends.postgresql'),
        'NAME': os.getenv('DATABASE_NAME', 'condosys_db'),
        'USER': os.getenv('DATABASE_USER', 'postgres'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD', ''),
        'HOST': os.getenv('DATABASE_HOST', 'localhost'),
        'PORT': os.getenv('DATABASE_PORT', '5432'),
        'ATOMIC_REQUESTS': True,
    }
}
```

- Instale el driver con: `python -m pip install psycopg` (ya estÃ¡ en requirements).
- Cree la base de datos y el usuario en PostgreSQL antes de migrar.
- `ATOMIC_REQUESTS=True` envuelve cada peticiÃ³n en una transacciÃ³n, lo que garantiza consistencia pero
  puede afectar al rendimiento con operaciones pesadas.

### 10.4 Seguridad en producciÃ³n

`settings.py` define un bloque de endurecimiento que se activa cuando `DEBUG=False`. Cada variable se lee del `.env`,
de modo que puede ajustarse por entorno:

| Ajuste | PropÃ³sito |
| --- | --- |
| `SECURE_SSL_REDIRECT` | Redirigir todo el trÃ¡fico HTTP a HTTPS |
| `SECURE_HSTS_SECONDS` | DuraciÃ³n del HSTS (31536000 = 1 aÃ±o) |
| `SECURE_HSTS_INCLUDE_SUBDOMAINS` | Incluir subdominios en HSTS |
| `SECURE_HSTS_PRELOAD` | Permitir pre-carga del HSTS en el navegador |
| `SESSION_COOKIE_SECURE` | Cookie de sesiÃ³n solo por HTTPS |
| `CSRF_COOKIE_SECURE` | Cookie CSRF solo por HTTPS |
| `SECURE_CONTENT_TYPE_NOSNIFF` | Prevenir el olfateo de tipos de contenido |
| `SECURE_REFERRER_POLICY` | PolÃ­tica de referencia (`same-origin`) |
| `CSRF_TRUSTED_ORIGINS` | OrÃ­genes de confianza para formularios (dominio de producciÃ³n) |
| `CORS_ALLOWED_ORIGINS` | OrÃ­genes permitidos si hay consumos externos |

*Tabla 10.2 - Ajustes de seguridad disponibles por entorno.*

> **PENDIENTE / BUG** â€” *SECRET_KEY no debe quedar en el repositorio*
>
> La clave secreta se lee del `.env` y `.env` estÃ¡ en `.gitignore`, lo cual es correcto. Verifique que ninguna copia de la clave se
> haya committeado por error antes de publicar el repositorio.

### 10.5 Lista de verificaciÃ³n de seguridad antes de publicar

| # | VerificaciÃ³n | Estado |
| --- | --- | --- |
| 1 | `DEBUG=False` en el `.env` de producciÃ³n | `[ ]` |
| 2 | `SECRET_KEY` Ãºnica, larga y no versionada | `[ ]` |
| 3 | `ALLOWED_HOSTS` limitado a los dominios reales | `[ ]` |
| 4 | `ALLOWED_HOSTS` no incluye comodines en producciÃ³n | `[ ]` |
| 5 | `CSRF_TRUSTED_ORIGINS` configurado con el dominio real | `[ ]` |
| 6 | `SECURE_SSL_REDIRECT` activo (sitio bajo HTTPS) | `[ ]` |
| 7 | Cookies de sesiÃ³n y CSRF marcadas como seguras | `[ ]` |
| 8 | `collectstatic` ejecutado y servido por WhiteNoise | `[ ]` |
| 9 | `manage.py check --deploy` sin avisos crÃ­ticos | `[ ]` |
| 10 | Datos de ejemplo (`poblar_datos`) eliminados | `[ ]` |
| 11 | ContraseÃ±as del superusuario cambiadas | `[ ]` |
| 12 | Redis con autenticaciÃ³n y no expuesto a Internet | `[ ]` |


## 11. Problemas conocidos y deuda tÃ©cnica

Este capÃ­tulo documenta los defectos y limitaciones que hoy existen en el cÃ³digo. Se incluye de forma deliberada: conocerlos antes de tocar el sistema evita descubrimientos en producciÃ³n. Cada punto indica dÃ³nde estÃ¡ el problema y cuÃ¡l es el camino de correcciÃ³n.

### 11.1 ConfiguraciÃ³n (settings.py)

| # | Problema | UbicaciÃ³n | CorrecciÃ³n sugerida |
|---|----------|-----------|---------------------|
| 1 | Bloque `REST_FRAMEWORK` duplicado: el primero define throttling y el segundo lo sobreescribe. El throttling configurado nunca se aplica. | `settings.py` | Consolidar en un solo bloque, con throttling incluido |
| 2 | `AUTH_USER_MODEL` declarado dos veces | `settings.py` | Dejar una sola declaraciÃ³n |
| 3 | `STATIC_URL`, `STATICFILES_DIRS` y `STATIC_ROOT` definidos dos veces | `settings.py` | Eliminar el bloque duplicado |
| 4 | El bloque de seguridad `if not DEBUG` es sobreescrito por el bloque posterior que lee del `.env` | `settings.py` | Unificar en una sola lectura por entorno |
| 5 | `SECRET_KEY` sin valor por defecto; el import de `ImproperlyConfigured` no se usa | `settings.py` | AÃ±adir fallback seguro o error explÃ­cito |

*Tabla 11.1 - Duplicaciones y omisiones en la configuraciÃ³n.*

### 11.2 URLs

| # | Problema | Efecto | CorrecciÃ³n sugerida |
|---|----------|--------|---------------------|
| 5 | En 9 apps, la vista HTML `app_index` estÃ¡ registrada en `''` antes de `include(router.urls)` con el router en `r''`. | El listado HTML tapa el listado JSON: los endpoints `-list` y `-root` de la API quedan inalcanzables en la raÃ­z del prefijo. El `-detail` y las acciones `detail=False` sÃ­ funcionan. | Mover el router a un prefijo propio (por ejemplo `api/`), como ya hace `areas_comunes` |

*Tabla 11.2 - Sombreo de rutas entre HTML y API.*

Apps afectadas: `accounts`, `propietarios`, `residents`, `maintenance`, `solicitudes`, `areas_comunes` (parcialmente), `reservations`, `communications`, `notifications` y `chat`.

### 11.3 Tiempo real

| # | Problema | Efecto | CorrecciÃ³n sugerida |
|---|----------|--------|---------------------|
| 6 | `asgi.py` no usa `ProtocolTypeRouter` | Los WebSockets de chat y notificaciones no se pueden conectar | Cablear el routing (ver capÃ­tulo 9) |
| 7 | `channels` no estÃ¡ en `INSTALLED_APPS` | Channels no inicializa su app | AÃ±adir la app |
| 8 | Consumers sin `AuthMiddlewareStack` | `self.scope['user']` no se resuelve | Envolver el `URLRouter` en `AuthMiddlewareStack` |

*Tabla 11.3 - Estado del tiempo real.*

### 11.4 Modelo de datos

| # | Problema | UbicaciÃ³n | CorrecciÃ³n sugerida |
|---|----------|-----------|---------------------|
| 9 | `chat.ChatMessage.__str__` referencia `self.group_name`, campo que no existe: lanza `AttributeError` en todo mensaje grupal | `chat/models.py` | Usar `self.group.name` y proteger el caso group nulo |
| 10 | Dos modelos para el Ã¡rea comÃºn: `reservations.CommonArea` (con garden) y `areas_comunes.AreaComun` (sin garden). `CommonArea` quedÃ³ huÃ©rfano tras la migraciÃ³n 0003, pero sigue registrado en admin, forms, serializers, ViewSet, router y en el seed. | `reservations/`, `areas_comunes/` | Eliminar `CommonArea` y migrar sus referencias |
| 11 | `AreaComun` no tiene relaciÃ³n con `Garden` ni con `Residencial`: no se puede asignar un Ã¡rea a un jardÃ­n o edificio concreto | `areas_comunes/models.py` | AÃ±adir la FK a `Garden` |
| 12 | PK no uniforme: `chat.ChatGroup`, `incidents.IncidentImage` y `reports.AuditLogDetail` usan `AutoField` | varios | Migrar a `UUIDField` |
| 13 | Import muerto: `Building` en `communications/models.py`; `PROTECT` sin usar en `accounts` y `structure` | varios | Limpiar |
| 14 | `ChatGroup` no define clase `Meta` | `chat/models.py` | AÃ±adir `ordering` y `verbose_name_plural` |
| 15 | FK polimÃ³rficas manuales sin integridad (`Communication.target_id`, `Notification.related_id`) | varios | Referencia genÃ©rica o tabla puente |

*Tabla 11.4 - Inconsistencias del modelo de datos.*

### 11.5 Seguridad y permisos

| # | Problema | Efecto |
|---|----------|--------|
| 16 | El middleware de CORS estÃ¡ activo pero la app `corsheaders` no estÃ¡ en `INSTALLED_APPS` | Las cabeceras CORS probablemente no se aplican |
| 17 | El throttling de DRF estÃ¡ configurado en el bloque que se sobreescribe | No hay lÃ­mite de peticiones a la API |
| 18 | Permisos declarados pero sin usar: `IsResidentOnly`, `IsPropietario`, `IsResidentOrManager`, `IsSecurity`, `CanModifyReservation` | CÃ³digo muerto; `IsResidentOrManager` duplica a `IsResident` |
| 19 | Permisos de objeto aplicados como permiso de clase sin `has_permission`: `CanAccessApartment` y `CanModifyIncident` no restringen los listados | El recorte real depende del filtro de `get_queryset`, no del permiso |
| 20 | Los mensajes de chat no validan rol (solo `login_required`) | Cualquier usuario autenticado puede usar el chat (consistente con la tabla de permisos) |

*Tabla 11.5 - Hallazgos de seguridad y permisos.*

### 11.6 Calidad y pruebas

| # | Problema | Efecto | Riesgo |
|---|----------|--------|--------|
| 21 | Los `tests.py` de todas las apps son plantillas vacÃ­as; no hay suite real | Ninguna regresiÃ³n se detecta automÃ¡ticamente | Alto |
| 22 | No hay linter, formateador ni integraciÃ³n continua | El estilo depende de la disciplina individual | Medio |
| 23 | `requirements.txt` sin versiones fijadas | Instalaciones no reproducibles | Medio |
| 24 | Constantes duplicadas entre apps: `MARITAL_CHOICES` en `propietarios` y `residents`; `PAYMENT_METHOD_CHOICES` en `payments` y `maintenance` | Cambiar una exige cambiar la otra | Bajo |
| 25 | El atributo `filter_fields` (obsoleto en DRF moderno) se usa en `accounts.UserViewSet` | Se ignora silenciosamente; el filtro por rol/estado no se aplica | Medio |
| 26 | EnvÃ­o de datos de demostraciÃ³n: el comando `poblar_datos` crea usuarios con contraseÃ±a conocida | Riesgo si se ejecuta en producciÃ³n | Alto |

*Tabla 11.6 - Deuda tÃ©cnica y riesgos de calidad.*

### 11.7 Orden de trabajo sugerido

Si va a abordar la deuda tÃ©cnica, este orden minimiza el riesgo:

| Prioridad | Tarea | Por quÃ© primero |
|-----------|-------|-----------------|
| 1 | Eliminar los datos de ejemplo del flujo de despliegue y proteger el comando | Riesgo de seguridad directo |
| 2 | Arreglar el sombreado de URLs moviendo los routers a `/api/` | Devuelve la API a la normalidad sin romper la UI |
| 3 | Consolidar los bloques duplicados de `settings.py` | Reduce la confusiÃ³n sobre quÃ© configuraciÃ³n manda |
| 4 | Activar o retirar channels/Celery | Decidir si son capacidad real o cÃ³digo muerto |
| 5 | Arreglar `ChatMessage.__str__` y limpiar permisos sin uso | CorrecciÃ³n de bajo riesgo, alto valor |
| 6 | Escribir la suite de pruebas mÃ­nima (permisos y lÃ³gica de pagos) | Sin esto, cualquier refactor grande es arriesgado |
| 7 | Congelar versiones en `requirements.txt` | Reproducibilidad del despliegue |
| 8 | Unificar los modelos de Ã¡rea comÃºn | Limpieza estructural, hacerla antes de crecer |

*Tabla 11.7 - Backlog tÃ©cnico priorizado.*

## 12. GuÃ­a de mantenimiento y extensiÃ³n

### 12.1 CÃ³mo agregar un mÃ³dulo nuevo

El sistema estÃ¡ diseÃ±ado para que agregar un mÃ³dulo sea mecÃ¡nico. Los pasos:

| # | Paso | Detalle |
|---|------|---------|
| 1 | Crear la app | `python manage.py startapp` (en espaÃ±ol, en plural) |
| 2 | Registrar la app | AÃ±adir `''` a `INSTALLED_APPS` en `settings.py` |
| 3 | Definir el modelo | `models.py` con `UUIDField` como PK, `related_name` en todas las FK, Ã­ndices en los campos de filtro |
| 4 | Crear migraciones | `python manage.py makemigrations && python manage.py migrate` |
| 5 | Definir serializers | `serializers.py` con el serializer de listado y, si difiere, el de detalle |
| 6 | Definir el ViewSet | `views.py` con el ViewSet, `permission_classes`, `filterset_fields`, `search_fields`, `ordering_fields` y `get_queryset` con el filtro de visibilidad |
| 7 | Definir permisos | Usar los permisos de `accounts.permissions`; si hace falta uno nuevo, crearlo allÃ­ |
| 8 | Definir el contexto de permisos | AÃ±adir el mÃ³dulo a `MODULOS` y a las tablas de roles en `accounts/context_processors.py` |
| 9 | Definir rutas | `urls.py` con `app_index` (`@role_required`) y el `DefaultRouter`; registrar en `ROOT_URLCONF` |
| 10 | Definir formularios | `forms.py` con `ModelForms` para crear y editar |
| 11 | Crear plantillas | `index.html` (listado) y `agregar.html` / `nuevo.html` (formulario), extendiendo `base.html` |
| 12 | Crear estilos | `<app>/static/css/<app>.css` importando `variables.css`; reutiliza las clases globales |
| 13 | Crear scripts | `<app>/static/js/<app>.js`; sin script inline, sin estilos inline |
| 14 | Registrar en el admin | `admin.py` con los `ModelAdmin` correspondientes |
| 15 | Probar | `python manage.py check`, luego recorrer el flujo con cada rol |

*Tabla 12.1 - Checklist para agregar un mÃ³dulo.*

### 12.2 CÃ³mo agregar un campo a un modelo

```python
# 1. Modificar el modelo
class Incident(models.Model):
    ...
    categoria_seguridad = models.CharField(max_length=50, blank=True)

# 2. Crear y aplicar la migraciÃ³n
python manage.py makemigrations incidents
python manage.py migrate

# 3. Actualizar el serializer si el campo debe exponerse en la API
class IncidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incident
        fields = '__all__'  # o la lista explÃ­cita

# 4. Si el campo debe filtrarse en la API, declararlo
filterset_fields = [..., 'categoria_seguridad']
```

> **ADVERTENCIA** â€” Cuidado con los `on_delete` al agregar relaciones
>
> Al agregar una ForeignKey, especifique siempre `on_delete` de forma explÃ­cita. `CASCADE` borra en cascada, `PROTECT` impide el borrado y `SET_NULL` deja el campo vacÃ­o. Elegir por defecto puede tener consecuencias irreversibles sobre los datos.

### 12.3 Buenas prÃ¡cticas al escribir cÃ³digo en este proyecto

- Idioma: todo el cÃ³digo, comentarios, nombres de plantilla y mensajes van en espaÃ±ol, salvo los nombres de clase y mÃ©todo de Django/DRF.
- Modelos: `UUIDField` como PK, `related_name` explÃ­cito, `on_delete` explÃ­cito, Ã­ndices en los campos de filtro, `unique_together` en lo que pertenece a un padre.
- Permisos: usar las constantes de cuentas (`ROLES_*`) y los permisos de `accounts.permissions.py`; nunca escribir la tupla de roles a mano.
- Visibilidad: todo listado debe pasar por un helper `_<entidad>_visibles(user)` y terminar en `.distinct()` cuando hay joins.
- Serializers: un serializer de listado ligero y uno de detalle cuando el detalle enriquece; seleccionarlos con `get_serializer_class` segÃºn la acciÃ³n.
- Frontend: sin script inline, sin estilos inline, CSS en espaÃ±ol, tokens de `variables.css`, `rem` excepto bordes y sombras.
- JS y plantillas: pasar datos por `data-*`, nunca por etiquetas de plantilla dentro del JS.
- PaginaciÃ³n: 15 elementos por pÃ¡gina en la vista HTML; 20 en la API (el default de DRF).

### 12.4 CÃ³mo diagnosticar problemas

| SÃ­ntoma | Causa probable | QuÃ© revisar |
|---------|----------------|-------------|
| No arranca: `ImproperlyConfigured` | Falta `DJANGO_SECRET_KEY` en `.env` | El archivo `.env` y que `python-dotenv` lo estÃ© leyendo |
| No arranca: No module named X | Dependencia no instalada o app no registrada | `pip install -r requirements.txt`; `INSTALLED_APPS` |
| Login correcto pero redirige mal | `status` distinto de `'active'` | El campo `status` del usuario |
| La API devuelve HTML en vez de JSON | El listado HTML sombrea el listado JSON | El orden de las rutas en `urls.py` (ver 11.2) |
| Los estilos no cargan en producciÃ³n | `collectstatic` no ejecutado | `STATIC_ROOT` y WhiteNoise |
| Un filtro de la API no hace nada | El campo no estÃ¡ en `filterset_fields`, o se usÃ³ `filter_fields` (obsoleto) | Declarar el campo en `filterset_fields` |
| El JS no encuentra un valor | El HTML no pasa el `data-*` esperado | Revisar que el JS lea `dataset` y que el HTML tenga el atributo |
| Un color no coincide con el diseÃ±o | Se usÃ³ un literal en vez de una variable | Revisar el uso de `variables.css` y las reglas de px/rem |
| Los websockets no conectan | `asgi.py` no enruta websockets | Cablear el `ProtocolTypeRouter` (capÃ­tulo 9) |
| `check` reporta 0 pero algo falla | El bloque de configuraciÃ³n que manda no es el que se lee | Revisar duplicados en `settings.py` |

*Tabla 12.2 - DiagnÃ³stico rÃ¡pido por sÃ­ntoma.*

### 12.5 Comandos de verificaciÃ³n antes de publicar

```bash
# 1. Verificar la configuraciÃ³n (debe reportar 0 problemas)
python manage.py check

# 2. Revisar la configuraciÃ³n de producciÃ³n
python manage.py check --deploy

# 3. Verificar que no hay cambios de modelo pendientes
python manage.py makemigrations --check --dry-run

# 4. Ver el estado de las migraciones
python manage.py showmigrations

# 5. Ejecutar la suite de pruebas
python manage.py test
```

### 12.6 Resumen de la arquitectura en una lÃ­nea

CONDOSYS es un monolito modular de Django: un Ãºnico proyecto y una Ãºnica base de datos, dieciocho aplicaciones de dominio que se comunican exclusivamente a travÃ©s del modelo de usuario compartido y de las relaciones entre modelos, una capa de presentaciÃ³n renderizada en el servidor con un sistema de diseÃ±o basado en variables, y una API REST en paralelo que expone cada mÃ³dulo con los mismos datos y los mismos permisos por rol. Toda la lÃ³gica de negocio vive en el lado del servidor; el JavaScript solo aporta interactividad. El sistema estÃ¡ preparado para escalar hacia tiempo real y base de datos de producciÃ³n, pero ambas rutas requieren trabajo adicional documentado en los capÃ­tulos 9 y 10.


## 13. MÃ³dulos y funciones incorporados en 2026

Este capÃ­tulo documenta las piezas que se aÃ±adieron al sistema despuÃ©s de la primera versiÃ³n del manual y que no aparecÃ­an en los capÃ­tulos anteriores: la aplicaciÃ³n `configuracion`, sus modelos, la recuperaciÃ³n de contraseÃ±a por correo y la lectura de cÃ©dulas con inteligencia artificial. Debe leerse como complemento de los capÃ­tulos 3, 5, 6 y 7.

### 13.1 La aplicaciÃ³n `configuracion`

`configuracion` es una app nueva que centraliza la administraciÃ³n de cuentas de usuario y la conexiÃ³n del sistema con un proveedor de inteligencia artificial. A diferencia del resto de apps, **no expone API REST**: no tiene `ModelViewSet` ni `DefaultRouter`; toda su capa de presentaciÃ³n son vistas de funciÃ³n protegidas.

| Elemento | Valor |
|---|---|
| Ruta base | `/configuracion/` (registrada en `condosys/urls.py`, antes de `login.urls`) |
| PresentaciÃ³n | Templates `configuracion/index.html`, `crear.html` y `editar.html` |
| EstÃ¡ticos | `configuracion/static/configuracion/` (CSS y JS propios) |
| Acceso | Exclusivo del rol `admin` (todas las vistas usan `@role_required('admin')`) |
| API REST | No. Solo vistas HTML de funciÃ³n |

**Vistas y rutas (`configuracion/urls.py`):**

| Nombre de URL | Ruta | Vista | FunciÃ³n |
|---|---|---|---|
| `configuracion_index` | `/configuracion/` | `app_index` | PÃ¡gina principal con pestaÃ±as y listado de usuarios |
| `crear_usuario` | `/configuracion/agregar/` | `crear_usuario` | Alta de usuario con contraseÃ±a temporal |
| `actualizar_usuario` | `/configuracion/actualizar/<uuid:pk>/` | `actualizar_usuario` | EdiciÃ³n de un usuario |
| `eliminar_usuario` | `/configuracion/eliminar/<uuid:pk>/` | `eliminar_usuario` | Baja de usuario (con diÃ¡logo de confirmaciÃ³n) |
| `guardar_ia` | `/configuracion/guardar-ia/` | `guardar_ia` | Guarda proveedor, modelo y API Key de la integraciÃ³n IA |

*Tabla 13.1 - Rutas y vistas de la app configuracion.*

La pantalla `configuracion_index` se organiza en seis pestaÃ±as. Solo **Usuarios** e **IntegraciÃ³n AI** estÃ¡n implementadas; **Seguridad**, **Notificaciones**, **Comprobantes fiscales** y **Preferencias generales** muestran el texto "MÃ³dulo prÃ³ximamente". La opciÃ³n **ConfiguraciÃ³n** del menÃº de usuario (no del menÃº lateral) apunta a `configuracion_index` y solo se renderiza para el rol `admin` (`templates/componentes/menu_usuario.html`). El mÃ³dulo **Residencial** del menÃº lateral sigue existiendo de forma independiente.

**Protecciones de la vista de ediciÃ³n (`actualizar_usuario`):** al editar la propia cuenta se fuerza `role='admin'`, `status='active'` e `is_active=True` para no bloquear el acceso, y `eliminar_usuario` impide borrar la cuenta con la que se estÃ¡ trabajando.

**Formularios (`configuracion/forms.py`):**

| Formulario | Campos | Reglas |
|---|---|---|
| `UsuarioForm` | first_name, last_name, document, avatar, phone, email, role, status, is_active | email y document Ãºnicos (validaciÃ³n propia) |
| `UsuarioCreateForm` | Los anteriores + password y password_confirmation | ContraseÃ±a mÃ­nima de 8 caracteres; se hashea con `set_password` |
| `IntegracionIAForm` | proveedor, modelo, api_key | `api_key` opcional; en blanco conserva la guardada |

*Tabla 13.2 - Formularios de la app configuracion.*

### 13.2 Modelo `configuracion.IntegracionIA`

Registro Ãºnico (singleton lÃ³gico) que guarda la conexiÃ³n con un proveedor de IA. Tiene PK `UUIDField`.

| Campo | Tipo | DescripciÃ³n |
|---|---|---|
| `proveedor` | CharField (choices) | `gpt` (GPT Â· OpenAI), `claude` (Claude Â· Anthropic), `gemini` (Gemini Â· Google), `llama` (Llama Â· Meta), `mistral` (Mistral AI), `deepseek` (DeepSeek), `grok` (Grok Â· xAI). Por defecto `gpt` |
| `modelo` | CharField | Identificador del modelo (texto libre con sugerencias) |
| `api_key` | CharField | Clave de la API; puede quedar en blanco |
| `MODELOS_POR_PROVEEDOR` | dict de clase | Modelos con visiÃ³n por proveedor (ver tabla siguiente) |

*Tabla 13.3 - Modelo IntegracionIA.*

| Proveedor | Modelos con visiÃ³n |
|---|---|
| gpt | gpt-5, gpt-4o, gpt-4.1, gpt-4o-mini, gpt-4.1-mini |
| claude | claude-opus-4, claude-sonnet-4, claude-3-7-sonnet, claude-3.5-sonnet |
| gemini | gemini-2.5-pro, gemini-2.5-flash, gemini-2.0-flash, gemini-1.5-pro |
| mistral | pixtral-large, pixtral-12b, mistral-medium-3, mistral-small-3 |
| grok | grok-4, grok-3 |
| deepseek, llama | Sin modelos con visiÃ³n |

*Tabla 13.3.1 - Modelos con visiÃ³n por proveedor.*

MÃ©todos relevantes: `obtener_unico()` devuelve el registro Ãºnico de configuraciÃ³n (o `None`) y se usa tanto en la vista como en `ia_vision`. El campo `api_key` es un `PasswordInput` con `render_value=True` y botÃ³n de ojo para mostrar u ocultar la clave.

### 13.3 Modelo `login.PasswordResetToken`

Token de un solo uso que respalda la recuperaciÃ³n de contraseÃ±a. PK `UUIDField`.

| Campo | Tipo | DescripciÃ³n |
|---|---|---|
| `user` | FK a `User` (CASCADE) | Cuenta que solicita el restablecimiento (`related_name='password_reset_tokens'`) |
| `token` | CharField(64), Ãºnico, indexado | Valor generado con `secrets.token_hex(32)` |
| `created_at` | DateTimeField | Fecha de emisiÃ³n |
| `expires_at` | DateTimeField | Vencimiento (emisiÃ³n + 30 minutos) |
| `used_at` | DateTimeField (nullable) | Marca de uso; `NULL` mientras no se haya consumido |

*Tabla 13.4 - Campos de PasswordResetToken.*

`Meta` ordena por `-created_at` e incluye el Ã­ndice compuesto `(user, used_at)`. Los mÃ©todos `esta_usado`, `expirado()`, `es_valido()` y `marcar_como_usado()` concentran la lÃ³gica de vigencia.

### 13.4 RecuperaciÃ³n de contraseÃ±a por correo

El flujo se compone de dos vistas de funciÃ³n en `login/views.py`.

| Nombre de URL | Ruta | Vista | Responsabilidad |
|---|---|---|---|
| `recuperar_clave` | `/recuperar-clave/` | `solicitar_recuperacion` | Solicita el correo y envÃ­a el enlace |
| `restablecer_clave` | `/restablecer-clave/` | `restablecer_clave` | Valida el token y guarda la nueva contraseÃ±a |

*Tabla 13.5 - Rutas del flujo de recuperaciÃ³n.*

**Secuencia:**

1. El usuario abre `/recuperar-clave/` desde el enlace "Â¿Se te ha olvidado la clave?" del login y escribe su correo.
2. `solicitar_recuperacion` busca `User` con `is_active=True` y `status='active'`. Si existe, elimina los tokens activos previos, crea uno nuevo (`secrets.token_hex(32)`) que vence en 30 minutos (`DURACION_TOKEN_MINUTOS = 30`) y envÃ­a el correo con el enlace a `/restablecer-clave/?token=...`.
3. La respuesta es siempre el mismo mensaje genÃ©rico, exista o no la cuenta, para evitar la enumeraciÃ³n de usuarios.
4. `restablecer_clave` comprueba que el token no estÃ© usado ni vencido, valida que las dos claves coincidan y pasen `validate_password`, guarda con `set_password` y llama a `marcar_como_usado()`.

**EnvÃ­o del correo.** `login/correos.py::enviar_correo_recuperacion` usa la biblioteca **Resend**. Requiere las variables de entorno `RESEND_API_KEY` y `RESEND_FROM` (valor por defecto `CONDOSYS <onboarding@resend.dev>`). Si falta la API key lanza `RuntimeError`; en modo `DEBUG` registra el enlace en el log en lugar de fallar silenciosamente. El asunto es "Solicitud de restablecimiento de contraseÃ±a".

> **NOTA** â€” RelaciÃ³n con `settings.py`
>
> El bloque "Email Configuration" (EMAIL_BACKEND, EMAIL_HOST, etc.) sigue presente para correo SMTP genÃ©rico; el envÃ­o transaccional de recuperaciÃ³n usa especÃ­ficamente Resend mediante `RESEND_API_KEY` / `RESEND_FROM`.

### 13.5 Lectura de cÃ©dula con inteligencia artificial

El mÃ³dulo de Visitantes incorpora la bÃºsqueda por cÃ©dula a partir de una foto. La lÃ³gica vive en `configuracion/ia_vision.py` y se invoca desde `visitors/views.py::buscar_cedula`.

| Elemento | Valor |
|---|---|
| Ruta | `/visitantes/buscar-cedula/` (nombre `buscar_cedula`, POST multipart) |
| Imagen mÃ¡xima | 8 MB (`MAX_IMAGEN_CEDULA_MB`) |
| Procesamiento | `configuracion/ia_vision.py` con Pillow: valida la imagen y la reduce a JPEG (lado mÃ¡ximo 1280 px) |
| Prompt | Pide los 11 dÃ­gitos de la cÃ©dula dominicana (formato 000-0000000-0) o `NADA` |
| Timeout | 60 segundos |
| Resultado | Redirige a `/visitantes/?documento=<cÃ©dula>` para filtrar el listado |

*Tabla 13.6 - Lectura de cÃ©dula con IA.*

`extraer_digitos()` toma de la respuesta del modelo los primeros 11 dÃ­gitos, o `None` si no hay cÃ©dula legible. La funciÃ³n depende de que la app `configuracion` tenga una `IntegracionIA` con `api_key`; si no, `ia_vision` lanza `ErrorVision`. En la plantilla, el diÃ¡logo "Buscar por cÃ©dula" permite usar la cÃ¡mara del dispositivo o adjuntar un archivo.

### 13.6 Variables de entorno nuevas

| Variable | Uso | Valor por defecto |
|---|---|---|
| `RESEND_API_KEY` | Clave privada de Resend | VacÃ­o |
| `RESEND_FROM` | Remitente verificado del correo | `CONDOSYS <onboarding@resend.dev>` |

*Tabla 13.7 - Variables de entorno del correo transaccional.*

### 13.7 Impacto en los inventarios

- La app `configuracion` se suma a las aplicaciones del proyecto y aporta el modelo `IntegracionIA`.
- La app `login` deja de estar vacÃ­a: aporta `PasswordResetToken`.
- El total de modelos pasa de 23 a **25** (ver la tabla del capÃ­tulo 6.8, actualizada).
- La tabla de rutas principales (capÃ­tulo 4.5) incorpora `/configuracion/`, `/recuperar-clave/`, `/restablecer-clave/` y `/visitantes/buscar-cedula/`.
- La matriz de permisos (capÃ­tulo 5.5) incluye el mÃ³dulo **ConfiguraciÃ³n** como acceso exclusivo del rol `admin`.

