<style>
:root{
  --verde: #163D1F; --fondo: #FEFEFE; --texto: #41413D;
  --texto-sec: #60605D; --texto-met: #ACACAC; --borde: #E7E7E7; --zebra: #F5F5F5;
  --nota-bg: #F6FBF3; --nota-borde: #3DA755;
  --adv-bg: #FFE5B0; --adv-borde: #B57900;
  --err-bg: #FDECEC; --err-borde: #EE443F;
  --exito-bg: #C5E9CD; --aviso-bg: #FFE5B0; --err-bg2: #FDECEC;
}
body{ font-family: Inter, Roboto, 'Segoe UI', Arial, sans-serif; background: var(--fondo); color: var(--texto); font-size: 14px; line-height: 1.6; }
h1{ color: var(--verde); font-weight: 700; font-size: 28px; line-height: 1.2; letter-spacing: .05em; padding: 0 0 8px; margin: 0 0 8px; border-bottom: 3px solid var(--verde); }
.marca{ letter-spacing: .05em; }
h2{ color: var(--verde); font-weight: 600; line-height: 1.3; margin: 28px 0 8px; padding-bottom: 4px; border-bottom: 1px solid var(--borde); }
h3{ color: var(--texto); font-weight: 600; line-height: 1.3; margin: 20px 0 8px; }
h4{ color: var(--texto); font-weight: 600; margin: 16px 0 6px; }
table{ border-collapse: collapse; width: 100%; margin: 16px 0; font-size: 14px; }
th{ background: var(--verde); color: #FEFEFE; font-weight: 600; padding: 10px 14px; text-align: left; }
td{ border: 1px solid var(--borde); padding: 8px 12px; color: var(--texto); }
thead{ display: table-header-group; }
tbody tr:nth-child(even) td{ background: var(--zebra); }
.mencion-ui{ display: inline-block; background: var(--zebra); border: 1px solid var(--borde); color: var(--verde); font-weight: 600; padding: 1px 8px; border-radius: 999px; letter-spacing: .02em; }
.caja{ padding: 12px 16px; border-radius: 6px; margin: 16px 0; font-size: 14px; line-height: 1.6; color: var(--texto); }
.caja-nota{ background: var(--nota-bg); border-left: 3px solid var(--nota-borde); }
.caja-advertencia{ background: var(--adv-bg); border-left: 3px solid var(--adv-borde); }
.caja-error{ background: var(--err-bg); border-left: 3px solid var(--err-borde); }
.caja-etiqueta{ font-weight: 600; color: var(--texto); letter-spacing: .05em; }
.captura{ background: #FBFBFB; border: 1px dashed #B5B6B4; border-radius: 6px; padding: 12px 16px; margin: 16px 0; color: #60605D; }
.captura-titulo{ display: block; font-weight: 600; color: #60605D; letter-spacing: .05em; }
.etiqueta-paso{ display: inline-block; background: var(--zebra); border: 1px solid var(--borde); color: var(--verde); font-weight: 600; border-radius: 999px; padding: 1px 10px; letter-spacing: .02em; }
.badge{ display: inline-block; padding: 1px 10px; border-radius: 999px; font-weight: 600; letter-spacing: .02em; }
.badge-exito{ background: var(--exito-bg); color: var(--verde); }
.badge-aviso{ background: var(--aviso-bg); color: var(--adv-borde); }
.badge-error{ background: var(--err-bg2); color: #D93E39; }
ol li, ul li{ margin: 6px 0; }
strong{ font-weight: 600; }
a{ color: var(--verde); }
</style>

<h1>Manual de Usuario — <span class="marca">CONDOSYS</span></h1>

**Sistema de administración residencial CONDOSYS**

---

## Índice

1. [Guía de Inicio Rápido](#1-guía-de-inicio-rápido)
2. [Conociendo el Sistema](#2-conociendo-el-sistema)
3. [Acceso, Sesión y Mi Perfil](#3-acceso-sesión-y-mi-perfil)
4. [Panel de Inicio](#4-panel-de-inicio)
5. [Departamentos](#5-departamentos)
6. [Propietarios](#6-propietarios)
7. [Residentes](#7-residentes)
8. [Pagos](#8-pagos)
9. [Mantenimientos](#9-mantenimientos)
10. [Incidencias](#10-incidencias)
11. [Solicitudes](#11-solicitudes)
12. [Visitantes](#12-visitantes)
13. [Áreas Comunes](#13-áreas-comunes)
14. [Reservas](#14-reservas)
15. [Comunicados](#15-comunicados)
16. [Reportes](#16-reportes)
17. [Configuración del Residencial](#17-configuración-del-residencial)
18. [Preguntas Frecuentes y Resolución de Problemas](#18-preguntas-frecuentes-y-resolución-de-problemas)

---

## 1. Guía de Inicio Rápido

Si es tu primera vez usando el sistema, completa estos pasos en orden.

### <span class="etiqueta-paso">Paso 1</span> — Inicia sesión

1. Abre la dirección del sistema en tu navegador.
2. Escribe tu <span class="mencion-ui">Email</span>.
3. Escribe tu <span class="mencion-ui">Contraseña</span>.
4. Presiona el botón <span class="mencion-ui">Acceder</span>.

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">Pantalla de acceso a CONDOSYS con los campos Email y Contraseña y el botón Acceder</span></div>

### <span class="etiqueta-paso">Paso 2</span> — Ubica el menú lateral

1. Mira el lado izquierdo de la pantalla.
2. Localiza el panel con el logotipo de <span class="mencion-ui">condosys</span>.
3. Explora los módulos que aparecen debajo del logotipo.

<div class="caja caja-nota"><span class="caja-etiqueta">💡 CONSEJO:</span> Solo verás los módulos que corresponden a tu tipo de usuario. Es normal que no aparezcan todos.</div>

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">Menú lateral con los módulos visibles para el usuario</span></div>

### <span class="etiqueta-paso">Paso 3</span> — Cambia tu contraseña la primera vez

1. Presiona tu nombre en la parte inferior del menú lateral.
2. Selecciona la opción <span class="mencion-ui">Mi perfil</span>.
3. Revisa que tus datos de contacto estén correctos.

<div class="caja caja-advertencia"><span class="caja-etiqueta">⚠️ NOTA:</span> Tu contraseña inicial te la entrega el Administrador o el Encargado de Administración. Si no la recuerdas, solicítales una nueva.</div>

### <span class="etiqueta-paso">Paso 4</span> — Registra tus datos en el sistema

1. Dirígete al módulo <span class="mencion-ui">Departamentos</span>.
2. Ubica el departamento que te corresponde.
3. Verifica que tu nombre figure como propietario.

<div class="caja caja-advertencia"><span class="caja-etiqueta">🔴 IMPORTANTE:</span> Sin departamentos registrados no podrás asignar pagos, incidencias ni reservas.</div>

### <span class="etiqueta-paso">Paso 5</span> — Reporta tus novedades

1. Entra al módulo <span class="mencion-ui">Incidencias</span>.
2. Presiona el botón <span class="mencion-ui">Agregar incidencia</span>.
3. Registra cualquier problema de plomería, electricidad, limpieza, ruido, agua, seguridad u otro.

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">Formulario de reporte de incidencia con el tipo de incidencia y la descripción</span></div>

### <span class="etiqueta-paso">Paso 6</span> — Consulta tus pagos

1. Entra al módulo <span class="mencion-ui">Pagos</span>.
2. Revisa la columna <span class="mencion-ui">Estado</span>.
3. Identifica los registros marcados como <span class="mencion-ui">Pendiente</span>, <span class="mencion-ui">En riesgo</span> o <span class="mencion-ui">Vencido</span>.

<div class="caja caja-nota"><span class="caja-etiqueta">💡 CONSEJO:</span> El enlace <span class="mencion-ui">Ver todos los pagos pendientes</span> del panel de inicio abre el filtro ya aplicado.</div>

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">Tabla de pagos con los estados Pendiente, En riesgo y Vencido destacados</span></div>

### <span class="etiqueta-paso">Paso 7</span> — Reserva un área común

1. Entra al módulo <span class="mencion-ui">Reservas</span>.
2. Presiona el botón <span class="mencion-ui">Agregar reserva</span>.
3. Elige el área común, la fecha y el horario.

<div class="caja caja-advertencia"><span class="caja-etiqueta">🔴 IMPORTANTE:</span> Tu reserva se crea en estado <span class="mencion-ui">Solicitada</span> y espera la aprobación de la administración.</div>

### <span class="etiqueta-paso">Paso 8</span> — Cierra sesión al terminar

1. Presiona tu nombre en la parte inferior del menú lateral.
2. Selecciona la opción <span class="mencion-ui">Cerrar sesión</span>.

---

## 2. Conociendo el Sistema

### 2.1 ¿Qué es CONDOSYS?

CONDOSYS es un sistema de administración residencial. Permite centralizar en un solo lugar la información de los departamentos, sus propietarios y residentes, los pagos, los cargos de mantenimiento, las incidencias, las solicitudes, los visitantes, las reservas de áreas comunes y los comunicados.

### 2.2 Estructura de la pantalla

Al iniciar sesión, la pantalla se divide en cuatro zonas principales:

- <span class="mencion-ui">Menú lateral izquierdo:</span> contiene los módulos disponibles para tu tipo de usuario.
- <span class="mencion-ui">Encabezado superior:</span> muestra el nombre del módulo actual y ofrece los botones de acción (Agregar, Actualizar, Cancelar o Volver).
- <span class="mencion-ui">Zona central:</span> muestra el contenido del módulo, ya sea un formulario o una tabla de registros.
- <span class="mencion-ui">Bloque de usuario (inferior izquierda):</span> muestra tu foto, tu nombre y tu correo, y abre el menú personal.

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">Vista general del sistema con el menú lateral, el encabezado y la tabla central</span></div>

### 2.3 Tipos de usuario y permisos

El sistema adapta su contenido según el tipo de usuario con el que inicias sesión.

| Tipo de usuario | Qué puede hacer |
|---|---|
| **Administrador** | Acceso completo a todos los módulos. Autoriza registros de usuarios, gestiona roles y permisos, configura el residencial y elimina información de cualquier módulo. |
| **Encargado de Administración** | Registra cuotas, pagos y cargos. Consulta y filtra estados de pago y emite comprobantes. Actualiza datos de propietarios y residentes. Da seguimiento a incidencias. Realiza consultas generales. No autoriza usuarios ni administra la configuración del residencial. |
| **Seguridad / Portería** | Registra y controla visitantes y accesos al residencial. No gestiona pagos, cuotas ni información de residentes. No cambia estados de incidencias ni administra reservas. |
| **Residente** | Inicia y cierra sesión. Consulta sus pagos, pagos pendientes y comprobantes. Reporta incidencias y da seguimiento. Consulta el historial de sus incidencias. |
| **Propietario** | Consulta sus pagos y comprobantes. Reporta incidencias y las da seguimiento. Reserva áreas comunes de sus propios departamentos. |

<div class="caja caja-advertencia"><span class="caja-etiqueta">⚠️ NOTA:</span> El tipo de usuario lo asigna el Administrador. Si necesitas un cambio de permisos, comunícate con la administración del residencial.</div>

### 2.4 Módulos disponibles

| Módulo | Descripción | Quién lo ve |
|---|---|---|
| **Inicio** | Panel con resúmenes, pagos por vencer y actividad reciente. | Todos |
| **Departamentos** | Registro y estado de cada unidad del residencial. | Todos |
| **Propietarios** | Datos de los propietarios de los departamentos. | Administración |
| **Residentes** | Datos de las personas que habitan los departamentos. | Administración y propietarios |
| **Pagos** | Registro de cuotas y pagos realizados. | Todos |
| **Mantenimientos** | Cargos recurrentes y su vigencia. | Todos |
| **Incidencias** | Reportes de problemas y su seguimiento. | Todos |
| **Solicitudes** | Trámites y pedidos especiales de los residentes. | Administración |
| **Visitantes** | Control de entrada y salida de visitantes. | Seguridad y administración |
| **Áreas Comunes** | Catálogo de áreas con su horario y reglas. | Todos |
| **Reservas** | Solicitudes de uso de áreas comunes. | Todos |
| **Comunicados** | Avisos y anuncios de la administración. | Todos |
| **Reportes** | Estadísticas y exportaciones de información. | Administración |
| **Residencial** | Configuración general del residencial. | Administrador |

### 2.5 Elementos que se repiten en el sistema

- <span class="mencion-ui">Botón Agregar:</span> crea un registro nuevo.
- <span class="mencion-ui">Botón Actualizar:</span> guarda los cambios de un registro existente.
- <span class="mencion-ui">Botón Cancelar:</span> abandona el formulario sin guardar.
- <span class="mencion-ui">Flecha de volver:</span> regresa al listado del módulo.
- <span class="mencion-ui">Botón Todas las columnas:</span> muestra u oculta columnas de la tabla.
- <span class="mencion-ui">Filtros:</span> permiten decidir qué registros se muestran en la tabla.

<div class="caja caja-advertencia"><span class="caja-etiqueta">⚠️ NOTA:</span> Cuando un filtro no arroja resultados, la tabla muestra el mensaje <span class="mencion-ui">Sin coincidencias</span>.</div>

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">Encabezado de un módulo con el botón Agregar y la flecha de volver</span></div>

### 2.6 Botones de acciones por fila

En la columna <span class="mencion-ui">Acciones</span> de cada tabla aparecen dos íconos:

- <span class="mencion-ui">Lápiz (Editar):</span> abre el registro para modificarlo.
- <span class="mencion-ui">Papelera (Eliminar):</span> abre una ventana de confirmación antes de borrar.

<div class="caja caja-advertencia"><span class="caja-etiqueta">⚠️ NOTA:</span> Los botones <span class="mencion-ui">Editar</span> y <span class="mencion-ui">Eliminar</span> solo aparecen si tu tipo de usuario tiene permiso para esa acción.</div>

---

## 3. Acceso, Sesión y Mi Perfil

### 3.1 Pantalla de inicio de sesión

Al entrar al sistema verás una pantalla dividida en dos partes: a la izquierda, el logotipo de CONDOSYS; a la derecha, el formulario de acceso.

1. Presiona el campo <span class="mencion-ui">Email</span>.
2. Escribe tu correo electrónico.
3. Presiona el campo <span class="mencion-ui">Contraseña</span>.
4. Escribe tu contraseña.
5. Presiona el botón <span class="mencion-ui">Acceder</span>.

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">Formulario de inicio de sesión de CONDOSYS</span></div>

### 3.2 Iniciar sesión

1. Escribe tu <span class="mencion-ui">Email</span>.
2. Escribe tu <span class="mencion-ui">Contraseña</span>.
3. Presiona <span class="mencion-ui">Acceder</span>.

**¿A dónde llegas después de entrar?**

- Si eres <span class="mencion-ui">Administrador</span> o <span class="mencion-ui">Encargado de Administración</span> y el residencial todavía no está configurado, irás directo a la pantalla de configuración.
- Si eres de <span class="mencion-ui">Seguridad / Portería</span>, irás directo a <span class="mencion-ui">Visitantes</span>.
- En cualquier otro caso, irás al <span class="mencion-ui">Inicio</span>.

<div class="caja caja-advertencia"><span class="caja-etiqueta">⚠️ NOTA:</span> Solo pueden entrar las cuentas que estén <span class="mencion-ui">Activas</span>. Las cuentas en estado <em>En verificación</em> o <em>Inactivo</em> son rechazadas.</div>

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">Mensaje de error «El email o la contraseña no son válidos.»</span></div>

### 3.3 Cerrar sesión

1. Presiona el bloque con tu nombre en la parte inferior del menú lateral.
2. Selecciona la opción <span class="mencion-ui">Cerrar sesión</span>.

<div class="caja caja-advertencia"><span class="caja-etiqueta">🔴 IMPORTANTE:</span> Cierra sesión siempre que termines de trabajar, especialmente en equipos compartidos.</div>

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">Menú de usuario desplegado con la opción Cerrar sesión</span></div>

### 3.4 Mi perfil

Accede desde el menú de usuario con la opción <span class="mencion-ui">Mi perfil</span>.

El formulario contiene los siguientes campos:

| Campo | Descripción |
|---|---|
| **Nombre completo** | Obligatorio. Se separa en nombre y apellido. |
| **Cedula** | Opcional. No se puede repetir entre cuentas. |
| **Teléfono** | Opcional. |
| **Correo electrónico** | Obligatorio. Es tu usuario de acceso, por lo que no puede estar repetido. |
| **Fecha de ingreso** | Solo lectura. Muestra la fecha de creación de tu cuenta. |
| **Adjuntar imagen** | Foto de perfil. Formatos JPG, PNG o WEBP, con un máximo de 2 MB. |

**Para actualizar tu información:**

1. Modifica los campos que necesites.
2. Cierra y vuelve a abrir el selector de imagen si quieres cambiar tu foto.
3. Presiona el botón <span class="mencion-ui">Actualizar</span> en el encabezado.

<div class="caja caja-advertencia"><span class="caja-etiqueta">⚠️ NOTA:</span> El tipo de usuario y el estado de tu cuenta <strong>no</strong> se modifican desde <em>Mi perfil</em>. Los gestiona la administración.</div>

<div class="caja caja-advertencia"><span class="caja-etiqueta">⚠️ NOTA:</span> Si cambias tu correo electrónico, 반드시 usa el nuevo correo para iniciar sesión la próxima vez.</div>

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">Pantalla Mi perfil con el formulario de datos personales y la zona de carga de imagen</span></div>

### 3.5 Configuración (Residencial)

La opción <span class="mencion-ui">Configuración</span> del menú de usuario abre el módulo <span class="mencion-ui">Residencial</span>, descrito en el capítulo 17.

<div class="caja caja-advertencia"><span class="caja-etiqueta">⚠️ NOTA:</span> Solo el Administrador puede guardar cambios en esta pantalla. Los demás usuarios la ven en modo de solo lectura.</div>

---

## 4. Panel de Inicio

El <span class="mencion-ui">Inicio</span> es la primera pantalla que ves después de iniciar sesión. Presenta un resumen rápido del estado del residencial.

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">Panel de Inicio con las cuatro tarjetas de resumen superiores</span></div>

### 4.1 Tarjetas de resumen

| Tarjeta | Qué muestra |
|---|---|
| **Departamentos** | Cantidad total de departamentos activos. |
| **Incidencias abiertas** | Incidencias en estado Nueva, Asignada o En progreso. |
| **Pagos pendientes** | Pagos en estado Pendiente, En riesgo o Vencido. |
| **Reservas pendientes** | Reservas que esperan aprobación. |

### 4.2 Pagos pendientes por vencer

Esta tabla muestra los cinco pagos pendientes con la fecha de vencimiento más próxima.

| Columna | Contenido |
|---|---|
| **Departamento** | Unidad a la que corresponde el pago. |
| **Propietario/Residente** | Persona que realiza el pago. |
| **Monto** | Cantidad a pagar. |
| **Vence** | Fecha límite del periodo. |
| **Estado** | Situación actual del pago. |

1. Ubica el enlace <span class="mencion-ui">Ver todos los pagos pendientes</span>.
2. Presiona el enlace para abrir el módulo <span class="mencion-ui">Pagos</span> con el filtro de estado <span class="mencion-ui">Pendiente</span> aplicado.

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">Tabla «Pagos pendientes por vencer» del panel de inicio</span></div>

### 4.3 Acciones rápidas

El panel ofrece accesos directos a las tareas más frecuentes. Las acciones disponibles dependen de tu tipo de usuario.

| Acción | Enlace |
|---|---|
| **Agregar pago** | Abre el formulario de nuevo pago. |
| **Agregar incidencia** | Abre el formulario de nueva incidencia. |
| **Agregar visitante** | Abre el formulario de nuevo visitante. |
| **Agregar comunicado** | Abre el formulario de nuevo comunicado. |
| **Reservas pendientes** | Muestra cuántas reservas esperan aprobación y enlaza al listado filtrado. |

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">Panel «Acciones Rápidas» del inicio</span></div>

### 4.4 Actividad reciente

La lista <span class="mencion-ui">Actividad Reciente</span> muestra los últimos movimientos registrados: nuevos pagos y nuevas incidencias, con el tiempo transcurrido desde su creación.

<div class="caja caja-nota"><span class="caja-etiqueta">💡 CONSEJO:</span> El enlace <span class="mencion-ui">Ver todo</span> está en la parte superior de la lista.</div>

<div class="caja caja-advertencia"><span class="caja-etiqueta">⚠️ NOTA:</span> Actualmente el enlace <span class="mencion-ui">Ver todo</span> no lleva a una pantalla propia; muestra toda la actividad en el propio panel de inicio.</div>

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">Lista «Actividad Reciente» con pagos e incidencias recientes</span></div>

---

## 5. Departamentos

El módulo <span class="mencion-ui">Departamentos</span> gestiona las unidades del residencial y su estado de ocupación.

<div class="caja caja-advertencia"><span class="caja-etiqueta">⚠️ NOTA:</span> Los datos de compelr esta estructura son la base de todo el sistema. Si un departamento no existe, no se le pueden asignar pagos, incidencias ni visitantes.</div>

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">Tabla del módulo Departamentos</span></div>

### 5.1 Ver los departamentos

1. Selecciona <span class="mencion-ui">Departamentos</span> en el menú lateral.
2. Localiza la tabla de departamentos.

**Columnas disponibles:**

| Columna | Contenido |
|---|---|
| **Miniatura** | Fotografía del departamento. |
| **Departamento** | Nombre o número de la unidad. |
| **Edificio / Torre** | Edificio o torre al que pertenece. |
| **Bloque** | Bloque dentro del edificio. |
| **Piso** | Piso en el que se encuentra. |
| **Jardin** | Jardín o conjunto del residencial. |
| **Propietario** | Persona propietaria del departamento. |
| <span class="badge badge-exito">Ocupado</span> | Estado actual de la unidad. |

**Estados posibles de un departamento:**

- <span class="mencion-ui">Vacío</span>
- <span class="mencion-ui">Ocupado</span>
- <span class="mencion-ui">En reparación</span>
- <span class="mencion-ui">Bloqueado</span>

<div class="caja caja-nota"><span class="caja-etiqueta">💡 CONSEJO:</span> Según cómo esté configurado el residencial, la tabla muestra <em>Edificios</em> o <em>Torres</em>, y se ajusta de forma automática.</div>

### 5.2 Filtrar los departamentos

La barra de filtros permite tres cosas:

1. Elige un <span class="mencion-ui">Jardín</span> para ver solo sus departamentos.
2. Elige un <span class="mencion-ui">Edificio o Torre</span> para ver solo sus departamentos.
3. Elige un <span class="mencion-ui">Estado</span> para ver solo las unidades en esa situación.

Para quitar un filtro, selecciona la opción <span class="mencion-ui">Todos...</span> correspondiente.

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">Barra de filtros de Departamentos con los selectores Jardín, Edificio y Estado</span></div>

### 5.3 Agregar un departamento

Solo disponible para Administradores y Encargados de Administración.

1. Selecciona <span class="mencion-ui">Departamentos</span> en el menú lateral.
2. Presiona el botón <span class="mencion-ui">Agregar departamento</span>.
3. Completa el campo <span class="mencion-ui">Apartamento</span> con el nombre o número de la unidad.
4. Elige el <span class="mencion-ui">Propietario</span> en la lista desplegable.
5. Sube una imagen del departamento, si la tienes.
6. Elige la <span class="mencion-ui">Torre</span> o el <span class="mencion-ui">Edificio</span> correspondiente.
7. Elige el <span class="mencion-ui">Bloque</span> correspondiente.
8. Escribe el <span class="mencion-ui">Piso</span>.
9. Activa o desactiva el interruptor <span class="mencion-ui">Ocupado</span>.
10. Presiona el botón <span class="mencion-ui">Agregar</span> en el encabezado.

**Formatos de imagen aceptados:** JPG, PNG o WEBP, con un máximo de 2 MB.

<div class="caja caja-nota"><span class="caja-etiqueta">💡 CONSEJO:</span> El interruptor <span class="mencion-ui">Ocupado</span> es la forma rápida de cambiar el estado de la unidad sin abrir el selector de estados.</div>

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">Formulario «Agregar departamento» con las secciones Información del departamento, Ubicación y Estado</span></div>

### 5.4 Editar un departamento

1. Ubica la fila del departamento que quieres modificar.
2. Presiona el ícono del <span class="mencion-ui">lápiz</span> en la columna <span class="mencion-ui">Acciones</span>.
3. Cambia los campos que necesites.
4. Presiona el botón <span class="mencion-ui">Actualizar</span> en el encabezado.

### 5.5 Eliminar un departamento

1. Ubica la fila del departamento que quieres eliminar.
2. Presiona el ícono de la <span class="mencion-ui">papelera</span> en la columna <span class="mencion-ui">Acciones</span>.
3. Lee el mensaje de confirmación.
4. Presiona el botón <span class="mencion-ui">Sí, Eliminar</span> para confirmar.
5. Presiona el botón <span class="mencion-ui">Cancelar</span> para volver atrás.

<div class="caja caja-advertencia"><span class="caja-etiqueta">🔴 IMPORTANTE:</span> Al eliminar un departamento se borran también sus registros relacionados (pagos, incidencias, solicitudes y visitantes). Esta acción no se puede deshacer.</div>

---

## 6. Propietarios

El módulo <span class="mencion-ui">Propietarios</span> registra a los dueños de los departamentos. Cada propietario puede tener uno o varios departamentos a su nombre.

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">Tabla del módulo Propietarios</span></div>

### 6.1 Ver los propietarios

1. Selecciona <span class="mencion-ui">Propietarios</span> en el menú lateral.
2. Localiza la tabla de propietarios.

**Columnas disponibles:**

| Columna | Contenido |
|---|---|
| **Foto** | Fotografía del propietario. |
| **Nombre completo** | Nombre del propietario. |
| **Cédula** | Documento de identidad. |
| **Estado civil** | Soltero/a, Casado/a, Divorciado/a, Viudo/a u Otro. |
| **Teléfono** | Número de contacto. |
| **Correo** | Correo electrónico. |
| **Contacto de emergencia** | Teléfono de la persona a contactar en una urgencia. |
| **Estado** | Activo o Inactivo. |

### 6.2 Filtrar los propietarios

1. Elige un <span class="mencion-ui">Estado</span> para ver solo propietarios activos o inactivos.
2. Elige un <span class="mencion-ui">Departamento</span> para ver solo los propietarios de esa unidad.

### 6.3 Agregar un propietario

Solo disponible para Administradores y Encargados de Administración.

1. Selecciona <span class="mencion-ui">Propietarios</span> en el menú lateral.
2. Presiona el botón <span class="mencion-ui">Nuevo propietario</span>.
3. Completa la sección <span class="mencion-ui">Información del personal</span> con el nombre, el estado civil, la cédula y la foto de perfil.
4. Completa la sección <span class="mencion-ui">Información de contacto</span> con el teléfono, el correo y el contacto de emergencia.
5. Escribe la <span class="mencion-ui">Contraseña</span> con la que la persona ingressará al sistema.
6. Repite la contraseña en <span class="mencion-ui">Confirmar contraseña</span>.
7. Activa o desactiva el interruptor <span class="mencion-ui">Activo</span>.
8. Presiona el botón <span class="mencion-ui">Agregar</span> en el encabezado.

**Requisitos de la contraseña:**

- Debe tener <span class="mencion-ui">mínimo 8 caracteres</span>.
- Debe coincidir con la confirmación.
- No puede ser demasiado común ni parecerse a los datos de la persona.

<div class="caja caja-advertencia"><span class="caja-etiqueta">🔴 IMPORTANTE:</span> La contraseña que escribas aquí es la única forma en que el propietario podrá entrar al sistema. Entrégasela de forma privada.</div>

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">Formulario «Agregar propietario» con las secciones de información personal, de contacto, contraseña y estado</span></div>

### 6.4 Editar un propietario

1. Ubica la fila del propietario que quieres modificar.
2. Presiona el ícono del <span class="mencion-ui">lápiz</span>.
3. Cambia los campos que necesites.
4. Presiona <span class="mencion-ui">Actualizar</span>.

<div class="caja caja-nota"><span class="caja-etiqueta">💡 CONSEJO:</span> Deja los campos de contraseña en blanco si no quieres cambiar la clave actual.</div>

### 6.5 Eliminar un propietario

1. Ubica la fila del propietario que quieres eliminar.
2. Presiona el ícono de la <span class="mencion-ui">papelera</span>.
3. Presiona <span class="mencion-ui">Sí, Eliminar</span> para confirmar.

---

## 7. Residentes

El módulo <span class="mencion-ui">Residentes</span> registra a las personas que habitan los departamentos, incluidos inquilinos, familiares y ocupantes.

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">Tabla del módulo Residentes</span></div>

### 7.1 Ver los residentes

1. Selecciona <span class="mencion-ui">Residentes</span> en el menú lateral.
2. Localiza la tabla de residentes.

**Columnas disponibles:**

| Columna | Contenido |
|---|---|
| **Foto** | Fotografía del residente. |
| **Nombre completo** | Nombre del residente. |
| **Cédula** | Documento de identidad. |
| **Estado civil** | Soltero/a, Casado/a, Divorciado/a, Viudo/a u Otro. |
| **Teléfono** | Número de contacto. |
| **Contacto de emergencia** | Teléfono de la persona a contactar en una urgencia. |
| **Apartamento** | Departamento que ocupa. |
| **Relación** | Propietario, Inquilino, Familiar u Ocupante. |
| **Fecha de ingreso** | Fecha en que ingresó al residencial. |
| **Mascotas** | Indica si tiene mascotas. |
| **Estado** | Activo o Inactivo. |

### 7.2 Filtrar los residentes

1. Elige un <span class="mencion-ui">Estado</span> para ver solo residentes activos o inactivos.
2. Elige un <span class="mencion-ui">Departamento</span> para ver solo los residentes de esa unidad.

### 7.3 Agregar un residente

Solo disponible para Administradores y Encargados de Administración.

1. Selecciona <span class="mencion-ui">Residentes</span> en el menú lateral.
2. Presiona el botón <span class="mencion-ui">Nuevo residente</span>.
3. Completa la sección <span class="mencion-ui">Información del personal</span> con el nombre, el estado civil, la cédula y la foto.
4. Completa la sección <span class="mencion-ui">Información de contacto</span> con el teléfono, el correo y el contacto de emergencia.
5. Elige el <span class="mencion-ui">Departamento</span> que ocupa.
6. Elige el <span class="mencion-ui">Tipo de relación</span> que tiene con el departamento.
7. Escribe la <span class="mencion-ui">Fecha de ingreso</span>.
8. Indica si tiene <span class="mencion-ui">Mascotas</span>.
9. Escribe la <span class="mencion-ui">Contraseña</span> de acceso.
10. Repite la contraseña en <span class="mencion-ui">Confirmar contraseña</span>.
11. Activa o desactiva el interruptor <span class="mencion-ui">Activo</span>.
12. Presiona el botón <span class="mencion-ui">Agregar</span>.

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">Formulario «Agregar residente» con las secciones de información del personal, de contacto, residencia, contraseña y estado</span></div>

### 7.4 Editar un residente

1. Ubica la fila del residente que quieres modificar.
2. Presiona el ícono del <span class="mencion-ui">lápiz</span>.
3. Cambia los campos que necesites.
4. Presiona <span class="mencion-ui">Actualizar</span>.

### 7.5 Eliminar un residente

1. Ubica la fila del residente que quieres eliminar.
2. Presiona el ícono de la <span class="mencion-ui">papelera</span>.
3. Presiona <span class="mencion-ui">Sí, Eliminar</span> para confirmar.

<div class="caja caja-nota"><span class="caja-etiqueta">💡 CONSEJO:</span> En lugar de eliminar a un residente que ya no vive en el residencial, desactiva el interruptor <span class="mencion-ui">Activo</span>. Así conservas su historial.</div>

---

## 8. Pagos

El módulo <span class="mencion-ui">Pagos</span> registra las cuotas de mantenimiento y los demás cargos aplicados a los departamentos, así como los pagos realizados.

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">Tabla del módulo Pagos</span></div>

### 8.1 Conceptos de cobro

| Concepto | Descripción |
|---|---|
| **Mantenimiento** | Cuota mensual de mantenimiento del residencial. |
| **Cuota extraordinaria** | Cobro adicional aprobado por la asamblea. |
| **Reserva** | Cargo por el uso de un área común. |
| **Parqueo** | Cargo por espacio de parqueo. |
| **Servicios** | Cobro de servicios. |
| **Otro** | Cualquier cargo no contemplado en las categorías anteriores. |

### 8.2 Estados de un pago

| Estado | Significado |
|---|---|
| <span class="badge badge-aviso">Pendiente</span> | El pago aún no se ha realizado. |
| <span class="badge badge-aviso">En riesgo</span> | El pago está próximo a vencer. |
| <span class="badge badge-error">Vencido</span> | El pago pasó su fecha límite. |
| <span class="badge badge-exito">Pagado</span> | El pago fue recibido. |
| <span class="badge badge-error">Anulado</span> | El cobro fue cancelado. |

### 8.3 Métodos de pago

Efectivo, Transferencia, Tarjeta, Cheque, Pago en línea y Otro.

### 8.4 Ver los pagos

1. Selecciona <span class="mencion-ui">Pagos</span> en el menú lateral.
2. Localiza la tabla de pagos.

**Columnas disponibles:**

| Columna | Contenido |
|---|---|
| **Comprobante** | Imagen del recibo, si se adjuntó. |
| **Departamento** | Unidad a la que corresponde el cobro. |
| **Propietario/Residente** | Persona que realiza el pago. |
| **Concepto** | Tipo de cobro. |
| **Monto** | Cantidad del cobro. |
| **Periodo/Mes correspondiente** | Mes al que corresponde el cobro. |
| **Fecha de pago** | Día en que se realizó el pago. |
| **Metodo de pago** | Forma en que se pagó. |
| **Estado** | Situación del pago. |

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">Tabla de Pagos con el filtro de conceptos y el filtro de estados</span></div>

### 8.5 Filtrar los pagos

1. Elige un <span class="mencion-ui">Departamento</span> para ver solo sus cobros.
2. Elige un <span class="mencion-ui">Concepto</span> para ver solo un tipo de cobro.
3. Elige un <span class="mencion-ui">Estado</span> para ver solo los pagos en esa situación.

<div class="caja caja-nota"><span class="caja-etiqueta">💡 CONSEJO:</span> Combina varios filtros a la vez para un análisis más preciso.</div>

### 8.6 Registrar un pago

Solo disponible para Administradores y Encargados de Administración.

1. Selecciona <span class="mencion-ui">Pagos</span> en el menú lateral.
2. Presiona el botón <span class="mencion-ui">Agregar pago</span>.
3. Elige el <span class="mencion-ui">Departamento</span> al que corresponde el cobro.
4. Elige <span class="mencion-ui">Quien paga</span>: *Un propietario* o *Un residente*.
5. Elige a la persona en el desplegable <span class="mencion-ui">Propietarios/Residentes</span>.
6. Escribe el <span class="mencion-ui">Monto</span> del pago.
7. Elige el <span class="mencion-ui">Concepto</span> del cobro.
8. Elige la fecha del <span class="mencion-ui">Período/Mes correspondiente</span>.
9. Elige la <span class="mencion-ui">Fecha del pago</span>.
10. Elige el <span class="mencion-ui">Método de pago</span>.
11. Adjunta la <span class="mencion-ui">Foto del comprobante</span>, si la tienes.
12. Elige el <span class="mencion-ui">Estado</span> del pago.
13. Presiona el botón <span class="mencion-ui">Agregar</span>.

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">Formulario «Agregar pago» con los campos de departamento, quien paga, monto, concepto, periodo y estado</span></div>

**Comportamiento del desplegable de personas:**

1. Al elegir el <span class="mencion-ui">Departamento</span>, la lista de personas se filtra automáticamente.
2. Al elegir <span class="mencion-ui">Quien paga</span>, el campo cambia de nombre: *Propietarios* o *Residentes*.
3. El campo permanece deshabilitado hasta que selecciones *Quien paga*.

<div class="caja caja-advertencia"><span class="caja-etiqueta">⚠️ NOTA:</span> La persona elegida debe pertenecer al departamento seleccionado. Si no coincide, el sistema rechaza el registro.</div>

**Adjuntar el comprobante:**

1. Presiona la zona de imagen del comprobante.
2. Suelta el archivo o selecciónalo desde tu equipo.
3. Verifica la vista previa.
4. Confirma que el archivo sea JPG, PNG o WEBP y no supere los 2 MB.

### 8.7 Generar un comprobante de pago

Esta función está disponible en la pantalla de <span class="mencion-ui">Actualizar pago</span>.

1. Selecciona <span class="mencion-ui">Pagos</span> en el menú lateral.
2. Presiona el ícono del <span class="mencion-ui">lápiz</span> en el pago que quieres facturar.
3. Completa los campos obligatorios del formulario.
4. Presiona el botón <span class="mencion-ui">Generar comprobante</span> del encabezado.
5. El comprobante se abre en una pestaña nueva.
6. Imprime o guarda el documento como PDF.

<div class="caja caja-advertencia"><span class="caja-etiqueta">⚠️ NOTA:</span> El botón <span class="mencion-ui">Generar comprobante</span> permanece deshabilitado hasta que completes los campos obligatorios: departamento, persona, monto, concepto, periodo y estado.</div>

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">Botón «Generar comprobante» del encabezado en la pantalla de actualizar pago</span></div>

### 8.8 Editar un pago

1. Ubica la fila del pago que quieres modificar.
2. Presiona el ícono del <span class="mencion-ui">lápiz</span>.
3. Cambia los campos que necesites.
4. Presiona <span class="mencion-ui">Actualizar</span>.

### 8.9 Eliminar un pago

1. Ubica la fila del pago que quieres eliminar.
2. Presiona el ícono de la <span class="mencion-ui">papelera</span>.
3. Presiona <span class="mencion-ui">Sí, Eliminar</span> para confirmar.

---

## 9. Mantenimientos

El módulo <span class="mencion-ui">Mantenimientos</span> registra los cargos recurrentes del residencial y sus reglas de cobro.

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">Tabla del módulo Mantenimientos</span></div>

### 9.1 Conceptos de mantenimiento

Mantenimiento, Seguridad, Limpieza, Administración, Fondo de reserva, Agua, Electricidad y Otro.

### 9.2 Periodicidades disponibles

| Periodicidad | Frecuencia |
|---|---|
| **Mensual** | Cada mes. |
| **Trimestral** | Cada tres meses. |
| **Semestral** | Cada seis meses. |
| **Anual** | Una vez al año. |

### 9.3 Ver los mantenimientos

1. Selecciona <span class="mencion-ui">Mantenimientos</span> en el menú lateral.
2. Localiza la tabla de cargos.

**Columnas disponibles:**

| Columna | Contenido |
|---|---|
| **Foto** | Imagen del cargo. |
| **Concepto** | Tipo de cargo. |
| **Monto** | Cantidad a cobrar. |
| **Periodicidad** | Frecuencia del cobro. |
| **Departamento** | Departamento al que aplica. |
| **Fecha de generación** | Fecha de vigencia del cargo. |
| **Estado** | Activo o Inactivo. |

### 9.4 Filtrar los mantenimientos

1. Elige un <span class="mencion-ui">Departamento</span> para ver solo sus cargos.
2. Elige un <span class="mencion-ui">Estado</span> para ver solo los cargos activos o inactivos.
3. Elige un <span class="mencion-ui">Año</span> para ver los cargos de un período específico.

### 9.5 Agregar un mantenimiento

Solo disponible para Administradores y Encargados de Administración.

1. Selecciona <span class="mencion-ui">Mantenimientos</span> en el menú lateral.
2. Presiona el botón <span class="mencion-ui">Agregar mantenimiento</span>.
3. Elige el <span class="mencion-ui">Concepto</span> del cargo.
4. Elige la <span class="mencion-ui">Periodicidad</span>.
5. Escribe el <span class="mencion-ui">Monto</span> a cobrar.
6. Elige el <span class="mencion-ui">Departamento</span>, si el cargo aplica solo a una unidad.
7. Elige la <span class="mencion-ui">Fecha de generación</span>.
8. Adjunta la <span class="mencion-ui">Foto del mantenimiento</span>, si la tienes.
9. Activa o desactiva el interruptor <span class="mencion-ui">Activo</span>.
10. Presiona el botón <span class="mencion-ui">Agregar</span>.

<div class="caja caja-nota"><span class="caja-etiqueta">💡 CONSEJO:</span> Si dejas el departamento en blanco, el cargo se aplica a todos los departamentos del residencial.</div>

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">Formulario «Agregar mantenimiento» con concepto, periodicidad, monto, departamento y fecha de generación</span></div>

### 9.6 Editar un mantenimiento

1. Ubica la fila del cargo que quieres modificar.
2. Presiona el ícono del <span class="mencion-ui">lápiz</span>.
3. Cambia los campos que necesites.
4. Presiona <span class="mencion-ui">Actualizar</span>.

### 9.7 Desactivar un mantenimiento

1. Ubica la fila del cargo que quieres dejar de aplicar.
2. Presiona el ícono del <span class="mencion-ui">lápiz</span>.
3. Desactiva el interruptor <span class="mencion-ui">Activo</span>.
4. Presiona <span class="mencion-ui">Actualizar</span>.

<div class="caja caja-advertencia"><span class="caja-etiqueta">🔴 IMPORTANTE:</span> No se recomienda eliminar un cargo ya cobrado. Desactívalo para conservar su historial.</div>

---

## 10. Incidencias

El módulo <span class="mencion-ui">Incidencias</span> permite reportar y dar seguimiento a los problemas del residencial.

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">Tabla del módulo Incidencias</span></div>

### 10.1 Tipos de incidencia

| Tipo | Descripción |
|---|---|
| **Plomería** | Fugas, llaves, desagües y obstrucciones. |
| **Electricidad** | Interruptores, bombillos, tomacorrientes y cables. |
| **Estructural** | Grietas, paredes, techos y pisos. |
| **Limpieza** | Basura, espacios sin limpiar y áreas comunes. |
| **Seguridad** | Puertas, cerraduras, cámaras y accesos. |
| **Ruido** | Ruidos molestos de vecinos o actividades. |
| **Agua** | Suministro, cortes de agua y fugas. |
| **Otro** | Cualquier problema no contemplado arriba. |

### 10.2 Niveles de prioridad

| Prioridad | Significado |
|---|---|
| **Baja** | Puede resolverse sin urgencia. |
| **Normal** | Debe atenderse en el orden habitual. |
| **Alta** | Afecta el bienestar de varios residentes. |
| **Urgente** | Requiere atención inmediata. |

### 10.3 Estados de una incidencia

El recorrido normal de una incidencia es: <span class="mencion-ui">Nueva → Asignada → En progreso → Resuelta → Cerrada</span>.

También puede pasar a <span class="mencion-ui">Rechazada</span>.

### 10.4 Reportar una incidencia

1. Selecciona <span class="mencion-ui">Incidencias</span> en el menú lateral.
2. Presiona el botón <span class="mencion-ui">Agregar incidencia</span>.
3. Elige el <span class="mencion-ui">Departamento</span> donde ocurre el problema.
4. Elige al <span class="mencion-ui">Residente</span> que reporta.
5. Elige el <span class="mencion-ui">Tipo de incidencia</span>.
6. Elige la <span class="mencion-ui">Prioridad</span>.
7. Escribe la <span class="mencion-ui">Descripción</span> del problema.
8. Elige la <span class="mencion-ui">Fecha del reporte</span>.
9. Adjunta la <span class="mencion-ui">Evidencia</span>, si la tienes.
10. Escribe el comentario inicial, si corresponde.
11. Presiona el botón <span class="mencion-ui">Agregar</span>.

**Formatos de evidencia aceptados:** JPG, PNG, WEBP o PDF, con un máximo de 2 MB.

<div class="caja caja-nota"><span class="caja-etiqueta">💡 CONSEJO:</span> Cuanto más específico sea el texto de la descripción, más rápido podrá resolverlo la administración.</div>

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">Formulario «Agregar incidencia» con el tipo de incidencia, la prioridad y la descripción</span></div>

<div class="caja caja-advertencia"><span class="caja-etiqueta">⚠️ NOTA:</span> Si eres residente o propietario, el campo <span class="mencion-ui">Estado</span> no aparece en el formulario. La administración controla el avance de la incidencia.</div>

### 10.5 Consultar las incidencias

1. Selecciona <span class="mencion-ui">Incidencias</span> en el menú lateral.
2. Localiza la tabla de incidencias.

**Columnas disponibles:**

| Columna | Contenido |
|---|---|
| **Evidencia** | Imagen o archivo adjunto. |
| **Departamento** | Unidad donde ocurre el problema. |
| **Residente** | Persona que reporta. |
| **Tipo de incidencia** | Categoría del problema. |
| **Prioridad** | Nivel de urgencia. |
| **Fecha de reporte** | Día en que se reportó. |
| **Descripción** | Detalle del problema. |
| **Comentarios/Actualizaciones** | Último seguimiento registrado. |
| **Estado** | Situación actual. |

### 10.6 Filtrar las incidencias

1. Elige un <span class="mencion-ui">Estado</span> para ver solo incidencias en esa situación.
2. Elige un <span class="mencion-ui">Departamento</span> para ver solo sus incidencias.
3. Elige un <span class="mencion-ui">Residente</span> para ver solo las que reportó esa persona.

### 10.7 Dar seguimiento a una incidencia

Solo disponible para Administradores y Encargados de Administración.

1. Ubica la fila de la incidencia que quieres actualizar.
2. Presiona el ícono del <span class="mencion-ui">lápiz</span>.
3. Cambia el <span class="mencion-ui">Estado</span> según el avance del trabajo.
4. Escribe el comentario o actualización en el campo <span class="mencion-ui">Comentarios/actualizaciones</span>.
5. Presiona el botón <span class="mencion-ui">Actualizar</span>.

Cada cambio de estado queda registrado en el historial de la incidencia junto con la fecha y el responsable.

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">Pantalla «Actualizar incidencia» con el selector de estado y el campo de comentarios</span></div>

### 10.8 Eliminar una incidencia

1. Ubica la fila de la incidencia que quieres eliminar.
2. Presiona el ícono de la <span class="mencion-ui">papelera</span>.
3. Presiona <span class="mencion-ui">Sí, Eliminar</span> para confirmar.

---

## 11. Solicitudes

El módulo <span class="mencion-ui">Solicitudes</span> gestiona trámites y peticiones especiales de los residentes, como certificados, permisos y documentación.

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">Tabla del módulo Solicitudes</span></div>

### 11.1 Tipos de solicitud

| Tipo | Descripción |
|---|---|
| **Certificado** | Solicitud de un certificado de residencia u otro. |
| **Permiso** | Solicitud de autorización para una actividad. |
| **Mantenimiento** | Petición de un trabajo de mantenimiento. |
| **Instalación** | Petición de instalación de equipos o servicios. |
| **Reparación** | Petición de una reparación. |
| **Documentación** | Trámite que requiere documentación. |
| **Otro** | Cualquier solicitud no contemplada arriba. |

### 11.2 Estados de una solicitud

Pendiente, En proceso, Aprobada, Rechazada y Completada.

### 11.3 Ver las solicitudes

1. Selecciona <span class="mencion-ui">Solicitudes</span> en el menú lateral.
2. Localiza la tabla de solicitudes.

**Columnas disponibles:**

| Columna | Contenido |
|---|---|
| **Evidencia** | Documento adjunto. |
| **Departamento** | Unidad que solicita. |
| **Residente** | Persona que solicita. |
| **Tipo de solicitud** | Categoría de la solicitud. |
| **Descripción** | Detalle de lo solicitado. |
| **Fecha de solicitud** | Día en que se realizó el pedido. |
| **Comentarios/Respuesta** | Seguimiento de la administración. |
| **Estado** | Situación actual. |

### 11.4 Filtrar las solicitudes

1. Elige un <span class="mencion-ui">Estado</span> para ver solo las solicitudes en esa situación.
2. Elige un <span class="mencion-ui">Departamento</span> para ver solo sus solicitudes.
3. Elige un <span class="mencion-ui">Residente</span> para ver solo las suyas.

### 11.5 Crear una solicitud

Solo disponible para Administradores y Encargados de Administración.

1. Selecciona <span class="mencion-ui">Solicitudes</span> en el menú lateral.
2. Presiona el botón <span class="mencion-ui">Agregar solicitud</span>.
3. Elige el <span class="mencion-ui">Apartamento</span> que realiza la solicitud.
4. Elige al <span class="mencion-ui">Residente</span> que la presenta.
5. Elige el <span class="mencion-ui">Tipo de solicitud</span>.
6. Escribe la <span class="mencion-ui">Descripción</span> de lo que necesitas.
7. Elige la <span class="mencion-ui">Fecha de solicitud</span>.
8. Adjunta el <span class="mencion-ui">Documento</span> de respaldo, si lo tienes.
9. Presiona el botón <span class="mencion-ui">Agregar</span>.

**Formatos de documento aceptados:** JPG, PNG, WEBP o PDF, con un máximo de 2 MB.

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">Formulario «Agregar solicitud» con el tipo de solicitud, la descripción y el adjunto</span></div>

### 11.6 Responder una solicitud

Solo disponible para Administradores y Encargados de Administración.

1. Ubica la fila de la solicitud que quieres atender.
2. Presiona el ícono del <span class="mencion-ui">lápiz</span>.
3. Escribe la respuesta en el campo <span class="mencion-ui">Comentarios/respuesta</span>.
4. Cambia el <span class="mencion-ui">Estado</span> según el avance.
5. Presiona el botón <span class="mencion-ui">Actualizar</span>.

<div class="caja caja-nota"><span class="caja-etiqueta">💡 CONSEJO:</span> Escribe la respuesta de forma clara para que el residente sepa qué debe hacer.</div>

### 11.7 Eliminar una solicitud

1. Ubica la fila de la solicitud que quieres eliminar.
2. Presiona el ícono de la <span class="mencion-ui">papelera</span>.
3. Presiona <span class="mencion-ui">Sí, Eliminar</span> para confirmar.

---

## 12. Visitantes

El módulo <span class="mencion-ui">Visitantes</span> controla la entrada y salida de las personas que visitan el residencial. Está dirigido al personal de seguridad y a la administración.

<div class="caja caja-advertencia"><span class="caja-etiqueta">🔴 IMPORTANTE:</span> El personal de seguridad inicia sesión en este módulo directamente, sin pasar por el panel de inicio.</div>

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">Tabla del módulo Visitantes</span></div>

### 12.1 Tipos de visitante

| Tipo | Descripción |
|---|---|
| **Familiar** | Parientes de los residentes. |
| **Delivery** | Entregas de paquetes o alimentos. |
| **Técnico** | Técnicos que realizan trabajos. |
| **Proveedor** | Proveedores de bienes o servicios. |
| **Otro** | Cualquier otro tipo de visitante. |

### 12.2 Estados de una visita

| Estado | Significado |
|---|---|
| <span class="badge badge-aviso">Esperando</span> | La visita fue registrada y aún no se autoriza. |
| <span class="badge badge-exito">Autorizado</span> | La visita fue aprobada por la administración. |
| <span class="badge badge-error">Rechazado</span> | La visita fue denegada. |
| <span class="badge badge-exito">Completado</span> | El visitante ya registró su salida. |
| <span class="badge badge-error">Cancelado</span> | La visita fue cancelada. |

### 12.3 Tipos de documento

Cédula, Pasaporte, Licencia de conducir y Otro.

### 12.4 Ver las visitas

1. Selecciona <span class="mencion-ui">Visitantes</span> en el menú lateral.
2. Localiza la tabla de visitas.

**Columnas disponibles:**

| Columna | Contenido |
|---|---|
| **Nombre completo** | Nombre del visitante. |
| **Tipo de visitante** | Categoría de la visita. |
| **Tipo de documento** | Documento de identidad presentado. |
| **Documento** | Número del documento. |
| **Departamento a visitar** | Unidad a la que se dirige. |
| **Autorizado por** | Persona que aprobó el ingreso. |
| **Fecha de entrada** | Fecha y hora programada de entrada. |
| **Fecha de salida** | Fecha y hora programada de salida. |
| **Estado** | Situación actual de la visita. |

### 12.5 Filtrar las visitas

La barra de filtros permite acotar el listado con cinco criterios:

1. Elige un <span class="mencion-ui">Estado</span> de visita.
2. Elige un <span class="mencion-ui">Departamento</span>.
3. Elige un <span class="mencion-ui">Tipo de visitante</span>.
4. Elige un <span class="mencion-ui">Mes</span>.
5. Elige un <span class="mencion-ui">Año</span>.

<div class="caja caja-nota"><span class="caja-etiqueta">💡 CONSEJO:</span> El botón de mes muestra nombres abreviados (Ene, Feb, Mar…) y el de año solo incluye los años con visitas programadas.</div>

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">Barra de filtros de Visitantes con los selectores de estado, departamento, tipo, mes y año</span></div>

### 12.6 Registrar un visitante

1. Selecciona <span class="mencion-ui">Visitantes</span> en el menú lateral.
2. Presiona el botón <span class="mencion-ui">Agregar visitante</span>.
3. Completa la sección <span class="mencion-ui">Información del visitante</span> con el nombre, el tipo de visitante y el tipo de documento.
4. Elige el <span class="mencion-ui">Departamento a visitar</span>.
5. Elige quién <span class="mencion-ui">Autorizó</span> el ingreso.
6. Adjunta la <span class="mencion-ui">Foto del documento</span>, si la tienes.
7. Elige la <span class="mencion-ui">Fecha de entrada</span> programada.
8. Elige la <span class="mencion-ui">Fecha de salida</span>, si corresponde.
9. Elige el <span class="mencion-ui">Estado</span> de la visita.
10. Presiona el botón <span class="mencion-ui">Agregar</span>.

**Formatos de documento aceptados:** JPG, PNG o WEBP, con un máximo de 2 MB.

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">Formulario «Agregar visitante» con las secciones de información del visitante, destino y autorización, y registro de acceso</span></div>

<div class="caja caja-advertencia"><span class="caja-etiqueta">⚠️ NOTA:</span> Si la fecha de salida es anterior o igual a la fecha de entrada, el sistema rechaza el registro.</div>

### 12.7 Editar una visita

1. Ubica la fila de la visita que quieres modificar.
2. Presiona el ícono del <span class="mencion-ui">lápiz</span>.
3. Cambia los campos que necesites.
4. Presiona <span class="mencion-ui">Actualizar</span>.

<div class="caja caja-nota"><span class="caja-etiqueta">💡 CONSEJO:</span> Cambia el <span class="mencion-ui">Estado</span> a <em>Autorizado</em> cuando el visitante sea aprobado para entrar.</div>

### 12.8 Eliminar una visita

1. Ubica la fila de la visita que quieres eliminar.
2. Presiona el ícono de la <span class="mencion-ui">papelera</span>.
3. Presiona <span class="mencion-ui">Sí, Eliminar</span> para confirmar.

---

## 13. Áreas Comunes

El módulo <span class="mencion-ui">Áreas Comunes</span> define qué zonas del residencial se pueden reservar, en qué horario y bajo qué condiciones.

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">Tabla del módulo Áreas Comunes</span></div>

### 13.1 Tipos de área

| Tipo | Descripción |
|---|---|
| **Gazebo** | Zona de reuniones al aire libre. |
| **Salón de eventos** | Espacio para eventos. |
| **Área social** | Espacio de encuentro. |
| **Piscina** | Área de natación. |
| **Cancha deportiva** | Cancha para deportes. |
| **Gimnasio** | Espacio de ejercicio. |
| **Zona de parrillas** | Área con parrillas. |
| **Otro** | Cualquier otra zona. |

### 13.2 Días habilitados

| Opción | Días permitidos |
|---|---|
| **Todos los días** | Cualquier día de la semana. |
| **Lunes a Viernes** | De lunes a viernes. |
| **Fines de semana** | Sábado y domingo. |
| **Personalizado** | Configuración especial. |

### 13.3 Estados de un área

Activo, Inactivo y En mantenimiento.

### 13.4 Ver las áreas comunes

1. Selecciona <span class="mencion-ui">Áreas Comunes</span> en el menú lateral.
2. Localiza la tabla de áreas.

**Columnas disponibles:**

| Columna | Contenido |
|---|---|
| **Nombre** | Nombre del área. |
| **Tipo de área** | Categoría del espacio. |
| **Capacidad** | Número de personas admitidas. |
| **Horario disponible** | Rango de horas en el que se puede usar. |
| **Días habilitados** | Días de la semana permitidos. |
| **Condiciones de uso** | Reglas que deben respetarse. |
| **Estado** | Situación actual del área. |

### 13.5 Filtrar las áreas comunes

1. Elige un <span class="mencion-ui">Tipo de área</span> para ver solo ese tipo de espacio.
2. Elige un <span class="mencion-ui">Estado</span> para ver solo las áreas activas, inactivas o en mantenimiento.

### 13.6 Agregar un área común

Solo disponible para Administradores y Encargados de Administración.

1. Selecciona <span class="mencion-ui">Áreas Comunes</span> en el menú lateral.
2. Presiona el botón <span class="mencion-ui">Agregar área común</span>.
3. Completa la sección <span class="mencion-ui">Información del área</span> con el nombre, el tipo y la capacidad.
4. Elige la hora <span class="mencion-ui">Disponible desde</span>.
5. Elige la hora <span class="mencion-ui">Disponible hasta</span>.
6. Elige los <span class="mencion-ui">Días habilitados</span>.
7. Escribe las <span class="mencion-ui">Condiciones de uso</span> (máximo 400 caracteres).
8. Elige el <span class="mencion-ui">Estado</span> del área.
9. Presiona el botón <span class="mencion-ui">Agregar</span>.

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">Formulario «Agregar área común» con las secciones de información del área, disponibilidad, reglas de uso y estado</span></div>

<div class="caja caja-advertencia"><span class="caja-etiqueta">⚠️ NOTA:</span> La hora de fin debe ser posterior a la hora de inicio. Un área en estado <em>Inactivo</em> no aparece en el formulario de reservas.</div>

### 13.7 Editar un área común

1. Ubica la fila del área que quieres modificar.
2. Presiona el ícono del <span class="mencion-ui">lápiz</span>.
3. Cambia los campos que necesites.
4. Presiona <span class="mencion-ui">Actualizar</span>.

<div class="caja caja-nota"><span class="caja-etiqueta">💡 CONSEJO:</span> Para frenar temporalmente el uso de un área, cámbiale el estado a <span class="mencion-ui">En mantenimiento</span>.</div>

### 13.8 Eliminar un área común

1. Ubica la fila del área que quieres eliminar.
2. Presiona el ícono de la <span class="mencion-ui">papelera</span>.
3. Presiona <span class="mencion-ui">Sí, Eliminar</span> para confirmar.

---

## 14. Reservas

El módulo <span class="mencion-ui">Reservas</span> gestiona las solicitudes de uso de las áreas comunes.

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">Tabla del módulo Reservas</span></div>

### 14.1 Estados de una reserva

| Estado | Significado |
|---|---|
| <span class="badge badge-aviso">Solicitada</span> | La reserva fue enviada y espera revisión. |
| <span class="badge badge-exito">Aprobada</span> | La administración autorizó la reserva. |
| <span class="badge badge-error">Rechazada</span> | La administración denegó la reserva. |
| <span class="badge badge-exito">Completada</span> | El uso del área ya ocurrió. |
| <span class="badge badge-error">Cancelada</span> | La reserva fue cancelada. |

### 14.2 Ver las reservas

1. Selecciona <span class="mencion-ui">Reservas</span> en el menú lateral.
2. Localiza la tabla de reservas.

**Columnas disponibles:**

| Columna | Contenido |
|---|---|
| **Foto** | Fotografía del propietario o residente. |
| **Propietario/Residente** | Persona que realiza la reserva. |
| **Área común** | Espacio reservado. |
| **Departamento** | Unidad del solicitante. |
| **Fecha de reserva** | Día de uso. |
| **Hora de inicio** | Hora de comienzo. |
| **Hora de fin** | Hora de finalización. |
| **Estado** | Situación de la reserva. |

### 14.3 Filtrar las reservas

1. Elige un <span class="mencion-ui">Departamento</span> para ver solo sus reservas.
2. Elige un <span class="mencion-ui">Estado</span> para ver solo las reservas en esa situación.

### 14.4 Crear una reserva

1. Selecciona <span class="mencion-ui">Reservas</span> en el menú lateral.
2. Presiona el botón <span class="mencion-ui">Agregar reserva</span>.
3. Elige el <span class="mencion-ui">Área común</span>.
4. Lee el aviso con el horario y los días permitidos de esa área.
5. Elige el <span class="mencion-ui">Apartamento</span> que realiza la reserva.
6. Elige <span class="mencion-ui">Quien reserva</span>.
7. Elige al <span class="mencion-ui">Propietario/Residente</span> asociado al departamento.
8. Elige la <span class="mencion-ui">Fecha de reserva</span>.
9. Elige la <span class="mencion-ui">Hora de inicio</span>.
10. Elige la <span class="mencion-ui">Hora de fin</span>.
11. Presiona el botón <span class="mencion-ui">Agregar</span>.

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">Formulario «Agregar reserva» con el área común, el horario y las secciones de información y horario</span></div>

**Validaciones del sistema:**

- La hora de fin debe ser <span class="mencion-ui">posterior</span> a la hora de inicio.
- La reserva debe caer <span class="mencion-ui">dentro del horario</span> del área seleccionada.
- La fecha debe coincidir con los <span class="mencion-ui">días habilitados</span> del área.
- El propietario o residente debe <span class="mencion-ui">pertenecer</span> al departamento elegido.

<div class="caja caja-advertencia"><span class="caja-etiqueta">⚠️ NOTA:</span> Si eres residente o propietario, el campo <span class="mencion-ui">Estado</span> no aparece en el formulario. Tu reserva se crea en estado <em>Solicitada</em> y la administración decide si la aprueba.</div>

<div class="caja caja-advertencia"><span class="caja-etiqueta">⚠️ NOTA:</span> Solo se muestran las áreas que están en estado <span class="mencion-ui">Activo</span>.</div>

### 14.5 Aprobar o rechazar una reserva

Solo disponible para Administradores y Encargados de Administración.

1. Ubica la fila de la reserva que quieres revisar.
2. Presiona el ícono del <span class="mencion-ui">lápiz</span>.
3. Elige el <span class="mencion-ui">Estado</span>: *Aprobada*, *Rechazada*, *Completada* o *Cancelada*.
4. Presiona el botón <span class="mencion-ui">Actualizar</span>.

<div class="caja caja-nota"><span class="caja-etiqueta">💡 CONSEJO:</span> El panel de inicio muestra un acceso directo con el número de reservas que esperan aprobación.</div>

### 14.6 Editar una reserva

1. Ubica la fila de la reserva que quieres modificar.
2. Presiona el ícono del <span class="mencion-ui">lápiz</span>.
3. Cambia los campos que necesites.
4. Presiona <span class="mencion-ui">Actualizar</span>.

### 14.7 Eliminar una reserva

1. Ubica la fila de la reserva que quieres eliminar.
2. Presiona el ícono de la <span class="mencion-ui">papelera</span>.
3. Presiona <span class="mencion-ui">Sí, Eliminar</span> para confirmar.

---

## 15. Comunicados

El módulo <span class="mencion-ui">Comunicados</span> publica avisos y anuncios de la administración para toda la comunidad.

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">Tabla del módulo Comunicados</span></div>

### 15.1 Categorías de comunicado

Aviso, Mantenimiento, Evento, Seguridad, Piscinas y General.

### 15.2 Destinatarios

| Opción | Descripción |
|---|---|
| **General** | Dirigido a toda la comunidad. |
| **Por edificio** | Dirigido a los residentes de un edificio específico. |
| **Para residente** | Dirigido a un residente en particular. |

### 15.3 Estados de un comunicado

- <span class="mencion-ui">Publicado:</span> visible para todos los destinatarios.
- <span class="mencion-ui">Borrador:</span> en preparación, todavía no visible.

### 15.4 Ver los comunicados

1. Selecciona <span class="mencion-ui">Comunicados</span> en el menú lateral.
2. Localiza la tabla de comunicados.

**Columnas disponibles:**

| Columna | Contenido |
|---|---|
| **Archivo/Imagen** | Imagen adjunta al comunicado. |
| **Título** | Encabezado del aviso. |
| **Categoría** | Tipo de comunicado. |
| **Mensaje** | Contenido del aviso. |
| **Dirigido a** | Destinatarios del comunicado. |
| **Fecha de publicación** | Día en que se publicó. |
| **Estado** | Publicado o Borrador. |

### 15.5 Filtrar los comunicados

1. Elige una <span class="mencion-ui">Categoría</span> para ver solo ese tipo de aviso.
2. Elige un <span class="mencion-ui">Estado</span> para ver solo los publicados o solo los borradores.

### 15.6 Publicar un comunicado

Solo disponible para Administradores y Encargados de Administración.

1. Selecciona <span class="mencion-ui">Comunicados</span> en el menú lateral.
2. Presiona el botón <span class="mencion-ui">Agregar comunicado</span>.
3. Escribe el <span class="mencion-ui">Título</span> del aviso.
4. Elige la <span class="mencion-ui">Categoría</span>.
5. Escribe el <span class="mencion-ui">Mensaje</span> (máximo 400 caracteres).
6. Adjunta una <span class="mencion-ui">Imagen</span>, si la tienes.
7. Elige a quién va <span class="mencion-ui">Dirigido</span>.
8. Elige la <span class="mencion-ui">Fecha de publicación</span>.
9. Elige el <span class="mencion-ui">Estado</span>: *Publicado* o *Borrador*.
10. Presiona el botón <span class="mencion-ui">Agregar</span>.

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">Formulario «Agregar comunicado» con el título, la categoría, el mensaje y el estado</span></div>

<div class="caja caja-advertencia"><span class="caja-etiqueta">⚠️ NOTA:</span> El mensaje no puede superar los 400 caracteres. La imagen opcional debe ser JPG, PNG o WEBP y pesar menos de 2 MB.</div>

### 15.7 Editar un comunicado

1. Ubica la fila del comunicado que quieres modificar.
2. Presiona el ícono del <span class="mencion-ui">lápiz</span>.
3. Cambia los campos que necesites.
4. Presiona <span class="mencion-ui">Actualizar</span>.

### 15.8 Eliminar un comunicado

1. Ubica la fila del comunicado que quieres eliminar.
2. Presiona el ícono de la <span class="mencion-ui">papelera</span>.
3. Presiona <span class="mencion-ui">Sí, Eliminar</span> para confirmar.

---

## 16. Reportes

El módulo <span class="mencion-ui">Reportes</span> consolida la información del residencial y permite exportarla para su análisis.

<div class="caja caja-advertencia"><span class="caja-etiqueta">⚠️ NOTA:</span> Solo Administradores y Encargados de Administración tienen acceso a este módulo.</div>

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">Panel de Reportes con las cuatro tarjetas de indicadores</span></div>

### 16.1 Indicadores del sistema

En la parte superior se muestran cuatro tarjetas con el estado general del residencial:

| Indicador | Qué mide |
|---|---|
| **Ingresos del mes** | Total de pagos recibidos en el mes en curso. |
| **Morosidad** | Suma de todos los pagos vencidos y en riesgo. |
| **Ocupación** | Porcentaje de departamentos ocupados. |
| **Incidencias abiertas** | Incidencias en estado Nueva, Asignada o En progreso. |

### 16.2 Tipos de reporte disponibles

| Reporte | Contenido |
|---|---|
| **Apartamentos ocupados / disponibles** | Lista de departamentos con su estado. |
| **Residentes activos** | Solo los residentes marcados como activos. |
| **Pagos realizados** | Pagos en estado Pagado. |
| **Pagos pendientes** | Pagos en estado Pendiente. |
| **Morosidad** | Pagos en estado En riesgo o Vencido. |
| **Incidencias por estado** | Incidencias con su categoría, prioridad y estado. |
| **Visitas registradas** | Visitantes con sus fechas de entrada y salida. |
| **Reservas de áreas comunes** | Reservas con su área, horario y estado. |
| **Ingresos mensuales** | Gráfico de barras con los pagos recibidos por mes. |

### 16.3 Generar un reporte

1. Selecciona <span class="mencion-ui">Reportes</span> en el menú lateral.
2. Elige el <span class="mencion-ui">Tipo de reporte</span>.
3. Elige la <span class="mencion-ui">Fecha inicial</span> del rango.
4. Elige la <span class="mencion-ui">Fecha final</span> del rango.
5. Elige el <span class="mencion-ui">Edificio o Torre</span> que quieres incluir.
6. Presiona el botón <span class="mencion-ui">Generar reporte</span>.
7. Revisa la <span class="mencion-ui">Vista previa</span> que aparece en pantalla.

<div class="caja caja-nota"><span class="caja-etiqueta">💡 CONSEJO:</span> Si no eliges fechas, el reporte de ingresos muestra los últimos 7 meses.</div>

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">Panel «Generar reporte» con el tipo de reporte, el rango de fechas y el botón Generar reporte</span></div>

**Vista previa según el tipo de reporte:**

- Los reportes de <span class="mencion-ui">Ingresos mensuales</span> muestran un gráfico de barras.
- Los demás reportes muestran una tabla con los datos.
- El selector <span class="mencion-ui">Seleccionar mes</span> permite ver el total de cada mes del gráfico.

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">Gráfico de barras de ingresos mensuales con el selector de mes</span></div>

### 16.4 Exportar un reporte

1. Configura el tipo de reporte y el rango de fechas.
2. Presiona el botón <span class="mencion-ui">Exportar CSV</span>.
3. El archivo se descarga a tu equipo.
4. Abre el archivo con tu hoja de cálculo favorita.

<div class="caja caja-nota"><span class="caja-etiqueta">💡 CONSEJO:</span> El archivo exportado lleva el nombre del reporte, por ejemplo `reporte-pagos_realizados.csv`.</div>

### 16.5 Lista lateral de reportes

El panel <span class="mencion-ui">Reportes disponibles</span> muestra todos los tipos de reporte. Presiona cualquiera para seleccionarlo rápidamente.

<div class="caja caja-advertencia"><span class="caja-etiqueta">⚠️ NOTA:</span> Cada reporte muestra hasta 200 registros. Para consultas más extensas, exporta a CSV.</div>

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">Panel lateral «Reportes disponibles» con la lista de tipos de reporte</span></div>

---

## 17. Configuración del Residencial

La pantalla <span class="mencion-ui">Residencial</span> (también disponible como <span class="mencion-ui">Configuración</span> en el menú de usuario) registra los datos generales del conjunto.

<div class="caja caja-advertencia"><span class="caja-etiqueta">⚠️ NOTA:</span> Solo el Administrador puede guardar cambios. Los demás usuarios ven la información en modo de solo lectura.</div>

<div class="caja caja-advertencia"><span class="caja-etiqueta">🔴 IMPORTANTE:</span> Esta es la primera pantalla que debe configurar el Administrador. Sin ella, los usuarios de administración son dirigidos a ella al iniciar sesión.</div>

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">Pantalla Residencial con las secciones de información general, dirección, estructura y contacto</span></div>

### 17.1 Completar la información general

1. Selecciona <span class="mencion-ui">Residencial</span> en el menú lateral.
2. Presiona el campo <span class="mencion-ui">Nombre del residencial</span>.
3. Escribe el nombre del conjunto.
4. Presiona el campo <span class="mencion-ui">RNC</span>.
5. Escribe el Registro Nacional de Contribuyentes, si aplica.
6. Presiona el botón <span class="mencion-ui">Agregar</span> o <span class="mencion-ui">Actualizar</span>.

### 17.2 Completar la dirección

1. Presiona el campo <span class="mencion-ui">Nombre de la vía</span>.
2. Escribe el nombre de la calle o avenida.
3. Presiona el campo <span class="mencion-ui">Número de la edificación</span>.
4. Escribe el número.
5. Presiona el campo <span class="mencion-ui">Sector</span>.
6. Escribe el sector.
7. Presiona el campo <span class="mencion-ui">Código Postal</span>.
8. Escribe el código postal.
9. Elige la <span class="mencion-ui">Provincia</span>.
10. Elige el <span class="mencion-ui">Municipio/Ciudad</span>.
11. Pega el <span class="mencion-ui">iframe de Google Map</span> en el campo indicado.
12. Revisa la vista previa del mapa.
13. Presiona el botón <span class="mencion-ui">Agregar</span> o <span class="mencion-ui">Actualizar</span>.

<div class="caja caja-nota"><span class="caja-etiqueta">💡 CONSEJO:</span> Los municipios disponibles se ajustan automáticamente al elegir la provincia.</div>

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">Sección «Dirección» del formulario del residencial con el selector de provincia y el mapa</span></div>

### 17.3 Completar la estructura

1. Elige la <span class="mencion-ui">Distribución</span> del residencial: *Torres* o *Edificios*.
2. Escribe la <span class="mencion-ui">Cantidad de edificios/torres</span>.
3. Escribe la <span class="mencion-ui">Cantidad de pisos por edificio/torre</span>.
4. Presiona el botón <span class="mencion-ui">Agregar</span> o <span class="mencion-ui">Actualizar</span>.

<div class="caja caja-advertencia"><span class="caja-etiqueta">🔴 IMPORTANTE:</span> La distribución se elige <strong>una sola vez</strong>. Una vez guardada, el campo queda bloqueado y no se puede cambiar.</div>

<div class="caja caja-nota"><span class="caja-etiqueta">💡 CONSEJO:</span> La distribución elegida determina si el resto del sistema habla de <em>Torres</em> o de <em>Edificios</em>.</div>

### 17.4 Completar los datos de contacto

1. Presiona el campo <span class="mencion-ui">Teléfono de administración</span>.
2. Escribe el número de contacto.
3. Presiona el campo <span class="mencion-ui">Correo de administración</span>.
4. Escribe el correo institucional.
5. Presiona el botón <span class="mencion-ui">Agregar</span> o <span class="mencion-ui">Actualizar</span>.

---

## 18. Preguntas Frecuentes y Resolución de Problemas

### 18.1 Preguntas Frecuentes

**1. ¿Por qué no me aparece un módulo en el menú?**

El sistema muestra únicamente los módulos permitidos para tu tipo de usuario. Si necesitas acceso a un módulo que no aparece, solicita un cambio de permisos al Administrador.

---

**2. ¿Por qué el botón Agregar no aparece?**

Solo los Administradores y los Encargados de Administración tienen permisos de creación en la mayoría de los módulos. En Incidencias y Reservas, los residentes y propietarios también pueden crear registros.

---

**3. ¿Por qué el botón Eliminar no aparece?**

La eliminación está reservada al Administrador y al Encargado de Administración. En el módulo Residencial, únicamente el Administrador puede eliminar registros.

---

**4. ¿Por qué no me puedo iniciar sesión?**

Verifica que estés escribiendo tu <span class="mencion-ui">correo electrónico</span> y no tu nombre de usuario. También confirma que tu cuenta esté en estado <span class="mencion-ui">Activo</span> y que tu contraseña sea correcta.

---

**5. ¿Cómo recupero mi contraseña?**

El enlace <span class="mencion-ui">¿Se te ha olvidado la clave?</span> del formulario de acceso no genera contraseñas automáticamente. Solicita al Administrador que restablezca tu contraseña.

---

**6. ¿Por qué el sistema me lleva a Configuración al entrar?**

Porque el residencial todavía no tiene información registrada. El Administrador o el Encargado de Administración debe completar la pantalla <span class="mencion-ui">Residencial</span> una vez.

---

**7. ¿Por qué el personal de seguridad entra directo a Visitantes?**

Por diseño. Las cuentas de Seguridad / Portería están orientadas al control de accesos, por lo que el sistema abre ese módulo directamente.

---

**8. ¿Por qué no aparece mi área común en el formulario de reservas?**

Solo se muestran las áreas en estado <span class="mencion-ui">Activo</span>. Verifica el estado del área en el módulo Áreas Comunes.

---

**9. ¿Por qué no puedo guardar una reserva en ese horario?**

El sistema valida tres reglas: la hora de fin debe ser posterior a la de inicio, la reserva debe caer dentro del horario del área y la fecha debe coincidir con los días habilitados.

---

**10. ¿Por qué no puedo elegir una persona en el formulario?**

El desplegable de personas se habilita después de elegir el campo <span class="mencion-ui">Quien paga</span> (en Pagos). En Incidencias y Solicitudes, el desplegable se habilita después de elegir el departamento.

---

**11. ¿Por qué el sistema dice que la persona no pertenece al departamento?**

Cada registro debe vincular a una persona con su departamento. Cambia el departamento o elige una persona que corresponda a la unidad seleccionada.

---

**12. ¿Por qué no puedo cambiar la distribución del residencial?**

La distribución se define una sola vez porque afecta a toda la estructura del sistema. Una vez guardada, el campo queda bloqueado.

---

**13. ¿Por qué se eliminó una cuenta de usuario al registrar a una persona?**

Cada registro de propietario o residente genera su cuenta de acceso con el correo y la contraseña que indiques. Si el correo ya estaba en uso, el sistema rechaza el registro.

---

**14. ¿Dónde veo el historial de una incidencia?**

La columna <span class="mencion-ui">Comentarios/Actualizaciones</span> muestra el último seguimiento registrado. Cada vez que la administración cambia el estado y escribe un comentario, ese movimiento queda guardado con su fecha y responsable.

---

**15. ¿Cómo obtengo un comprobante de pago?**

Abre el pago que quieres facturar desde el ícono del <span class="mencion-ui">lápiz</span> y presiona el botón <span class="mencion-ui">Generar comprobante</span> del encabezado. El botón se habilita cuando los campos obligatorios están completos.

---

### 18.2 Resolución de Problemas

**Problema: aparece el mensaje «El email o la contraseña no son válidos»**

1. Verifica que el correo esté escrito correctamente.
2. Verifica que no haya espacios al inicio o al final.
3. Confirma que la cuenta esté en estado <span class="mencion-ui">Activo</span>.
4. Solicita al Administrador que restablezca tu contraseña si el problema persiste.

---

**Problema: la tabla muestra «Sin coincidencias»**

1. Revisa los filtros activos en la barra superior.
2. Cambia los filtros a la opción <span class="mencion-ui">Todos...</span>.
3. Avanza a la siguiente página de resultados, si aplica.

---

**Problema: el sistema no me deja subir una imagen**

1. Verifica que el archivo sea JPG, PNG o WEBP.
2. Verifica que el archivo pese menos de 2 MB.
3. Verifica que el formato esté permitido en ese campo. Las evidencias de incidencias y los adjuntos de solicitudes también aceptan PDF.

---

**Problema: el sistema dice «La hora de fin debe ser posterior a la hora de inicio»**

1. Revisa la <span class="mencion-ui">Hora de inicio</span> del formulario.
2. Corrige la <span class="mencion-ui">Hora de fin</span> con un valor más tarde.
3. Vuelve a guardar el registro.

---

**Problema: el sistema dice «Fuera del horario del área»**

1. Revisa el horario permitido del área en el módulo Áreas Comunes.
2. Ajusta la <span class="mencion-ui">Hora de inicio</span> y la <span class="mencion-ui">Hora de fin</span> dentro de ese rango.

---

**Problema: el sistema dice «Esa área solo está disponible...»**

1. Cambia la <span class="mencion-ui">Fecha de reserva</span> por un día permitido.
2. Si necesitas otro día, pide a la administración que modifique los <span class="mencion-ui">Días habilitados</span> del área.

---

**Problema: el botón Generar comprobante aparece deshabilitado**

1. Completa el campo <span class="mencion-ui">Departamento</span>.
2. Completa el campo de la persona que paga.
3. Completa el campo <span class="mencion-ui">Monto</span>.
4. Completa el campo <span class="mencion-ui">Concepto</span>.
5. Completa el campo <span class="mencion-ui">Período/Mes correspondiente</span>.
6. Completa el campo <span class="mencion-ui">Estado</span>.

---

**Problema: el enlace Ver todo de Actividad Reciente no abre una pantalla propia**

Se trata de una funcionalidad en construcción. Por ahora, toda la actividad reciente se muestra directamente en el panel de inicio.

---

**Problema: aparece el mensaje «No tienes permisos para acceder a este módulo»**

Tu tipo de usuario no tiene acceso a esa sección. Regresa al Inicio y utiliza los módulos que te aparecen en el menú lateral.

---

**Problema: aparece el mensaje «No se pudo crear el comunicado: no hay ningún jardín configurado»**

Debes registrar primero al menos un jardín con sus edificios desde el módulo <span class="mencion-ui">Departamentos</span>, antes de publicar comunicados.

---

### 18.3 Módulos no disponibles en la interfaz

Actualmente el sistema <span class="mencion-ui">no muestra</span> los módulos de <span class="mencion-ui">Chat</span> y <span class="mencion-ui">Notificaciones</span> en el menú lateral. Estas secciones se encuentran en fase de desarrollo y todavía no están habilitadas para los usuarios.

Si necesitas recibir avisos automáticos o communicate con la administración, utiliza por ahora el módulo <span class="mencion-ui">Comunicados</span> o registra una <span class="mencion-ui">Solicitud</span>.

---

### 18.4 Cuándo solicitar ayuda

Contacta a la administración del residencial cuando:

- No puedas iniciar sesión tras varios intentos.
- Necesites un cambio de permisos o de tipo de usuario.
- Necesites restablecer tu contraseña.
- Detectes un dato incorrecto que no puedes corregir por tu cuenta.
- Necesites información que los reportes no muestran.

---

*Fin del manual de usuario — CONDOSYS*