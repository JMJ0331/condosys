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

<h1>Manual de Usuario â€” <span class="marca">CONDOSYS</span></h1>

**Sistema de administraciÃ³n residencial CONDOSYS**

---

## Ãndice

1. [GuÃ­a de Inicio RÃ¡pido](#1-guÃ­a-de-inicio-rÃ¡pido)
2. [Conociendo el Sistema](#2-conociendo-el-sistema)
3. [Acceso, SesiÃ³n y Mi Perfil](#3-acceso-sesiÃ³n-y-mi-perfil)
4. [Panel de Inicio](#4-panel-de-inicio)
5. [Departamentos](#5-departamentos)
6. [Propietarios](#6-propietarios)
7. [Residentes](#7-residentes)
8. [Pagos](#8-pagos)
9. [Mantenimientos](#9-mantenimientos)
10. [Incidencias](#10-incidencias)
11. [Solicitudes](#11-solicitudes)
12. [Visitantes](#12-visitantes)
13. [Ãreas Comunes](#13-Ã¡reas-comunes)
14. [Reservas](#14-reservas)
15. [Comunicados](#15-comunicados)
16. [Reportes](#16-reportes)
17. [ConfiguraciÃ³n del Residencial](#17-configuraciÃ³n-del-residencial)
18. [ConfiguraciÃ³n](#18-configuraciÃ³n)
19. [Preguntas Frecuentes y ResoluciÃ³n de Problemas](#19-preguntas-frecuentes-y-resoluciÃ³n-de-problemas)

---

## 1. GuÃ­a de Inicio RÃ¡pido

Si es tu primera vez usando el sistema, completa estos pasos en orden.

### <span class="etiqueta-paso">Paso 1</span> â€” Inicia sesiÃ³n

1. Abre la direcciÃ³n del sistema en tu navegador.
2. Escribe tu <span class="mencion-ui">Email</span>.
3. Escribe tu <span class="mencion-ui">ContraseÃ±a</span>.
4. Presiona el botÃ³n <span class="mencion-ui">Acceder</span>.

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">Pantalla de acceso a CONDOSYS con los campos Email y ContraseÃ±a y el botÃ³n Acceder</span></div>

### <span class="etiqueta-paso">Paso 2</span> â€” Ubica el menÃº lateral

1. Mira el lado izquierdo de la pantalla.
2. Localiza el panel con el logotipo de <span class="mencion-ui">condosys</span>.
3. Explora los mÃ³dulos que aparecen debajo del logotipo.

<div class="caja caja-nota"><span class="caja-etiqueta">ðŸ’¡ CONSEJO:</span> Solo verÃ¡s los mÃ³dulos que corresponden a tu tipo de usuario. Es normal que no aparezcan todos.</div>

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">MenÃº lateral con los mÃ³dulos visibles para el usuario</span></div>

### <span class="etiqueta-paso">Paso 3</span> â€” Cambia tu contraseÃ±a la primera vez

1. Presiona tu nombre en la parte inferior del menÃº lateral.
2. Selecciona la opciÃ³n <span class="mencion-ui">Mi perfil</span>.
3. Revisa que tus datos de contacto estÃ©n correctos.
4. Para cambiar tu contraseÃ±a, cierra sesiÃ³n y usa el enlace <span class="mencion-ui">Â¿Se te ha olvidado la clave?</span> del formulario de acceso.

<div class="caja caja-advertencia"><span class="caja-etiqueta">âš ï¸ NOTA:</span> Tu contraseÃ±a inicial te la entrega el Administrador o el Encargado de AdministraciÃ³n. Si la olvidas, puedes restablecerla tÃº mismo desde el enlace del inicio de sesiÃ³n.</div>

### <span class="etiqueta-paso">Paso 4</span> â€” Registra tus datos en el sistema

1. DirÃ­gete al mÃ³dulo <span class="mencion-ui">Departamentos</span>.
2. Ubica el departamento que te corresponde.
3. Verifica que tu nombre figure como propietario.

<div class="caja caja-advertencia"><span class="caja-etiqueta">ðŸ”´ IMPORTANTE:</span> Sin departamentos registrados no podrÃ¡s asignar pagos, incidencias ni reservas.</div>

### <span class="etiqueta-paso">Paso 5</span> â€” Reporta tus novedades

1. Entra al mÃ³dulo <span class="mencion-ui">Incidencias</span>.
2. Presiona el botÃ³n <span class="mencion-ui">Agregar incidencia</span>.
3. Registra cualquier problema de plomerÃ­a, electricidad, limpieza, ruido, agua, seguridad u otro.

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">Formulario de reporte de incidencia con el tipo de incidencia y la descripciÃ³n</span></div>

### <span class="etiqueta-paso">Paso 6</span> â€” Consulta tus pagos

1. Entra al mÃ³dulo <span class="mencion-ui">Pagos</span>.
2. Revisa la columna <span class="mencion-ui">Estado</span>.
3. Identifica los registros marcados como <span class="mencion-ui">Pendiente</span>, <span class="mencion-ui">En riesgo</span> o <span class="mencion-ui">Vencido</span>.

<div class="caja caja-nota"><span class="caja-etiqueta">ðŸ’¡ CONSEJO:</span> El enlace <span class="mencion-ui">Ver todos los pagos pendientes</span> del panel de inicio abre el filtro ya aplicado.</div>

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">Tabla de pagos con los estados Pendiente, En riesgo y Vencido destacados</span></div>

### <span class="etiqueta-paso">Paso 7</span> â€” Reserva un Ã¡rea comÃºn

1. Entra al mÃ³dulo <span class="mencion-ui">Reservas</span>.
2. Presiona el botÃ³n <span class="mencion-ui">Agregar reserva</span>.
3. Elige el Ã¡rea comÃºn, la fecha y el horario.

<div class="caja caja-advertencia"><span class="caja-etiqueta">ðŸ”´ IMPORTANTE:</span> Tu reserva se crea en estado <span class="mencion-ui">Solicitada</span> y espera la aprobaciÃ³n de la administraciÃ³n.</div>

### <span class="etiqueta-paso">Paso 8</span> â€” Cierra sesiÃ³n al terminar

1. Presiona tu nombre en la parte inferior del menÃº lateral.
2. Selecciona la opciÃ³n <span class="mencion-ui">Cerrar sesiÃ³n</span>.

---

## 2. Conociendo el Sistema

### 2.1 Â¿QuÃ© es CONDOSYS?

CONDOSYS es un sistema de administraciÃ³n residencial. Permite centralizar en un solo lugar la informaciÃ³n de los departamentos, sus propietarios y residentes, los pagos, los cargos de mantenimiento, las incidencias, las solicitudes, los visitantes, las reservas de Ã¡reas comunes y los comunicados.

### 2.2 Estructura de la pantalla

Al iniciar sesiÃ³n, la pantalla se divide en cuatro zonas principales:

- <span class="mencion-ui">MenÃº lateral izquierdo:</span> contiene los mÃ³dulos disponibles para tu tipo de usuario.
- <span class="mencion-ui">Encabezado superior:</span> muestra el nombre del mÃ³dulo actual y ofrece los botones de acciÃ³n (Agregar, Actualizar, Cancelar o Volver).
- <span class="mencion-ui">Zona central:</span> muestra el contenido del mÃ³dulo, ya sea un formulario o una tabla de registros.
- <span class="mencion-ui">Bloque de usuario (inferior izquierda):</span> muestra tu foto, tu nombre y tu correo, y abre el menÃº personal.

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">Vista general del sistema con el menÃº lateral, el encabezado y la tabla central</span></div>

### 2.3 Tipos de usuario y permisos

El sistema adapta su contenido segÃºn el tipo de usuario con el que inicias sesiÃ³n.

| Tipo de usuario | QuÃ© puede hacer |
|---|---|
| **Administrador** | Acceso completo a todos los mÃ³dulos. Autoriza registros de usuarios, gestiona roles y permisos, configura el residencial y elimina informaciÃ³n de cualquier mÃ³dulo. |
| **Encargado de AdministraciÃ³n** | Registra cuotas, pagos y cargos. Consulta y filtra estados de pago y emite comprobantes. Actualiza datos de propietarios y residentes. Da seguimiento a incidencias. Realiza consultas generales. No autoriza usuarios ni administra la configuraciÃ³n del residencial. |
| **Seguridad / PorterÃ­a** | Registra y controla visitantes y accesos al residencial. No gestiona pagos, cuotas ni informaciÃ³n de residentes. No cambia estados de incidencias ni administra reservas. |
| **Residente** | Inicia y cierra sesiÃ³n. Consulta sus pagos, pagos pendientes y comprobantes. Reporta incidencias y da seguimiento. Consulta el historial de sus incidencias. |
| **Propietario** | Consulta sus pagos y comprobantes. Reporta incidencias y las da seguimiento. Reserva Ã¡reas comunes de sus propios departamentos. |

<div class="caja caja-advertencia"><span class="caja-etiqueta">âš ï¸ NOTA:</span> El tipo de usuario lo asigna el Administrador. Si necesitas un cambio de permisos, comunÃ­cate con la administraciÃ³n del residencial.</div>

### 2.4 MÃ³dulos disponibles

| MÃ³dulo | DescripciÃ³n | QuiÃ©n lo ve |
|---|---|---|
| **Inicio** | Panel con resÃºmenes, pagos por vencer y actividad reciente. | Todos |
| **Departamentos** | Registro y estado de cada unidad del residencial. | Todos |
| **Propietarios** | Datos de los propietarios de los departamentos. | AdministraciÃ³n |
| **Residentes** | Datos de las personas que habitan los departamentos. | AdministraciÃ³n y propietarios |
| **Pagos** | Registro de cuotas y pagos realizados. | Todos |
| **Mantenimientos** | Cargos recurrentes y su vigencia. | Todos |
| **Incidencias** | Reportes de problemas y su seguimiento. | Todos |
| **Solicitudes** | TrÃ¡mites y pedidos especiales de los residentes. | AdministraciÃ³n |
| **Visitantes** | Control de entrada y salida de visitantes. | Seguridad y administraciÃ³n |
| **Ãreas Comunes** | CatÃ¡logo de Ã¡reas con su horario y reglas. | Todos |
| **Reservas** | Solicitudes de uso de Ã¡reas comunes. | Todos |
| **Comunicados** | Avisos y anuncios de la administraciÃ³n. | Todos |
| **Reportes** | EstadÃ­sticas y exportaciones de informaciÃ³n. | AdministraciÃ³n |
| **Residencial** | ConfiguraciÃ³n general del residencial. | Administrador |
| **ConfiguraciÃ³n** | GestiÃ³n de usuarios e integraciÃ³n con inteligencia artificial. Se abre desde el menÃº de usuario. | Administrador |

### 2.5 Elementos que se repiten en el sistema

- <span class="mencion-ui">BotÃ³n Agregar:</span> crea un registro nuevo.
- <span class="mencion-ui">BotÃ³n Actualizar:</span> guarda los cambios de un registro existente.
- <span class="mencion-ui">BotÃ³n Cancelar:</span> abandona el formulario sin guardar.
- <span class="mencion-ui">Flecha de volver:</span> regresa al listado del mÃ³dulo.
- <span class="mencion-ui">BotÃ³n Todas las columnas:</span> muestra u oculta columnas de la tabla.
- <span class="mencion-ui">Filtros:</span> permiten decidir quÃ© registros se muestran en la tabla.

<div class="caja caja-advertencia"><span class="caja-etiqueta">âš ï¸ NOTA:</span> Cuando un filtro no arroja resultados, la tabla muestra el mensaje <span class="mencion-ui">Sin coincidencias</span>.</div>

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">Encabezado de un mÃ³dulo con el botÃ³n Agregar y la flecha de volver</span></div>

### 2.6 Botones de acciones por fila

En la columna <span class="mencion-ui">Acciones</span> de cada tabla aparecen dos Ã­conos:

- <span class="mencion-ui">LÃ¡piz (Editar):</span> abre el registro para modificarlo.
- <span class="mencion-ui">Papelera (Eliminar):</span> abre una ventana de confirmaciÃ³n antes de borrar.

<div class="caja caja-advertencia"><span class="caja-etiqueta">âš ï¸ NOTA:</span> Los botones <span class="mencion-ui">Editar</span> y <span class="mencion-ui">Eliminar</span> solo aparecen si tu tipo de usuario tiene permiso para esa acciÃ³n.</div>

---

## 3. Acceso, SesiÃ³n y Mi Perfil

### 3.1 Pantalla de inicio de sesiÃ³n

Al entrar al sistema verÃ¡s una pantalla dividida en dos partes: a la izquierda, el logotipo de CONDOSYS; a la derecha, el formulario de acceso.

1. Presiona el campo <span class="mencion-ui">Email</span>.
2. Escribe tu correo electrÃ³nico.
3. Presiona el campo <span class="mencion-ui">ContraseÃ±a</span>.
4. Escribe tu contraseÃ±a.
5. Presiona el botÃ³n <span class="mencion-ui">Acceder</span>.

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">Formulario de inicio de sesiÃ³n de CONDOSYS</span></div>

### 3.2 Iniciar sesiÃ³n

1. Escribe tu <span class="mencion-ui">Email</span>.
2. Escribe tu <span class="mencion-ui">ContraseÃ±a</span>.
3. Presiona <span class="mencion-ui">Acceder</span>.

**Â¿A dÃ³nde llegas despuÃ©s de entrar?**

- Si eres <span class="mencion-ui">Administrador</span> o <span class="mencion-ui">Encargado de AdministraciÃ³n</span> y el residencial todavÃ­a no estÃ¡ configurado, irÃ¡s directo a la pantalla de configuraciÃ³n.
- Si eres de <span class="mencion-ui">Seguridad / PorterÃ­a</span>, irÃ¡s directo a <span class="mencion-ui">Visitantes</span>.
- En cualquier otro caso, irÃ¡s al <span class="mencion-ui">Inicio</span>.

<div class="caja caja-advertencia"><span class="caja-etiqueta">âš ï¸ NOTA:</span> Solo pueden entrar las cuentas que estÃ©n <span class="mencion-ui">Activas</span>. Las cuentas en estado <em>En verificaciÃ³n</em> o <em>Inactivo</em> son rechazadas.</div>

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">Mensaje de error Â«El email o la contraseÃ±a no son vÃ¡lidos.Â»</span></div>

### 3.3 Cerrar sesiÃ³n

1. Presiona el bloque con tu nombre en la parte inferior del menÃº lateral.
2. Selecciona la opciÃ³n <span class="mencion-ui">Cerrar sesiÃ³n</span>.

<div class="caja caja-advertencia"><span class="caja-etiqueta">ðŸ”´ IMPORTANTE:</span> Cierra sesiÃ³n siempre que termines de trabajar, especialmente en equipos compartidos.</div>

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">MenÃº de usuario desplegado con la opciÃ³n Cerrar sesiÃ³n</span></div>

### 3.4 Mi perfil

Accede desde el menÃº de usuario con la opciÃ³n <span class="mencion-ui">Mi perfil</span>.

El formulario contiene los siguientes campos:

| Campo | DescripciÃ³n |
|---|---|
| **Nombre completo** | Obligatorio. Se separa en nombre y apellido. |
| **Cedula** | Opcional. No se puede repetir entre cuentas. |
| **TelÃ©fono** | Opcional. |
| **Correo electrÃ³nico** | Obligatorio. Es tu usuario de acceso, por lo que no puede estar repetido. |
| **Fecha de ingreso** | Solo lectura. Muestra la fecha de creaciÃ³n de tu cuenta. |
| **Adjuntar imagen** | Foto de perfil. Formatos JPG, PNG o WEBP, con un mÃ¡ximo de 2 MB. |

**Para actualizar tu informaciÃ³n:**

1. Modifica los campos que necesites.
2. Cierra y vuelve a abrir el selector de imagen si quieres cambiar tu foto.
3. Presiona el botÃ³n <span class="mencion-ui">Actualizar</span> en el encabezado.

<div class="caja caja-advertencia"><span class="caja-etiqueta">âš ï¸ NOTA:</span> El tipo de usuario y el estado de tu cuenta <strong>no</strong> se modifican desde <em>Mi perfil</em>. Los gestiona la administraciÃ³n.</div>

<div class="caja caja-advertencia"><span class="caja-etiqueta">âš ï¸ NOTA:</span> Si cambias tu correo electrÃ³nico, usa el nuevo correo para iniciar sesiÃ³n la prÃ³xima vez.</div>

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">Pantalla Mi perfil con el formulario de datos personales y la zona de carga de imagen</span></div>

### 3.5 ConfiguraciÃ³n

La opciÃ³n <span class="mencion-ui">ConfiguraciÃ³n</span> del menÃº de usuario (solo visible para el Administrador) abre el mÃ³dulo <span class="mencion-ui">ConfiguraciÃ³n</span>, descrito en el capÃ­tulo 18. Desde ahÃ­ se gestionan los <span class="mencion-ui">Usuarios</span> y la <span class="mencion-ui">IntegraciÃ³n AI</span>.

<div class="caja caja-advertencia"><span class="caja-etiqueta">âš ï¸ NOTA:</span> La configuraciÃ³n general del residencial (direcciÃ³n, estructura y contacto) estÃ¡ en un mÃ³dulo aparte llamado <span class="mencion-ui">Residencial</span>, descrito en el capÃ­tulo 17.</div>

---

## 4. Panel de Inicio

El <span class="mencion-ui">Inicio</span> es la primera pantalla que ves despuÃ©s de iniciar sesiÃ³n. Presenta un resumen rÃ¡pido del estado del residencial.

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">Panel de Inicio con las cuatro tarjetas de resumen superiores</span></div>

### 4.1 Tarjetas de resumen

| Tarjeta | QuÃ© muestra |
|---|---|
| **Departamentos** | Cantidad total de departamentos activos. |
| **Incidencias abiertas** | Incidencias en estado Nueva, Asignada o En progreso. |
| **Pagos pendientes** | Pagos en estado Pendiente, En riesgo o Vencido. |
| **Reservas pendientes** | Reservas que esperan aprobaciÃ³n. |

### 4.2 Pagos pendientes por vencer

Esta tabla muestra los cinco pagos pendientes con la fecha de vencimiento mÃ¡s prÃ³xima.

| Columna | Contenido |
|---|---|
| **Departamento** | Unidad a la que corresponde el pago. |
| **Propietario/Residente** | Persona que realiza el pago. |
| **Monto** | Cantidad a pagar. |
| **Vence** | Fecha lÃ­mite del periodo. |
| **Estado** | SituaciÃ³n actual del pago. |

1. Ubica el enlace <span class="mencion-ui">Ver todos los pagos pendientes</span>.
2. Presiona el enlace para abrir el mÃ³dulo <span class="mencion-ui">Pagos</span> con el filtro de estado <span class="mencion-ui">Pendiente</span> aplicado.

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">Tabla Â«Pagos pendientes por vencerÂ» del panel de inicio</span></div>

### 4.3 Acciones rÃ¡pidas

El panel ofrece accesos directos a las tareas mÃ¡s frecuentes. Las acciones disponibles dependen de tu tipo de usuario.

| AcciÃ³n | Enlace |
|---|---|
| **Agregar pago** | Abre el formulario de nuevo pago. |
| **Agregar incidencia** | Abre el formulario de nueva incidencia. |
| **Agregar visitante** | Abre el formulario de nuevo visitante. |
| **Agregar comunicado** | Abre el formulario de nuevo comunicado. |
| **Reservas pendientes** | Muestra cuÃ¡ntas reservas esperan aprobaciÃ³n y enlaza al listado filtrado. |

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">Panel Â«Acciones RÃ¡pidasÂ» del inicio</span></div>

### 4.4 Actividad reciente

La lista <span class="mencion-ui">Actividad Reciente</span> muestra los Ãºltimos movimientos registrados: nuevos pagos y nuevas incidencias, con el tiempo transcurrido desde su creaciÃ³n.

<div class="caja caja-nota"><span class="caja-etiqueta">ðŸ’¡ CONSEJO:</span> El enlace <span class="mencion-ui">Ver todo</span> estÃ¡ en la parte superior de la lista.</div>

<div class="caja caja-advertencia"><span class="caja-etiqueta">âš ï¸ NOTA:</span> Actualmente el enlace <span class="mencion-ui">Ver todo</span> no lleva a una pantalla propia; muestra toda la actividad en el propio panel de inicio.</div>

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">Lista Â«Actividad RecienteÂ» con pagos e incidencias recientes</span></div>

---

## 5. Departamentos

El mÃ³dulo <span class="mencion-ui">Departamentos</span> gestiona las unidades del residencial y su estado de ocupaciÃ³n.

<div class="caja caja-advertencia"><span class="caja-etiqueta">âš ï¸ NOTA:</span> Los datos de compelr esta estructura son la base de todo el sistema. Si un departamento no existe, no se le pueden asignar pagos, incidencias ni visitantes.</div>

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">Tabla del mÃ³dulo Departamentos</span></div>

### 5.1 Ver los departamentos

1. Selecciona <span class="mencion-ui">Departamentos</span> en el menÃº lateral.
2. Localiza la tabla de departamentos.

**Columnas disponibles:**

| Columna | Contenido |
|---|---|
| **Miniatura** | FotografÃ­a del departamento. |
| **Departamento** | Nombre o nÃºmero de la unidad. |
| **Edificio / Torre** | Edificio o torre al que pertenece. |
| **Bloque** | Bloque dentro del edificio. |
| **Piso** | Piso en el que se encuentra. |
| **Jardin** | JardÃ­n o conjunto del residencial. |
| **Propietario** | Persona propietaria del departamento. |
| <span class="badge badge-exito">Ocupado</span> | Estado actual de la unidad. |

**Estados posibles de un departamento:**

- <span class="mencion-ui">VacÃ­o</span>
- <span class="mencion-ui">Ocupado</span>
- <span class="mencion-ui">En reparaciÃ³n</span>
- <span class="mencion-ui">Bloqueado</span>

<div class="caja caja-nota"><span class="caja-etiqueta">ðŸ’¡ CONSEJO:</span> SegÃºn cÃ³mo estÃ© configurado el residencial, la tabla muestra <em>Edificios</em> o <em>Torres</em>, y se ajusta de forma automÃ¡tica.</div>

### 5.2 Filtrar los departamentos

La barra de filtros permite tres cosas:

1. Elige un <span class="mencion-ui">JardÃ­n</span> para ver solo sus departamentos.
2. Elige un <span class="mencion-ui">Edificio o Torre</span> para ver solo sus departamentos.
3. Elige un <span class="mencion-ui">Estado</span> para ver solo las unidades en esa situaciÃ³n.

Para quitar un filtro, selecciona la opciÃ³n <span class="mencion-ui">Todos...</span> correspondiente.

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">Barra de filtros de Departamentos con los selectores JardÃ­n, Edificio y Estado</span></div>

### 5.3 Agregar un departamento

Solo disponible para Administradores y Encargados de AdministraciÃ³n.

1. Selecciona <span class="mencion-ui">Departamentos</span> en el menÃº lateral.
2. Presiona el botÃ³n <span class="mencion-ui">Agregar departamento</span>.
3. Completa el campo <span class="mencion-ui">Apartamento</span> con el nombre o nÃºmero de la unidad.
4. Elige el <span class="mencion-ui">Propietario</span> en la lista desplegable.
5. Sube una imagen del departamento, si la tienes.
6. Elige la <span class="mencion-ui">Torre</span> o el <span class="mencion-ui">Edificio</span> correspondiente.
7. Elige el <span class="mencion-ui">Bloque</span> correspondiente.
8. Escribe el <span class="mencion-ui">Piso</span>.<div class="caja caja-advertencia"><span class="caja-etiqueta">IMPORTANTE:</span> El número de piso no puede superar la cantidad máxima configurada para edificios/torres en la configuración del residencial. Si se ingresa un valor mayor, el sistema mostrará un error y no permitirá guardar.</div>
9. Activa o desactiva el interruptor <span class="mencion-ui">Ocupado</span>.
10. Presiona el botÃ³n <span class="mencion-ui">Agregar</span> en el encabezado.

**Formatos de imagen aceptados:** JPG, PNG o WEBP, con un mÃ¡ximo de 2 MB.

<div class="caja caja-nota"><span class="caja-etiqueta">ðŸ’¡ CONSEJO:</span> El interruptor <span class="mencion-ui">Ocupado</span> es la forma rÃ¡pida de cambiar el estado de la unidad sin abrir el selector de estados.</div>

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">Formulario Â«Agregar departamentoÂ» con las secciones InformaciÃ³n del departamento, UbicaciÃ³n y Estado</span></div>

### 5.4 Editar un departamento

1. Ubica la fila del departamento que quieres modificar.
2. Presiona el Ã­cono del <span class="mencion-ui">lÃ¡piz</span> en la columna <span class="mencion-ui">Acciones</span>.
3. Cambia los campos que necesites.
4. Presiona el botÃ³n <span class="mencion-ui">Actualizar</span> en el encabezado.

### 5.5 Eliminar un departamento

1. Ubica la fila del departamento que quieres eliminar.
2. Presiona el Ã­cono de la <span class="mencion-ui">papelera</span> en la columna <span class="mencion-ui">Acciones</span>.
3. Lee el mensaje de confirmaciÃ³n.
4. Presiona el botÃ³n <span class="mencion-ui">SÃ­, Eliminar</span> para confirmar.
5. Presiona el botÃ³n <span class="mencion-ui">Cancelar</span> para volver atrÃ¡s.

<div class="caja caja-advertencia"><span class="caja-etiqueta">ðŸ”´ IMPORTANTE:</span> Al eliminar un departamento se borran tambiÃ©n sus registros relacionados (pagos, incidencias, solicitudes y visitantes). Esta acciÃ³n no se puede deshacer.</div>

---

## 6. Propietarios

El mÃ³dulo <span class="mencion-ui">Propietarios</span> registra a los dueÃ±os de los departamentos. Cada propietario puede tener uno o varios departamentos a su nombre.

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">Tabla del mÃ³dulo Propietarios</span></div>

### 6.1 Ver los propietarios

1. Selecciona <span class="mencion-ui">Propietarios</span> en el menÃº lateral.
2. Localiza la tabla de propietarios.

**Columnas disponibles:**

| Columna | Contenido |
|---|---|
| **Foto** | FotografÃ­a del propietario. |
| **Nombre completo** | Nombre del propietario. |
| **CÃ©dula** | Documento de identidad. |
| **Estado civil** | Soltero/a, Casado/a, Divorciado/a, Viudo/a u Otro. |
| **TelÃ©fono** | NÃºmero de contacto. |
| **Correo** | Correo electrÃ³nico. |
| **Contacto de emergencia** | TelÃ©fono de la persona a contactar en una urgencia. |
| **Estado** | Activo o Inactivo. |

### 6.2 Filtrar los propietarios

1. Elige un <span class="mencion-ui">Estado</span> para ver solo propietarios activos o inactivos.
2. Elige un <span class="mencion-ui">Departamento</span> para ver solo los propietarios de esa unidad.

### 6.3 Agregar un propietario

Solo disponible para Administradores y Encargados de AdministraciÃ³n.

1. Selecciona <span class="mencion-ui">Propietarios</span> en el menÃº lateral.
2. Presiona el botÃ³n <span class="mencion-ui">Nuevo propietario</span>.
3. Completa la secciÃ³n <span class="mencion-ui">InformaciÃ³n del personal</span> con el nombre, el estado civil, la cÃ©dula y la foto de perfil.
4. Completa la secciÃ³n <span class="mencion-ui">InformaciÃ³n de contacto</span> con el telÃ©fono, el correo y el contacto de emergencia.
5. Escribe la <span class="mencion-ui">ContraseÃ±a</span> con la que la persona ingressarÃ¡ al sistema.
6. Repite la contraseÃ±a en <span class="mencion-ui">Confirmar contraseÃ±a</span>.
7. Activa o desactiva el interruptor <span class="mencion-ui">Activo</span>.
8. Presiona el botÃ³n <span class="mencion-ui">Agregar</span> en el encabezado.

**Requisitos de la contraseÃ±a:**

- Debe tener <span class="mencion-ui">mÃ­nimo 8 caracteres</span>.
- Debe coincidir con la confirmaciÃ³n.
- No puede ser demasiado comÃºn ni parecerse a los datos de la persona.

<div class="caja caja-advertencia"><span class="caja-etiqueta">ðŸ”´ IMPORTANTE:</span> La contraseÃ±a que escribas aquÃ­ es la Ãºnica forma en que el propietario podrÃ¡ entrar al sistema. EntrÃ©gasela de forma privada.</div>

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">Formulario Â«Agregar propietarioÂ» con las secciones de informaciÃ³n personal, de contacto, contraseÃ±a y estado</span></div>

### 6.4 Editar un propietario

1. Ubica la fila del propietario que quieres modificar.
2. Presiona el Ã­cono del <span class="mencion-ui">lÃ¡piz</span>.
3. Cambia los campos que necesites.
4. Presiona <span class="mencion-ui">Actualizar</span>.

<div class="caja caja-nota"><span class="caja-etiqueta">ðŸ’¡ CONSEJO:</span> Deja los campos de contraseÃ±a en blanco si no quieres cambiar la clave actual.</div>

### 6.5 Eliminar un propietario

1. Ubica la fila del propietario que quieres eliminar.
2. Presiona el Ã­cono de la <span class="mencion-ui">papelera</span>.
3. Presiona <span class="mencion-ui">SÃ­, Eliminar</span> para confirmar.

---

## 7. Residentes

El mÃ³dulo <span class="mencion-ui">Residentes</span> registra a las personas que habitan los departamentos, incluidos inquilinos, familiares y ocupantes.

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">Tabla del mÃ³dulo Residentes</span></div>

### 7.1 Ver los residentes

1. Selecciona <span class="mencion-ui">Residentes</span> en el menÃº lateral.
2. Localiza la tabla de residentes.

**Columnas disponibles:**

| Columna | Contenido |
|---|---|
| **Foto** | FotografÃ­a del residente. |
| **Nombre completo** | Nombre del residente. |
| **CÃ©dula** | Documento de identidad. |
| **Estado civil** | Soltero/a, Casado/a, Divorciado/a, Viudo/a u Otro. |
| **TelÃ©fono** | NÃºmero de contacto. |
| **Contacto de emergencia** | TelÃ©fono de la persona a contactar en una urgencia. |
| **Apartamento** | Departamento que ocupa. |
| **RelaciÃ³n** | Propietario, Inquilino, Familiar u Ocupante. |
| **Fecha de ingreso** | Fecha en que ingresÃ³ al residencial. |
| **Mascotas** | Indica si tiene mascotas. |
| **Estado** | Activo o Inactivo. |

### 7.2 Filtrar los residentes

1. Elige un <span class="mencion-ui">Estado</span> para ver solo residentes activos o inactivos.
2. Elige un <span class="mencion-ui">Departamento</span> para ver solo los residentes de esa unidad.

### 7.3 Agregar un residente

Solo disponible para Administradores y Encargados de AdministraciÃ³n.

1. Selecciona <span class="mencion-ui">Residentes</span> en el menÃº lateral.
2. Presiona el botÃ³n <span class="mencion-ui">Nuevo residente</span>.
3. Completa la secciÃ³n <span class="mencion-ui">InformaciÃ³n del personal</span> con el nombre, el estado civil, la cÃ©dula y la foto.
4. Completa la secciÃ³n <span class="mencion-ui">InformaciÃ³n de contacto</span> con el telÃ©fono, el correo y el contacto de emergencia.
5. Elige el <span class="mencion-ui">Departamento</span> que ocupa.
6. Elige el <span class="mencion-ui">Tipo de relaciÃ³n</span> que tiene con el departamento.
7. Escribe la <span class="mencion-ui">Fecha de ingreso</span>.
8. Indica si tiene <span class="mencion-ui">Mascotas</span>.
9. Escribe la <span class="mencion-ui">ContraseÃ±a</span> de acceso.
10. Repite la contraseÃ±a en <span class="mencion-ui">Confirmar contraseÃ±a</span>.
11. Activa o desactiva el interruptor <span class="mencion-ui">Activo</span>.
12. Presiona el botÃ³n <span class="mencion-ui">Agregar</span>.

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">Formulario Â«Agregar residenteÂ» con las secciones de informaciÃ³n del personal, de contacto, residencia, contraseÃ±a y estado</span></div>

### 7.4 Editar un residente

1. Ubica la fila del residente que quieres modificar.
2. Presiona el Ã­cono del <span class="mencion-ui">lÃ¡piz</span>.
3. Cambia los campos que necesites.
4. Presiona <span class="mencion-ui">Actualizar</span>.

### 7.5 Eliminar un residente

1. Ubica la fila del residente que quieres eliminar.
2. Presiona el Ã­cono de la <span class="mencion-ui">papelera</span>.
3. Presiona <span class="mencion-ui">SÃ­, Eliminar</span> para confirmar.

<div class="caja caja-nota"><span class="caja-etiqueta">ðŸ’¡ CONSEJO:</span> En lugar de eliminar a un residente que ya no vive en el residencial, desactiva el interruptor <span class="mencion-ui">Activo</span>. AsÃ­ conservas su historial.</div>

---

## 8. Pagos

El mÃ³dulo <span class="mencion-ui">Pagos</span> registra las cuotas de mantenimiento y los demÃ¡s cargos aplicados a los departamentos, asÃ­ como los pagos realizados.

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">Tabla del mÃ³dulo Pagos</span></div>

### 8.1 Conceptos de cobro

| Concepto | DescripciÃ³n |
|---|---|
| **Mantenimiento** | Cuota mensual de mantenimiento del residencial. |
| **Cuota extraordinaria** | Cobro adicional aprobado por la asamblea. |
| **Reserva** | Cargo por el uso de un Ã¡rea comÃºn. |
| **Parqueo** | Cargo por espacio de parqueo. |
| **Servicios** | Cobro de servicios. |
| **Otro** | Cualquier cargo no contemplado en las categorÃ­as anteriores. |

### 8.2 Estados de un pago

| Estado | Significado |
|---|---|
| <span class="badge badge-aviso">Pendiente</span> | El pago aÃºn no se ha realizado. |
| <span class="badge badge-aviso">En riesgo</span> | El pago estÃ¡ prÃ³ximo a vencer. |
| <span class="badge badge-error">Vencido</span> | El pago pasÃ³ su fecha lÃ­mite. |
| <span class="badge badge-exito">Pagado</span> | El pago fue recibido. |
| <span class="badge badge-error">Anulado</span> | El cobro fue cancelado. |

### 8.3 MÃ©todos de pago

Efectivo, Transferencia, Tarjeta, Cheque, Pago en lÃ­nea y Otro.

### 8.4 Ver los pagos

1. Selecciona <span class="mencion-ui">Pagos</span> en el menÃº lateral.
2. Localiza la tabla de pagos.

**Columnas disponibles:**

| Columna | Contenido |
|---|---|
| **Comprobante** | Imagen del recibo, si se adjuntÃ³. |
| **Departamento** | Unidad a la que corresponde el cobro. |
| **Propietario/Residente** | Persona que realiza el pago. |
| **Concepto** | Tipo de cobro. |
| **Monto** | Cantidad del cobro. |
| **Periodo/Mes correspondiente** | Mes al que corresponde el cobro. |
| **Fecha de pago** | DÃ­a en que se realizÃ³ el pago. |
| **Metodo de pago** | Forma en que se pagÃ³. |
| **Estado** | SituaciÃ³n del pago. |

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">Tabla de Pagos con el filtro de conceptos y el filtro de estados</span></div>

### 8.5 Filtrar los pagos

1. Elige un <span class="mencion-ui">Departamento</span> para ver solo sus cobros.
2. Elige un <span class="mencion-ui">Concepto</span> para ver solo un tipo de cobro.
3. Elige un <span class="mencion-ui">Estado</span> para ver solo los pagos en esa situaciÃ³n.

<div class="caja caja-nota"><span class="caja-etiqueta">ðŸ’¡ CONSEJO:</span> Combina varios filtros a la vez para un anÃ¡lisis mÃ¡s preciso.</div>

### 8.6 Registrar un pago

Solo disponible para Administradores y Encargados de AdministraciÃ³n.

1. Selecciona <span class="mencion-ui">Pagos</span> en el menÃº lateral.
2. Presiona el botÃ³n <span class="mencion-ui">Agregar pago</span>.
3. Elige el <span class="mencion-ui">Departamento</span> al que corresponde el cobro.
4. Elige <span class="mencion-ui">Quien paga</span>: *Un propietario* o *Un residente*.
5. Elige a la persona en el desplegable <span class="mencion-ui">Propietarios/Residentes</span>.
6. Escribe el <span class="mencion-ui">Monto</span> del pago.
7. Elige el <span class="mencion-ui">Concepto</span> del cobro.
8. Elige la fecha del <span class="mencion-ui">PerÃ­odo/Mes correspondiente</span>.
9. Elige la <span class="mencion-ui">Fecha del pago</span>.
10. Elige el <span class="mencion-ui">MÃ©todo de pago</span>.
11. Adjunta la <span class="mencion-ui">Foto del comprobante</span>, si la tienes.
12. Elige el <span class="mencion-ui">Estado</span> del pago.
13. Presiona el botÃ³n <span class="mencion-ui">Agregar</span>.

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">Formulario Â«Agregar pagoÂ» con los campos de departamento, quien paga, monto, concepto, periodo y estado</span></div>

**Comportamiento del desplegable de personas:**

1. Al elegir el <span class="mencion-ui">Departamento</span>, la lista de personas se filtra automÃ¡ticamente.
2. Al elegir <span class="mencion-ui">Quien paga</span>, el campo cambia de nombre: *Propietarios* o *Residentes*.
3. El campo permanece deshabilitado hasta que selecciones *Quien paga*.

<div class="caja caja-advertencia"><span class="caja-etiqueta">âš ï¸ NOTA:</span> La persona elegida debe pertenecer al departamento seleccionado. Si no coincide, el sistema rechaza el registro.</div>

**Adjuntar el comprobante:**

1. Presiona la zona de imagen del comprobante.
2. Suelta el archivo o selecciÃ³nalo desde tu equipo.
3. Verifica la vista previa.
4. Confirma que el archivo sea JPG, PNG o WEBP y no supere los 2 MB.

### 8.7 Generar un comprobante de pago

Esta funciÃ³n estÃ¡ disponible en la pantalla de <span class="mencion-ui">Actualizar pago</span>.

1. Selecciona <span class="mencion-ui">Pagos</span> en el menÃº lateral.
2. Presiona el Ã­cono del <span class="mencion-ui">lÃ¡piz</span> en el pago que quieres facturar.
3. Completa los campos obligatorios del formulario.
4. Presiona el botÃ³n <span class="mencion-ui">Generar comprobante</span> del encabezado.
5. El comprobante se abre en una pestaÃ±a nueva.
6. Imprime o guarda el documento como PDF.

<div class="caja caja-advertencia"><span class="caja-etiqueta">âš ï¸ NOTA:</span> El botÃ³n <span class="mencion-ui">Generar comprobante</span> permanece deshabilitado hasta que completes los campos obligatorios: departamento, persona, monto, concepto, periodo y estado.</div>

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">BotÃ³n Â«Generar comprobanteÂ» del encabezado en la pantalla de actualizar pago</span></div>

### 8.8 Editar un pago

1. Ubica la fila del pago que quieres modificar.
2. Presiona el Ã­cono del <span class="mencion-ui">lÃ¡piz</span>.
3. Cambia los campos que necesites.
4. Presiona <span class="mencion-ui">Actualizar</span>.

### 8.9 Eliminar un pago

1. Ubica la fila del pago que quieres eliminar.
2. Presiona el Ã­cono de la <span class="mencion-ui">papelera</span>.
3. Presiona <span class="mencion-ui">SÃ­, Eliminar</span> para confirmar.

---

## 9. Mantenimientos

El mÃ³dulo <span class="mencion-ui">Mantenimientos</span> registra los cargos recurrentes del residencial y sus reglas de cobro.

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">Tabla del mÃ³dulo Mantenimientos</span></div>

### 9.1 Conceptos de mantenimiento

Mantenimiento, Seguridad, Limpieza, AdministraciÃ³n, Fondo de reserva, Agua, Electricidad y Otro.

### 9.2 Periodicidades disponibles

| Periodicidad | Frecuencia |
|---|---|
| **Mensual** | Cada mes. |
| **Trimestral** | Cada tres meses. |
| **Semestral** | Cada seis meses. |
| **Anual** | Una vez al aÃ±o. |

### 9.3 Ver los mantenimientos

1. Selecciona <span class="mencion-ui">Mantenimientos</span> en el menÃº lateral.
2. Localiza la tabla de cargos.

**Columnas disponibles:**

| Columna | Contenido |
|---|---|
| **Foto** | Imagen del cargo. |
| **Concepto** | Tipo de cargo. |
| **Monto** | Cantidad a cobrar. |
| **Periodicidad** | Frecuencia del cobro. |
| **Departamento** | Departamento al que aplica. |
| **Fecha de generaciÃ³n** | Fecha de vigencia del cargo. |
| **Estado** | Activo o Inactivo. |

### 9.4 Filtrar los mantenimientos

1. Elige un <span class="mencion-ui">Departamento</span> para ver solo sus cargos.
2. Elige un <span class="mencion-ui">Estado</span> para ver solo los cargos activos o inactivos.
3. Elige un <span class="mencion-ui">AÃ±o</span> para ver los cargos de un perÃ­odo especÃ­fico.

### 9.5 Agregar un mantenimiento

Solo disponible para Administradores y Encargados de AdministraciÃ³n.

1. Selecciona <span class="mencion-ui">Mantenimientos</span> en el menÃº lateral.
2. Presiona el botÃ³n <span class="mencion-ui">Agregar mantenimiento</span>.
3. Elige el <span class="mencion-ui">Concepto</span> del cargo.
4. Elige la <span class="mencion-ui">Periodicidad</span>.
5. Escribe el <span class="mencion-ui">Monto</span> a cobrar.
6. Elige el <span class="mencion-ui">Departamento</span>, si el cargo aplica solo a una unidad.
7. Elige la <span class="mencion-ui">Fecha de generaciÃ³n</span>.
8. Adjunta la <span class="mencion-ui">Foto del mantenimiento</span>, si la tienes.
9. Activa o desactiva el interruptor <span class="mencion-ui">Activo</span>.
10. Presiona el botÃ³n <span class="mencion-ui">Agregar</span>.

<div class="caja caja-nota"><span class="caja-etiqueta">ðŸ’¡ CONSEJO:</span> Si dejas el departamento en blanco, el cargo se aplica a todos los departamentos del residencial.</div>

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">Formulario Â«Agregar mantenimientoÂ» con concepto, periodicidad, monto, departamento y fecha de generaciÃ³n</span></div>

### 9.6 Editar un mantenimiento

1. Ubica la fila del cargo que quieres modificar.
2. Presiona el Ã­cono del <span class="mencion-ui">lÃ¡piz</span>.
3. Cambia los campos que necesites.
4. Presiona <span class="mencion-ui">Actualizar</span>.

### 9.7 Desactivar un mantenimiento

1. Ubica la fila del cargo que quieres dejar de aplicar.
2. Presiona el Ã­cono del <span class="mencion-ui">lÃ¡piz</span>.
3. Desactiva el interruptor <span class="mencion-ui">Activo</span>.
4. Presiona <span class="mencion-ui">Actualizar</span>.

<div class="caja caja-advertencia"><span class="caja-etiqueta">ðŸ”´ IMPORTANTE:</span> No se recomienda eliminar un cargo ya cobrado. DesactÃ­valo para conservar su historial.</div>

---

## 10. Incidencias

El mÃ³dulo <span class="mencion-ui">Incidencias</span> permite reportar y dar seguimiento a los problemas del residencial.

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">Tabla del mÃ³dulo Incidencias</span></div>

### 10.1 Tipos de incidencia

| Tipo | DescripciÃ³n |
|---|---|
| **PlomerÃ­a** | Fugas, llaves, desagÃ¼es y obstrucciones. |
| **Electricidad** | Interruptores, bombillos, tomacorrientes y cables. |
| **Estructural** | Grietas, paredes, techos y pisos. |
| **Limpieza** | Basura, espacios sin limpiar y Ã¡reas comunes. |
| **Seguridad** | Puertas, cerraduras, cÃ¡maras y accesos. |
| **Ruido** | Ruidos molestos de vecinos o actividades. |
| **Agua** | Suministro, cortes de agua y fugas. |
| **Otro** | Cualquier problema no contemplado arriba. |

### 10.2 Niveles de prioridad

| Prioridad | Significado |
|---|---|
| **Baja** | Puede resolverse sin urgencia. |
| **Normal** | Debe atenderse en el orden habitual. |
| **Alta** | Afecta el bienestar de varios residentes. |
| **Urgente** | Requiere atenciÃ³n inmediata. |

### 10.3 Estados de una incidencia

El recorrido normal de una incidencia es: <span class="mencion-ui">Nueva â†’ Asignada â†’ En progreso â†’ Resuelta â†’ Cerrada</span>.

TambiÃ©n puede pasar a <span class="mencion-ui">Rechazada</span>.

### 10.4 Reportar una incidencia

1. Selecciona <span class="mencion-ui">Incidencias</span> en el menÃº lateral.
2. Presiona el botÃ³n <span class="mencion-ui">Agregar incidencia</span>.
3. Elige el <span class="mencion-ui">Departamento</span> donde ocurre el problema.
4. Elige al <span class="mencion-ui">Residente</span> que reporta.
5. Elige el <span class="mencion-ui">Tipo de incidencia</span>.
6. Elige la <span class="mencion-ui">Prioridad</span>.
7. Escribe la <span class="mencion-ui">DescripciÃ³n</span> del problema.
8. Elige la <span class="mencion-ui">Fecha del reporte</span>.
9. Adjunta la <span class="mencion-ui">Evidencia</span>, si la tienes.
10. Escribe el comentario inicial, si corresponde.
11. Presiona el botÃ³n <span class="mencion-ui">Agregar</span>.

**Formatos de evidencia aceptados:** JPG, PNG, WEBP o PDF, con un mÃ¡ximo de 2 MB.

<div class="caja caja-nota"><span class="caja-etiqueta">ðŸ’¡ CONSEJO:</span> Cuanto mÃ¡s especÃ­fico sea el texto de la descripciÃ³n, mÃ¡s rÃ¡pido podrÃ¡ resolverlo la administraciÃ³n.</div>

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">Formulario Â«Agregar incidenciaÂ» con el tipo de incidencia, la prioridad y la descripciÃ³n</span></div>

<div class="caja caja-advertencia"><span class="caja-etiqueta">âš ï¸ NOTA:</span> Si eres residente o propietario, el campo <span class="mencion-ui">Estado</span> no aparece en el formulario. La administraciÃ³n controla el avance de la incidencia.</div>

### 10.5 Consultar las incidencias

1. Selecciona <span class="mencion-ui">Incidencias</span> en el menÃº lateral.
2. Localiza la tabla de incidencias.

**Columnas disponibles:**

| Columna | Contenido |
|---|---|
| **Evidencia** | Imagen o archivo adjunto. |
| **Departamento** | Unidad donde ocurre el problema. |
| **Residente** | Persona que reporta. |
| **Tipo de incidencia** | CategorÃ­a del problema. |
| **Prioridad** | Nivel de urgencia. |
| **Fecha de reporte** | DÃ­a en que se reportÃ³. |
| **DescripciÃ³n** | Detalle del problema. |
| **Comentarios/Actualizaciones** | Ãšltimo seguimiento registrado. |
| **Estado** | SituaciÃ³n actual. |

### 10.6 Filtrar las incidencias

1. Elige un <span class="mencion-ui">Estado</span> para ver solo incidencias en esa situaciÃ³n.
2. Elige un <span class="mencion-ui">Departamento</span> para ver solo sus incidencias.
3. Elige un <span class="mencion-ui">Residente</span> para ver solo las que reportÃ³ esa persona.

### 10.7 Dar seguimiento a una incidencia

Solo disponible para Administradores y Encargados de AdministraciÃ³n.

1. Ubica la fila de la incidencia que quieres actualizar.
2. Presiona el Ã­cono del <span class="mencion-ui">lÃ¡piz</span>.
3. Cambia el <span class="mencion-ui">Estado</span> segÃºn el avance del trabajo.
4. Escribe el comentario o actualizaciÃ³n en el campo <span class="mencion-ui">Comentarios/actualizaciones</span>.
5. Presiona el botÃ³n <span class="mencion-ui">Actualizar</span>.

Cada cambio de estado queda registrado en el historial de la incidencia junto con la fecha y el responsable.

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">Pantalla Â«Actualizar incidenciaÂ» con el selector de estado y el campo de comentarios</span></div>

### 10.8 Eliminar una incidencia

1. Ubica la fila de la incidencia que quieres eliminar.
2. Presiona el Ã­cono de la <span class="mencion-ui">papelera</span>.
3. Presiona <span class="mencion-ui">SÃ­, Eliminar</span> para confirmar.

---

## 11. Solicitudes

El mÃ³dulo <span class="mencion-ui">Solicitudes</span> gestiona trÃ¡mites y peticiones especiales de los residentes, como certificados, permisos y documentaciÃ³n.

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">Tabla del mÃ³dulo Solicitudes</span></div>

### 11.1 Tipos de solicitud

| Tipo | DescripciÃ³n |
|---|---|
| **Certificado** | Solicitud de un certificado de residencia u otro. |
| **Permiso** | Solicitud de autorizaciÃ³n para una actividad. |
| **Mantenimiento** | PeticiÃ³n de un trabajo de mantenimiento. |
| **InstalaciÃ³n** | PeticiÃ³n de instalaciÃ³n de equipos o servicios. |
| **ReparaciÃ³n** | PeticiÃ³n de una reparaciÃ³n. |
| **DocumentaciÃ³n** | TrÃ¡mite que requiere documentaciÃ³n. |
| **Otro** | Cualquier solicitud no contemplada arriba. |

### 11.2 Estados de una solicitud

Pendiente, En proceso, Aprobada, Rechazada y Completada.

### 11.3 Ver las solicitudes

1. Selecciona <span class="mencion-ui">Solicitudes</span> en el menÃº lateral.
2. Localiza la tabla de solicitudes.

**Columnas disponibles:**

| Columna | Contenido |
|---|---|
| **Evidencia** | Documento adjunto. |
| **Departamento** | Unidad que solicita. |
| **Residente** | Persona que solicita. |
| **Tipo de solicitud** | CategorÃ­a de la solicitud. |
| **DescripciÃ³n** | Detalle de lo solicitado. |
| **Fecha de solicitud** | DÃ­a en que se realizÃ³ el pedido. |
| **Comentarios/Respuesta** | Seguimiento de la administraciÃ³n. |
| **Estado** | SituaciÃ³n actual. |

### 11.4 Filtrar las solicitudes

1. Elige un <span class="mencion-ui">Estado</span> para ver solo las solicitudes en esa situaciÃ³n.
2. Elige un <span class="mencion-ui">Departamento</span> para ver solo sus solicitudes.
3. Elige un <span class="mencion-ui">Residente</span> para ver solo las suyas.

### 11.5 Crear una solicitud

Solo disponible para Administradores y Encargados de AdministraciÃ³n.

1. Selecciona <span class="mencion-ui">Solicitudes</span> en el menÃº lateral.
2. Presiona el botÃ³n <span class="mencion-ui">Agregar solicitud</span>.
3. Elige el <span class="mencion-ui">Apartamento</span> que realiza la solicitud.
4. Elige al <span class="mencion-ui">Residente</span> que la presenta.
5. Elige el <span class="mencion-ui">Tipo de solicitud</span>.
6. Escribe la <span class="mencion-ui">DescripciÃ³n</span> de lo que necesitas.
7. Elige la <span class="mencion-ui">Fecha de solicitud</span>.
8. Adjunta el <span class="mencion-ui">Documento</span> de respaldo, si lo tienes.
9. Presiona el botÃ³n <span class="mencion-ui">Agregar</span>.

**Formatos de documento aceptados:** JPG, PNG, WEBP o PDF, con un mÃ¡ximo de 2 MB.

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">Formulario Â«Agregar solicitudÂ» con el tipo de solicitud, la descripciÃ³n y el adjunto</span></div>

### 11.6 Responder una solicitud

Solo disponible para Administradores y Encargados de AdministraciÃ³n.

1. Ubica la fila de la solicitud que quieres atender.
2. Presiona el Ã­cono del <span class="mencion-ui">lÃ¡piz</span>.
3. Escribe la respuesta en el campo <span class="mencion-ui">Comentarios/respuesta</span>.
4. Cambia el <span class="mencion-ui">Estado</span> segÃºn el avance.
5. Presiona el botÃ³n <span class="mencion-ui">Actualizar</span>.

<div class="caja caja-nota"><span class="caja-etiqueta">ðŸ’¡ CONSEJO:</span> Escribe la respuesta de forma clara para que el residente sepa quÃ© debe hacer.</div>

### 11.7 Eliminar una solicitud

1. Ubica la fila de la solicitud que quieres eliminar.
2. Presiona el Ã­cono de la <span class="mencion-ui">papelera</span>.
3. Presiona <span class="mencion-ui">SÃ­, Eliminar</span> para confirmar.

---

## 12. Visitantes

El mÃ³dulo <span class="mencion-ui">Visitantes</span> controla la entrada y salida de las personas que visitan el residencial. EstÃ¡ dirigido al personal de seguridad y a la administraciÃ³n.

<div class="caja caja-advertencia"><span class="caja-etiqueta">ðŸ”´ IMPORTANTE:</span> El personal de seguridad inicia sesiÃ³n en este mÃ³dulo directamente, sin pasar por el panel de inicio.</div>

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">Tabla del mÃ³dulo Visitantes</span></div>

### 12.1 Tipos de visitante

| Tipo | DescripciÃ³n |
|---|---|
| **Familiar** | Parientes de los residentes. |
| **Delivery** | Entregas de paquetes o alimentos. |
| **TÃ©cnico** | TÃ©cnicos que realizan trabajos. |
| **Proveedor** | Proveedores de bienes o servicios. |
| **Otro** | Cualquier otro tipo de visitante. |

### 12.2 Estados de una visita

| Estado | Significado |
|---|---|
| <span class="badge badge-aviso">Esperando</span> | La visita fue registrada y aÃºn no se autoriza. |
| <span class="badge badge-exito">Autorizado</span> | La visita fue aprobada por la administraciÃ³n. |
| <span class="badge badge-error">Rechazado</span> | La visita fue denegada. |
| <span class="badge badge-exito">Completado</span> | El visitante ya registrÃ³ su salida. |
| <span class="badge badge-error">Cancelado</span> | La visita fue cancelada. |

### 12.3 Tipos de documento

CÃ©dula, Pasaporte, Licencia de conducir y Otro.

### 12.4 Ver las visitas

1. Selecciona <span class="mencion-ui">Visitantes</span> en el menÃº lateral.
2. Localiza la tabla de visitas.

**Columnas disponibles:**

| Columna | Contenido |
|---|---|
| **Nombre completo** | Nombre del visitante. |
| **Tipo de visitante** | CategorÃ­a de la visita. |
| **Tipo de documento** | Documento de identidad presentado. |
| **Documento** | NÃºmero del documento. |
| **Departamento a visitar** | Unidad a la que se dirige. |
| **Autorizado por** | Persona que aprobÃ³ el ingreso. |
| **Fecha de entrada** | Fecha y hora programada de entrada. |
| **Fecha de salida** | Fecha y hora programada de salida. |
| **Estado** | SituaciÃ³n actual de la visita. |

### 12.5 Filtrar las visitas

La barra de filtros permite acotar el listado con cinco criterios:

1. Elige un <span class="mencion-ui">Estado</span> de visita.
2. Elige un <span class="mencion-ui">Departamento</span>.
3. Elige un <span class="mencion-ui">Tipo de visitante</span>.
4. Elige un <span class="mencion-ui">Mes</span>.
5. Elige un <span class="mencion-ui">AÃ±o</span>.

<div class="caja caja-nota"><span class="caja-etiqueta">ðŸ’¡ CONSEJO:</span> El botÃ³n de mes muestra nombres abreviados (Ene, Feb, Marâ€¦) y el de aÃ±o solo incluye los aÃ±os con visitas programadas.</div>

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">Barra de filtros de Visitantes con los selectores de estado, departamento, tipo, mes y aÃ±o</span></div>

### 12.6 Registrar un visitante

1. Selecciona <span class="mencion-ui">Visitantes</span> en el menÃº lateral.
2. Presiona el botÃ³n <span class="mencion-ui">Agregar visitante</span>.
3. Completa la secciÃ³n <span class="mencion-ui">InformaciÃ³n del visitante</span> con el nombre, el tipo de visitante y el tipo de documento.
4. Elige el <span class="mencion-ui">Departamento a visitar</span>.
5. Elige quiÃ©n <span class="mencion-ui">AutorizÃ³</span> el ingreso.
6. Adjunta la <span class="mencion-ui">Foto del documento</span>, si la tienes.
7. Elige la <span class="mencion-ui">Fecha de entrada</span> programada.
8. Elige la <span class="mencion-ui">Fecha de salida</span>, si corresponde.
9. Elige el <span class="mencion-ui">Estado</span> de la visita.
10. Presiona el botÃ³n <span class="mencion-ui">Agregar</span>.

**Formatos de documento aceptados:** JPG, PNG o WEBP, con un mÃ¡ximo de 2 MB.

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">Formulario Â«Agregar visitanteÂ» con las secciones de informaciÃ³n del visitante, destino y autorizaciÃ³n, y registro de acceso</span></div>

<div class="caja caja-advertencia"><span class="caja-etiqueta">âš ï¸ NOTA:</span> Si la fecha de salida es anterior o igual a la fecha de entrada, el sistema rechaza el registro.</div>

### 12.7 Editar una visita

1. Ubica la fila de la visita que quieres modificar.
2. Presiona el Ã­cono del <span class="mencion-ui">lÃ¡piz</span>.
3. Cambia los campos que necesites.
4. Presiona <span class="mencion-ui">Actualizar</span>.

<div class="caja caja-nota"><span class="caja-etiqueta">ðŸ’¡ CONSEJO:</span> Cambia el <span class="mencion-ui">Estado</span> a <em>Autorizado</em> cuando el visitante sea aprobado para entrar.</div>

### 12.8 Eliminar una visita

1. Ubica la fila de la visita que quieres eliminar.
2. Presiona el Ã­cono de la <span class="mencion-ui">papelera</span>.
3. Presiona <span class="mencion-ui">SÃ­, Eliminar</span> para confirmar.

### 12.9 Buscar por cÃ©dula con inteligencia artificial

La tabla de visitas permite buscar por cÃ©dula leyendo el nÃºmero desde una foto, con la integraciÃ³n de inteligencia artificial configurada por el Administrador.

1. Presiona el botÃ³n <span class="mencion-ui">Buscar por cÃ©dula</span>.
2. En la ventana, presiona <span class="mencion-ui">Usar cÃ¡mara</span> para tomar la foto, o adjunta una imagen desde el archivo.
3. Si usas la cÃ¡mara, presiona <span class="mencion-ui">Capturar foto</span>.
4. Presiona el botÃ³n <span class="mencion-ui">Buscar</span>.

El sistema detecta la cÃ©dula, muestra un aviso con el nÃºmero y filtra la tabla por ese documento.

<div class="caja caja-advertencia"><span class="caja-etiqueta">ðŸ’¡ CONSEJO:</span> Mientras hay una bÃºsqueda activa, aparece un enlace <span class="mencion-ui">Limpiar</span> sobre la tabla para quitar el filtro.</div>

<div class="caja caja-advertencia"><span class="caja-etiqueta">âš ï¸ NOTA:</span> La imagen puede pesar hasta 8 MB. La cÃ¡mara requiere HTTPS o localhost y tu permiso. Si la IntegraciÃ³n AI no estÃ¡ configurada, esta funciÃ³n no podrÃ¡ leer la cÃ©dula desde la foto.</div>

---

## 13. Ãreas Comunes

El mÃ³dulo <span class="mencion-ui">Ãreas Comunes</span> define quÃ© zonas del residencial se pueden reservar, en quÃ© horario y bajo quÃ© condiciones.

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">Tabla del mÃ³dulo Ãreas Comunes</span></div>

### 13.1 Tipos de Ã¡rea

| Tipo | DescripciÃ³n |
|---|---|
| **Gazebo** | Zona de reuniones al aire libre. |
| **SalÃ³n de eventos** | Espacio para eventos. |
| **Ãrea social** | Espacio de encuentro. |
| **Piscina** | Ãrea de nataciÃ³n. |
| **Cancha deportiva** | Cancha para deportes. |
| **Gimnasio** | Espacio de ejercicio. |
| **Zona de parrillas** | Ãrea con parrillas. |
| **Otro** | Cualquier otra zona. |

### 13.2 DÃ­as habilitados

| OpciÃ³n | DÃ­as permitidos |
|---|---|
| **Todos los dÃ­as** | Cualquier dÃ­a de la semana. |
| **Lunes a Viernes** | De lunes a viernes. |
| **Fines de semana** | SÃ¡bado y domingo. |
| **Personalizado** | ConfiguraciÃ³n especial. |

### 13.3 Estados de un Ã¡rea

Activo, Inactivo y En mantenimiento.

### 13.4 Ver las Ã¡reas comunes

1. Selecciona <span class="mencion-ui">Ãreas Comunes</span> en el menÃº lateral.
2. Localiza la tabla de Ã¡reas.

**Columnas disponibles:**

| Columna | Contenido |
|---|---|
| **Nombre** | Nombre del Ã¡rea. |
| **Tipo de Ã¡rea** | CategorÃ­a del espacio. |
| **Capacidad** | NÃºmero de personas admitidas. |
| **Horario disponible** | Rango de horas en el que se puede usar. |
| **DÃ­as habilitados** | DÃ­as de la semana permitidos. |
| **Condiciones de uso** | Reglas que deben respetarse. |
| **Estado** | SituaciÃ³n actual del Ã¡rea. |

### 13.5 Filtrar las Ã¡reas comunes

1. Elige un <span class="mencion-ui">Tipo de Ã¡rea</span> para ver solo ese tipo de espacio.
2. Elige un <span class="mencion-ui">Estado</span> para ver solo las Ã¡reas activas, inactivas o en mantenimiento.

### 13.6 Agregar un Ã¡rea comÃºn

Solo disponible para Administradores y Encargados de AdministraciÃ³n.

1. Selecciona <span class="mencion-ui">Ãreas Comunes</span> en el menÃº lateral.
2. Presiona el botÃ³n <span class="mencion-ui">Agregar Ã¡rea comÃºn</span>.
3. Completa la secciÃ³n <span class="mencion-ui">InformaciÃ³n del Ã¡rea</span> con el nombre, el tipo y la capacidad.
4. Elige la hora <span class="mencion-ui">Disponible desde</span>.
5. Elige la hora <span class="mencion-ui">Disponible hasta</span>.
6. Elige los <span class="mencion-ui">DÃ­as habilitados</span>.
7. Escribe las <span class="mencion-ui">Condiciones de uso</span> (mÃ¡ximo 400 caracteres).
8. Elige el <span class="mencion-ui">Estado</span> del Ã¡rea.
9. Presiona el botÃ³n <span class="mencion-ui">Agregar</span>.

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">Formulario Â«Agregar Ã¡rea comÃºnÂ» con las secciones de informaciÃ³n del Ã¡rea, disponibilidad, reglas de uso y estado</span></div>

<div class="caja caja-advertencia"><span class="caja-etiqueta">âš ï¸ NOTA:</span> La hora de fin debe ser posterior a la hora de inicio. Un Ã¡rea en estado <em>Inactivo</em> no aparece en el formulario de reservas.</div>

### 13.7 Editar un Ã¡rea comÃºn

1. Ubica la fila del Ã¡rea que quieres modificar.
2. Presiona el Ã­cono del <span class="mencion-ui">lÃ¡piz</span>.
3. Cambia los campos que necesites.
4. Presiona <span class="mencion-ui">Actualizar</span>.

<div class="caja caja-nota"><span class="caja-etiqueta">ðŸ’¡ CONSEJO:</span> Para frenar temporalmente el uso de un Ã¡rea, cÃ¡mbiale el estado a <span class="mencion-ui">En mantenimiento</span>.</div>

### 13.8 Eliminar un Ã¡rea comÃºn

1. Ubica la fila del Ã¡rea que quieres eliminar.
2. Presiona el Ã­cono de la <span class="mencion-ui">papelera</span>.
3. Presiona <span class="mencion-ui">SÃ­, Eliminar</span> para confirmar.

---

## 14. Reservas

El mÃ³dulo <span class="mencion-ui">Reservas</span> gestiona las solicitudes de uso de las Ã¡reas comunes.

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">Tabla del mÃ³dulo Reservas</span></div>

### 14.1 Estados de una reserva

| Estado | Significado |
|---|---|
| <span class="badge badge-aviso">Solicitada</span> | La reserva fue enviada y espera revisiÃ³n. |
| <span class="badge badge-exito">Aprobada</span> | La administraciÃ³n autorizÃ³ la reserva. |
| <span class="badge badge-error">Rechazada</span> | La administraciÃ³n denegÃ³ la reserva. |
| <span class="badge badge-exito">Completada</span> | El uso del Ã¡rea ya ocurriÃ³. |
| <span class="badge badge-error">Cancelada</span> | La reserva fue cancelada. |

### 14.2 Ver las reservas

1. Selecciona <span class="mencion-ui">Reservas</span> en el menÃº lateral.
2. Localiza la tabla de reservas.

**Columnas disponibles:**

| Columna | Contenido |
|---|---|
| **Foto** | FotografÃ­a del propietario o residente. |
| **Propietario/Residente** | Persona que realiza la reserva. |
| **Ãrea comÃºn** | Espacio reservado. |
| **Departamento** | Unidad del solicitante. |
| **Fecha de reserva** | DÃ­a de uso. |
| **Hora de inicio** | Hora de comienzo. |
| **Hora de fin** | Hora de finalizaciÃ³n. |
| **Estado** | SituaciÃ³n de la reserva. |

### 14.3 Filtrar las reservas

1. Elige un <span class="mencion-ui">Departamento</span> para ver solo sus reservas.
2. Elige un <span class="mencion-ui">Estado</span> para ver solo las reservas en esa situaciÃ³n.

### 14.4 Crear una reserva

1. Selecciona <span class="mencion-ui">Reservas</span> en el menÃº lateral.
2. Presiona el botÃ³n <span class="mencion-ui">Agregar reserva</span>.
3. Elige el <span class="mencion-ui">Ãrea comÃºn</span>.
4. Lee el aviso con el horario y los dÃ­as permitidos de esa Ã¡rea.
5. Elige el <span class="mencion-ui">Apartamento</span> que realiza la reserva.
6. Elige <span class="mencion-ui">Quien reserva</span>.
7. Elige al <span class="mencion-ui">Propietario/Residente</span> asociado al departamento.
8. Elige la <span class="mencion-ui">Fecha de reserva</span>.
9. Elige la <span class="mencion-ui">Hora de inicio</span>.
10. Elige la <span class="mencion-ui">Hora de fin</span>.
11. Presiona el botÃ³n <span class="mencion-ui">Agregar</span>.

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">Formulario Â«Agregar reservaÂ» con el Ã¡rea comÃºn, el horario y las secciones de informaciÃ³n y horario</span></div>

**Validaciones del sistema:**

- La hora de fin debe ser <span class="mencion-ui">posterior</span> a la hora de inicio.
- La reserva debe caer <span class="mencion-ui">dentro del horario</span> del Ã¡rea seleccionada.
- La fecha debe coincidir con los <span class="mencion-ui">dÃ­as habilitados</span> del Ã¡rea.
- El propietario o residente debe <span class="mencion-ui">pertenecer</span> al departamento elegido.

<div class="caja caja-advertencia"><span class="caja-etiqueta">âš ï¸ NOTA:</span> Si eres residente o propietario, el campo <span class="mencion-ui">Estado</span> no aparece en el formulario. Tu reserva se crea en estado <em>Solicitada</em> y la administraciÃ³n decide si la aprueba.</div>

<div class="caja caja-advertencia"><span class="caja-etiqueta">âš ï¸ NOTA:</span> Solo se muestran las Ã¡reas que estÃ¡n en estado <span class="mencion-ui">Activo</span>.</div>

### 14.5 Aprobar o rechazar una reserva

Solo disponible para Administradores y Encargados de AdministraciÃ³n.

1. Ubica la fila de la reserva que quieres revisar.
2. Presiona el Ã­cono del <span class="mencion-ui">lÃ¡piz</span>.
3. Elige el <span class="mencion-ui">Estado</span>: *Aprobada*, *Rechazada*, *Completada* o *Cancelada*.
4. Presiona el botÃ³n <span class="mencion-ui">Actualizar</span>.

<div class="caja caja-nota"><span class="caja-etiqueta">ðŸ’¡ CONSEJO:</span> El panel de inicio muestra un acceso directo con el nÃºmero de reservas que esperan aprobaciÃ³n.</div>

### 14.6 Editar una reserva

1. Ubica la fila de la reserva que quieres modificar.
2. Presiona el Ã­cono del <span class="mencion-ui">lÃ¡piz</span>.
3. Cambia los campos que necesites.
4. Presiona <span class="mencion-ui">Actualizar</span>.

### 14.7 Eliminar una reserva

1. Ubica la fila de la reserva que quieres eliminar.
2. Presiona el Ã­cono de la <span class="mencion-ui">papelera</span>.
3. Presiona <span class="mencion-ui">SÃ­, Eliminar</span> para confirmar.

---

## 15. Comunicados

El mÃ³dulo <span class="mencion-ui">Comunicados</span> publica avisos y anuncios de la administraciÃ³n para toda la comunidad.

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">Tabla del mÃ³dulo Comunicados</span></div>

### 15.1 CategorÃ­as de comunicado

Aviso, Mantenimiento, Evento, Seguridad, Piscinas y General.

### 15.2 Destinatarios

| OpciÃ³n | DescripciÃ³n |
|---|---|
| **General** | Dirigido a toda la comunidad. |
| **Por edificio** | Dirigido a los residentes de un edificio especÃ­fico. |
| **Para residente** | Dirigido a un residente en particular. |

### 15.3 Estados de un comunicado

- <span class="mencion-ui">Publicado:</span> visible para todos los destinatarios.
- <span class="mencion-ui">Borrador:</span> en preparaciÃ³n, todavÃ­a no visible.

### 15.4 Ver los comunicados

1. Selecciona <span class="mencion-ui">Comunicados</span> en el menÃº lateral.
2. Localiza la tabla de comunicados.

**Columnas disponibles:**

| Columna | Contenido |
|---|---|
| **Archivo/Imagen** | Imagen adjunta al comunicado. |
| **TÃ­tulo** | Encabezado del aviso. |
| **CategorÃ­a** | Tipo de comunicado. |
| **Mensaje** | Contenido del aviso. |
| **Dirigido a** | Destinatarios del comunicado. |
| **Fecha de publicaciÃ³n** | DÃ­a en que se publicÃ³. |
| **Estado** | Publicado o Borrador. |

### 15.5 Filtrar los comunicados

1. Elige una <span class="mencion-ui">CategorÃ­a</span> para ver solo ese tipo de aviso.
2. Elige un <span class="mencion-ui">Estado</span> para ver solo los publicados o solo los borradores.

### 15.6 Publicar un comunicado

Solo disponible para Administradores y Encargados de AdministraciÃ³n.

1. Selecciona <span class="mencion-ui">Comunicados</span> en el menÃº lateral.
2. Presiona el botÃ³n <span class="mencion-ui">Agregar comunicado</span>.
3. Escribe el <span class="mencion-ui">TÃ­tulo</span> del aviso.
4. Elige la <span class="mencion-ui">CategorÃ­a</span>.
5. Escribe el <span class="mencion-ui">Mensaje</span> (mÃ¡ximo 400 caracteres).
6. Adjunta una <span class="mencion-ui">Imagen</span>, si la tienes.
7. Elige a quiÃ©n va <span class="mencion-ui">Dirigido</span>.
8. Elige la <span class="mencion-ui">Fecha de publicaciÃ³n</span>.
9. Elige el <span class="mencion-ui">Estado</span>: *Publicado* o *Borrador*.
10. Presiona el botÃ³n <span class="mencion-ui">Agregar</span>.

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">Formulario Â«Agregar comunicadoÂ» con el tÃ­tulo, la categorÃ­a, el mensaje y el estado</span></div>

<div class="caja caja-advertencia"><span class="caja-etiqueta">âš ï¸ NOTA:</span> El mensaje no puede superar los 400 caracteres. La imagen opcional debe ser JPG, PNG o WEBP y pesar menos de 2 MB.</div>

### 15.7 Editar un comunicado

1. Ubica la fila del comunicado que quieres modificar.
2. Presiona el Ã­cono del <span class="mencion-ui">lÃ¡piz</span>.
3. Cambia los campos que necesites.
4. Presiona <span class="mencion-ui">Actualizar</span>.

### 15.8 Eliminar un comunicado

1. Ubica la fila del comunicado que quieres eliminar.
2. Presiona el Ã­cono de la <span class="mencion-ui">papelera</span>.
3. Presiona <span class="mencion-ui">SÃ­, Eliminar</span> para confirmar.

---

## 16. Reportes

El mÃ³dulo <span class="mencion-ui">Reportes</span> consolida la informaciÃ³n del residencial y permite exportarla para su anÃ¡lisis.

<div class="caja caja-advertencia"><span class="caja-etiqueta">âš ï¸ NOTA:</span> Solo Administradores y Encargados de AdministraciÃ³n tienen acceso a este mÃ³dulo.</div>

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">Panel de Reportes con las cuatro tarjetas de indicadores</span></div>

### 16.1 Indicadores del sistema

En la parte superior se muestran cuatro tarjetas con el estado general del residencial:

| Indicador | QuÃ© mide |
|---|---|
| **Ingresos del mes** | Total de pagos recibidos en el mes en curso. |
| **Morosidad** | Suma de todos los pagos vencidos y en riesgo. |
| **OcupaciÃ³n** | Porcentaje de departamentos ocupados. |
| **Incidencias abiertas** | Incidencias en estado Nueva, Asignada o En progreso. |

### 16.2 Tipos de reporte disponibles

| Reporte | Contenido |
|---|---|
| **Apartamentos ocupados / disponibles** | Lista de departamentos con su estado. |
| **Residentes activos** | Solo los residentes marcados como activos. |
| **Pagos realizados** | Pagos en estado Pagado. |
| **Pagos pendientes** | Pagos en estado Pendiente. |
| **Morosidad** | Pagos en estado En riesgo o Vencido. |
| **Incidencias por estado** | Incidencias con su categorÃ­a, prioridad y estado. |
| **Visitas registradas** | Visitantes con sus fechas de entrada y salida. |
| **Reservas de Ã¡reas comunes** | Reservas con su Ã¡rea, horario y estado. |
| **Ingresos mensuales** | GrÃ¡fico de barras con los pagos recibidos por mes. |

### 16.3 Generar un reporte

1. Selecciona <span class="mencion-ui">Reportes</span> en el menÃº lateral.
2. Elige el <span class="mencion-ui">Tipo de reporte</span>.
3. Elige la <span class="mencion-ui">Fecha inicial</span> del rango.
4. Elige la <span class="mencion-ui">Fecha final</span> del rango.
5. Elige el <span class="mencion-ui">Edificio o Torre</span> que quieres incluir.
6. Presiona el botÃ³n <span class="mencion-ui">Generar reporte</span>.
7. Revisa la <span class="mencion-ui">Vista previa</span> que aparece en pantalla.

<div class="caja caja-nota"><span class="caja-etiqueta">ðŸ’¡ CONSEJO:</span> Si no eliges fechas, el reporte de ingresos muestra los Ãºltimos 7 meses.</div>

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">Panel Â«Generar reporteÂ» con el tipo de reporte, el rango de fechas y el botÃ³n Generar reporte</span></div>

**Vista previa segÃºn el tipo de reporte:**

- Los reportes de <span class="mencion-ui">Ingresos mensuales</span> muestran un grÃ¡fico de barras.
- Los demÃ¡s reportes muestran una tabla con los datos.
- El selector <span class="mencion-ui">Seleccionar mes</span> permite ver el total de cada mes del grÃ¡fico.

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">GrÃ¡fico de barras de ingresos mensuales con el selector de mes</span></div>

### 16.4 Exportar un reporte

1. Configura el tipo de reporte y el rango de fechas.
2. Presiona el botÃ³n <span class="mencion-ui">Exportar CSV</span>.
3. El archivo se descarga a tu equipo.
4. Abre el archivo con tu hoja de cÃ¡lculo favorita.

<div class="caja caja-nota"><span class="caja-etiqueta">ðŸ’¡ CONSEJO:</span> El archivo exportado lleva el nombre del reporte, por ejemplo `reporte-pagos_realizados.csv`.</div>

### 16.5 Lista lateral de reportes

El panel <span class="mencion-ui">Reportes disponibles</span> muestra todos los tipos de reporte. Presiona cualquiera para seleccionarlo rÃ¡pidamente.

<div class="caja caja-advertencia"><span class="caja-etiqueta">âš ï¸ NOTA:</span> Cada reporte muestra hasta 200 registros. Para consultas mÃ¡s extensas, exporta a CSV.</div>

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">Panel lateral Â«Reportes disponiblesÂ» con la lista de tipos de reporte</span></div>

---

## 17. ConfiguraciÃ³n del Residencial

La pantalla <span class="mencion-ui">Residencial</span> (tambiÃ©n disponible como <span class="mencion-ui">ConfiguraciÃ³n</span> en el menÃº de usuario) registra los datos generales del conjunto.

<div class="caja caja-advertencia"><span class="caja-etiqueta">âš ï¸ NOTA:</span> Solo el Administrador puede guardar cambios. Los demÃ¡s usuarios ven la informaciÃ³n en modo de solo lectura.</div>

<div class="caja caja-advertencia"><span class="caja-etiqueta">ðŸ”´ IMPORTANTE:</span> Esta es la primera pantalla que debe configurar el Administrador. Sin ella, los usuarios de administraciÃ³n son dirigidos a ella al iniciar sesiÃ³n.</div>

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">Pantalla Residencial con las secciones de informaciÃ³n general, direcciÃ³n, estructura y contacto</span></div>

### 17.1 Completar la informaciÃ³n general

1. Selecciona <span class="mencion-ui">Residencial</span> en el menÃº lateral.
2. Presiona el campo <span class="mencion-ui">Nombre del residencial</span>.
3. Escribe el nombre del conjunto.
4. Presiona el campo <span class="mencion-ui">RNC</span>.
5. Escribe el Registro Nacional de Contribuyentes, si aplica.
6. Presiona el botÃ³n <span class="mencion-ui">Agregar</span> o <span class="mencion-ui">Actualizar</span>.

### 17.2 Completar la direcciÃ³n

1. Presiona el campo <span class="mencion-ui">Nombre de la vÃ­a</span>.
2. Escribe el nombre de la calle o avenida.
3. Presiona el campo <span class="mencion-ui">NÃºmero de la edificaciÃ³n</span>.
4. Escribe el nÃºmero.
5. Presiona el campo <span class="mencion-ui">Sector</span>.
6. Escribe el sector.
7. Presiona el campo <span class="mencion-ui">CÃ³digo Postal</span>.
8. Escribe el cÃ³digo postal.
9. Elige la <span class="mencion-ui">Provincia</span>.
10. Elige el <span class="mencion-ui">Municipio/Ciudad</span>.
11. Pega el <span class="mencion-ui">iframe de Google Map</span> en el campo indicado.
12. Revisa la vista previa del mapa.
13. Presiona el botÃ³n <span class="mencion-ui">Agregar</span> o <span class="mencion-ui">Actualizar</span>.

<div class="caja caja-nota"><span class="caja-etiqueta">ðŸ’¡ CONSEJO:</span> Los municipios disponibles se ajustan automÃ¡ticamente al elegir la provincia.</div>

<div class="captura"><span class="captura-titulo">INSERTAR CAPTURA DE PANTALLA</span><span class="captura-leyenda">SecciÃ³n Â«DirecciÃ³nÂ» del formulario del residencial con el selector de provincia y el mapa</span></div>

### 17.3 Completar la estructura

1. Elige la <span class="mencion-ui">DistribuciÃ³n</span> del residencial: *Torres* o *Edificios*.
2. Escribe la <span class="mencion-ui">Cantidad de edificios/torres</span>.
3. Escribe la <span class="mencion-ui">Cantidad de pisos por edificio/torre</span>.<div class="caja caja-advertencia"><span class="caja-etiqueta">IMPORTANTE:</span> El número de pisos no puede superar la cantidad máxima configurada en el residencial. Si se ingresa un valor mayor, el sistema mostrará un error y no permitirá guardar.</div>
4. Presiona el botÃ³n <span class="mencion-ui">Agregar</span> o <span class="mencion-ui">Actualizar</span>.

<div class="caja caja-advertencia"><span class="caja-etiqueta">ðŸ”´ IMPORTANTE:</span> La distribuciÃ³n se elige <strong>una sola vez</strong>. Una vez guardada, el campo queda bloqueado y no se puede cambiar.</div>

<div class="caja caja-nota"><span class="caja-etiqueta">ðŸ’¡ CONSEJO:</span> La distribuciÃ³n elegida determina si el resto del sistema habla de <em>Torres</em> o de <em>Edificios</em>.</div>

### 17.4 Completar los datos de contacto

1. Presiona el campo <span class="mencion-ui">TelÃ©fono de administraciÃ³n</span>.
2. Escribe el nÃºmero de contacto.
3. Presiona el campo <span class="mencion-ui">Correo de administraciÃ³n</span>.
4. Escribe el correo institucional.
5. Presiona el botÃ³n <span class="mencion-ui">Agregar</span> o <span class="mencion-ui">Actualizar</span>.

---

## 18. ConfiguraciÃ³n

El mÃ³dulo <span class="mencion-ui">ConfiguraciÃ³n</span> reÃºne la administraciÃ³n de las cuentas de usuario y la conexiÃ³n del sistema con un proveedor de inteligencia artificial. Se abre desde la opciÃ³n <span class="mencion-ui">ConfiguraciÃ³n</span> del menÃº de usuario y solo estÃ¡ disponible para el <span class="mencion-ui">Administrador</span>.

<div class="caja caja-advertencia"><span class="caja-etiqueta">âš ï¸ NOTA:</span> Esta pantalla es distinta del mÃ³dulo <em>Residencial</em> (capÃ­tulo 17), donde se registran los datos generales del residencial.</div>

### 18.1 PestaÃ±as del mÃ³dulo

La pantalla estÃ¡ organizada en seis pestaÃ±as. Solo <span class="mencion-ui">Usuarios</span> e <span class="mencion-ui">IntegraciÃ³n AI</span> estÃ¡n disponibles; las demÃ¡s muestran el aviso <span class="mencion-ui">MÃ³dulo prÃ³ximamente</span>.

| PestaÃ±a | Estado | Contenido |
|---|---|---|
| **Usuarios** | Disponible | Listado y gestiÃ³n de todas las cuentas del sistema. |
| **IntegraciÃ³n AI** | Disponible | Proveedor, modelo y clave de la inteligencia artificial. |
| **Seguridad** | PrÃ³ximamente | AÃºn no disponible. |
| **Notificaciones** | PrÃ³ximamente | AÃºn no disponible. |
| **Comprobantes fiscales** | PrÃ³ximamente | AÃºn no disponible. |
| **Preferencias generales** | PrÃ³ximamente | AÃºn no disponible. |

### 18.2 Ver los usuarios

1. Abre la pestaÃ±a <span class="mencion-ui">Usuarios</span>.
2. Localiza la tabla <span class="mencion-ui">Todos los usuarios</span>.

**Columnas disponibles:**

| Columna | Contenido |
|---|---|
| **Foto de perfil** | Imagen de la cuenta, o un marcador si no tiene. |
| **Nombre completo** | Nombre y apellido. Si no se registrÃ³, se muestra el correo. |
| **CÃ©dula** | Documento de identidad. |
| **TelÃ©fono** | NÃºmero de contacto. |
| **Correo electrÃ³nico** | Es el usuario de acceso. |
| **Rol** | Tipo de usuario del sistema. |
| **Fecha de ingreso** | Fecha de creaciÃ³n de la cuenta. |
| **Estado** | Activo, Inactivo o En verificaciÃ³n. |
| **Acciones** | Editar o eliminar la cuenta. |

### 18.3 Filtrar los usuarios

1. Usa el selector de estado para ver solo <span class="mencion-ui">Activo</span>, <span class="mencion-ui">Inactivo</span>, <span class="mencion-ui">En verificaciÃ³n</span> o <span class="mencion-ui">Todos los estados</span>.
2. Usa el botÃ³n <span class="mencion-ui">Todas las columnas</span> para mostrar u ocultar columnas de la tabla.

### 18.4 Agregar un usuario

1. Presiona el botÃ³n <span class="mencion-ui">Agregar usuario</span>.
2. Completa los campos <span class="mencion-ui">Nombre</span>, <span class="mencion-ui">Apellido</span>, <span class="mencion-ui">CÃ©dula</span>, <span class="mencion-ui">TelÃ©fono</span> y <span class="mencion-ui">Correo electrÃ³nico</span>.
3. Adjunta la <span class="mencion-ui">Foto de perfil</span>, si lo deseas.
4. Elige el <span class="mencion-ui">Rol</span> y el <span class="mencion-ui">Estado</span> de la cuenta.
5. Deja activo el interruptor <span class="mencion-ui">Activo</span> para que la cuenta pueda iniciar sesiÃ³n.
6. Escribe una <span class="mencion-ui">ContraseÃ±a temporal</span> y confÃ­rmala (mÃ­nimo 8 caracteres).
7. Presiona el botÃ³n <span class="mencion-ui">Agregar</span>.

<div class="caja caja-advertencia"><span class="caja-etiqueta">âš ï¸ NOTA:</span> El correo electrÃ³nico y la cÃ©dula no pueden repetirse entre cuentas. La contraseÃ±a temporal se guarda cifrada y es la que entregas al usuario para su primer ingreso.</div>

### 18.5 Editar un usuario

1. Ubica la fila del usuario.
2. Presiona el Ã­cono del <span class="mencion-ui">lÃ¡piz</span>.
3. Cambia los campos que necesites.
4. Presiona <span class="mencion-ui">Actualizar</span>.

<div class="caja caja-advertencia"><span class="caja-etiqueta">ðŸ”´ IMPORTANTE:</span> Al editar tu propia cuenta no podrÃ¡s cambiar tu rol ni desactivarla: el sistema mantiene el rol <em>Administrador</em> y el estado <em>Activo</em> para no bloquear tu acceso.</div>

### 18.6 Eliminar un usuario

1. Ubica la fila del usuario.
2. Presiona el Ã­cono de la <span class="mencion-ui">papelera</span>.
3. Presiona <span class="mencion-ui">SÃ­, Eliminar</span> para confirmar.

<div class="caja caja-advertencia"><span class="caja-etiqueta">âš ï¸ NOTA:</span> No puedes eliminar tu propia cuenta; el botÃ³n aparece deshabilitado.</div>

### 18.7 IntegraciÃ³n AI

La pestaÃ±a <span class="mencion-ui">IntegraciÃ³n AI</span> guarda la conexiÃ³n con un proveedor de inteligencia artificial, que el sistema usa para leer cÃ©dulas desde una foto en el mÃ³dulo <em>Visitantes</em>.

1. Abre la pestaÃ±a <span class="mencion-ui">IntegraciÃ³n AI</span>.
2. Elige el <span class="mencion-ui">Proveedor</span>: GPT (OpenAI), Claude (Anthropic), Gemini (Google), Llama (Meta), Mistral AI, DeepSeek o Grok (xAI).
3. Elige o escribe el <span class="mencion-ui">Modelo</span> dentro de ese proveedor.
4. Escribe la <span class="mencion-ui">API Key</span> con el botÃ³n del ojo para revisarla.
5. Presiona <span class="mencion-ui">Guardar</span> (o <span class="mencion-ui">Actualizar</span> si ya habÃ­a una clave guardada).

<div class="caja caja-advertencia"><span class="caja-etiqueta">ðŸ’¡ CONSEJO:</span> Para quitar una clave existente, deja el campo <span class="mencion-ui">API Key</span> en blanco y guarda.</div>

<div class="caja caja-advertencia"><span class="caja-etiqueta">âš ï¸ NOTA:</span> Algunos proveedores no ofrecen modelos con visiÃ³n (por ejemplo DeepSeek y Llama). Elige un proveedor con modelos de imagen para poder escanear cÃ©dulas.</div>

---

## 19. Preguntas Frecuentes y ResoluciÃ³n de Problemas

### 19.1 Preguntas Frecuentes

**1. Â¿Por quÃ© no me aparece un mÃ³dulo en el menÃº?**

El sistema muestra Ãºnicamente los mÃ³dulos permitidos para tu tipo de usuario. Si necesitas acceso a un mÃ³dulo que no aparece, solicita un cambio de permisos al Administrador.

---

**2. Â¿Por quÃ© el botÃ³n Agregar no aparece?**

Solo los Administradores y los Encargados de AdministraciÃ³n tienen permisos de creaciÃ³n en la mayorÃ­a de los mÃ³dulos. En Incidencias y Reservas, los residentes y propietarios tambiÃ©n pueden crear registros.

---

**3. Â¿Por quÃ© el botÃ³n Eliminar no aparece?**

La eliminaciÃ³n estÃ¡ reservada al Administrador y al Encargado de AdministraciÃ³n. En el mÃ³dulo Residencial, Ãºnicamente el Administrador puede eliminar registros.

---

**4. Â¿Por quÃ© no me puedo iniciar sesiÃ³n?**

Verifica que estÃ©s escribiendo tu <span class="mencion-ui">correo electrÃ³nico</span> y no tu nombre de usuario. TambiÃ©n confirma que tu cuenta estÃ© en estado <span class="mencion-ui">Activo</span> y que tu contraseÃ±a sea correcta.

---

**5. Â¿CÃ³mo recupero mi contraseÃ±a?**

Usa el enlace <span class="mencion-ui">Â¿Se te ha olvidado la clave?</span> del formulario de acceso, escribe tu correo electrÃ³nico y presiona <span class="mencion-ui">Enviar enlace</span>. Si el correo corresponde a una cuenta activa, recibirÃ¡s un mensaje con un enlace para crear una nueva contraseÃ±a. El enlace vence a los 30 minutos y solo puede usarse una vez. Por seguridad, el sistema muestra el mismo mensaje exista o no la cuenta.

---

**6. Â¿Por quÃ© el sistema me lleva a ConfiguraciÃ³n al entrar?**

Porque el residencial todavÃ­a no tiene informaciÃ³n registrada. El Administrador o el Encargado de AdministraciÃ³n debe completar la pantalla <span class="mencion-ui">Residencial</span> una vez.

---

**7. Â¿Por quÃ© el personal de seguridad entra directo a Visitantes?**

Por diseÃ±o. Las cuentas de Seguridad / PorterÃ­a estÃ¡n orientadas al control de accesos, por lo que el sistema abre ese mÃ³dulo directamente.

---

**8. Â¿Por quÃ© no aparece mi Ã¡rea comÃºn en el formulario de reservas?**

Solo se muestran las Ã¡reas en estado <span class="mencion-ui">Activo</span>. Verifica el estado del Ã¡rea en el mÃ³dulo Ãreas Comunes.

---

**9. Â¿Por quÃ© no puedo guardar una reserva en ese horario?**

El sistema valida tres reglas: la hora de fin debe ser posterior a la de inicio, la reserva debe caer dentro del horario del Ã¡rea y la fecha debe coincidir con los dÃ­as habilitados.

---

**10. Â¿Por quÃ© no puedo elegir una persona en el formulario?**

El desplegable de personas se habilita despuÃ©s de elegir el campo <span class="mencion-ui">Quien paga</span> (en Pagos). En Incidencias y Solicitudes, el desplegable se habilita despuÃ©s de elegir el departamento.

---

**11. Â¿Por quÃ© el sistema dice que la persona no pertenece al departamento?**

Cada registro debe vincular a una persona con su departamento. Cambia el departamento o elige una persona que corresponda a la unidad seleccionada.

---

**12. Â¿Por quÃ© no puedo cambiar la distribuciÃ³n del residencial?**

La distribuciÃ³n se define una sola vez porque afecta a toda la estructura del sistema. Una vez guardada, el campo queda bloqueado.

---

**13. Â¿Por quÃ© se eliminÃ³ una cuenta de usuario al registrar a una persona?**

Cada registro de propietario o residente genera su cuenta de acceso con el correo y la contraseÃ±a que indiques. Si el correo ya estaba en uso, el sistema rechaza el registro.

---

**14. Â¿DÃ³nde veo el historial de una incidencia?**

La columna <span class="mencion-ui">Comentarios/Actualizaciones</span> muestra el Ãºltimo seguimiento registrado. Cada vez que la administraciÃ³n cambia el estado y escribe un comentario, ese movimiento queda guardado con su fecha y responsable.

---

**15. Â¿CÃ³mo obtengo un comprobante de pago?**

Abre el pago que quieres facturar desde el Ã­cono del <span class="mencion-ui">lÃ¡piz</span> y presiona el botÃ³n <span class="mencion-ui">Generar comprobante</span> del encabezado. El botÃ³n se habilita cuando los campos obligatorios estÃ¡n completos.

---

### 19.2 ResoluciÃ³n de Problemas

**Problema: aparece el mensaje Â«El email o la contraseÃ±a no son vÃ¡lidosÂ»**

1. Verifica que el correo estÃ© escrito correctamente.
2. Verifica que no haya espacios al inicio o al final.
3. Confirma que la cuenta estÃ© en estado <span class="mencion-ui">Activo</span>.
4. Si olvidaste la contraseÃ±a, usa el enlace <span class="mencion-ui">Â¿Se te ha olvidado la clave?</span> para restablecerla por correo.

---

**Problema: la tabla muestra Â«Sin coincidenciasÂ»**

1. Revisa los filtros activos en la barra superior.
2. Cambia los filtros a la opciÃ³n <span class="mencion-ui">Todos...</span>.
3. Avanza a la siguiente pÃ¡gina de resultados, si aplica.

---

**Problema: el sistema no me deja subir una imagen**

1. Verifica que el archivo sea JPG, PNG o WEBP.
2. Verifica que el archivo pese menos de 2 MB.
3. Verifica que el formato estÃ© permitido en ese campo. Las evidencias de incidencias y los adjuntos de solicitudes tambiÃ©n aceptan PDF.

---

**Problema: el sistema dice Â«La hora de fin debe ser posterior a la hora de inicioÂ»**

1. Revisa la <span class="mencion-ui">Hora de inicio</span> del formulario.
2. Corrige la <span class="mencion-ui">Hora de fin</span> con un valor mÃ¡s tarde.
3. Vuelve a guardar el registro.

---

**Problema: el sistema dice Â«Fuera del horario del Ã¡reaÂ»**

1. Revisa el horario permitido del Ã¡rea en el mÃ³dulo Ãreas Comunes.
2. Ajusta la <span class="mencion-ui">Hora de inicio</span> y la <span class="mencion-ui">Hora de fin</span> dentro de ese rango.

---

**Problema: el sistema dice Â«Esa Ã¡rea solo estÃ¡ disponible...Â»**

1. Cambia la <span class="mencion-ui">Fecha de reserva</span> por un dÃ­a permitido.
2. Si necesitas otro dÃ­a, pide a la administraciÃ³n que modifique los <span class="mencion-ui">DÃ­as habilitados</span> del Ã¡rea.

---

**Problema: el botÃ³n Generar comprobante aparece deshabilitado**

1. Completa el campo <span class="mencion-ui">Departamento</span>.
2. Completa el campo de la persona que paga.
3. Completa el campo <span class="mencion-ui">Monto</span>.
4. Completa el campo <span class="mencion-ui">Concepto</span>.
5. Completa el campo <span class="mencion-ui">PerÃ­odo/Mes correspondiente</span>.
6. Completa el campo <span class="mencion-ui">Estado</span>.

---

**Problema: el enlace Ver todo de Actividad Reciente no abre una pantalla propia**

Se trata de una funcionalidad en construcciÃ³n. Por ahora, toda la actividad reciente se muestra directamente en el panel de inicio.

---

**Problema: aparece el mensaje Â«No tienes permisos para acceder a este mÃ³duloÂ»**

Tu tipo de usuario no tiene acceso a esa secciÃ³n. Regresa al Inicio y utiliza los mÃ³dulos que te aparecen en el menÃº lateral.

---

**Problema: aparece el mensaje Â«No se pudo crear el comunicado: no hay ningÃºn jardÃ­n configuradoÂ»**

Debes registrar primero al menos un jardÃ­n con sus edificios desde el mÃ³dulo <span class="mencion-ui">Departamentos</span>, antes de publicar comunicados.

---

### 19.3 MÃ³dulos no disponibles en la interfaz

Actualmente el sistema <span class="mencion-ui">no muestra</span> los mÃ³dulos de <span class="mencion-ui">Chat</span> y <span class="mencion-ui">Notificaciones</span> en el menÃº lateral. Estas secciones se encuentran en fase de desarrollo y todavÃ­a no estÃ¡n habilitadas para los usuarios.

Si necesitas recibir avisos automÃ¡ticos o communicate con la administraciÃ³n, utiliza por ahora el mÃ³dulo <span class="mencion-ui">Comunicados</span> o registra una <span class="mencion-ui">Solicitud</span>.

---

### 19.4 CuÃ¡ndo solicitar ayuda

Contacta a la administraciÃ³n del residencial cuando:

- No puedas iniciar sesiÃ³n tras varios intentos.
- Necesites un cambio de permisos o de tipo de usuario.
- No recibas el correo de recuperaciÃ³n de contraseÃ±a o el enlace haya vencido.
- Detectes un dato incorrecto que no puedes corregir por tu cuenta.
- Necesites informaciÃ³n que los reportes no muestran.

---

*Fin del manual de usuario â€” CONDOSYS*

