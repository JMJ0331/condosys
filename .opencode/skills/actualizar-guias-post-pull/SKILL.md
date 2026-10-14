---
name: actualizar-guias-post-pull
description: Use cuando un `git pull` trae cambios nuevos al repo CONDOSYS o cuando el usuario pide "actualizar las guías/manuales", "post-pull", "revisa el pull" o "sincroniza la documentación". Lee el diff de git y actualiza `manual-de-usuario-condosys.md` y/o `MANUAL_TECNICO_CONDOSYS.md` solo si los cambios de código impactan lo que está documentado.
---

# Actualizar guías de CONDOSYS tras un `git pull`

Mantiene sincronizados los dos documentos del repositorio con el código que acaba de llegar:

- `manual-de-usuario-condosys.md` — guía para usuarios finales y administradores.
- `MANUAL_TECNICO_CONDOSYS.md` — arquitectura, modelos, API, permisos y despliegue.

Regla central: **solo se edita si hay relación directa** entre el diff y algo ya documentado. Si no la hay, no se toca nada.

## Cuándo se ejecuta

- Automáticamente: el plugin `.opencode/plugins/guias-post-pull.ts` detecta un `git pull` exitoso con cambios nuevos e inyecta la orden de ejecutar esta skill en la salida del comando.
- Manualmente: comando `/actualizar-guias-post-pull` o cuando el usuario lo pida.

## Paso 0 — Determinar el rango de cambios

Trabaja siempre desde la raíz del repo (es donde viven el `manage.py` y las guías). Ejecuta:

```powershell
git log --oneline -1
git log ORIG_HEAD..HEAD --oneline
git diff --stat ORIG_HEAD HEAD
git diff --name-status ORIG_HEAD HEAD
```

- Tras un `git pull`/merge, `ORIG_HEAD` apunta al commit previo. Ese es el rango correcto.
- Si `ORIG_HEAD` no existe o el diff sale vacío, usa `HEAD@{1}`:
  `git diff --stat HEAD@{1} HEAD`.
- Filtra el ruido: ignora `db.sqlite3`, `.env`, `venv/`, `media/`, `__pycache__`, `.pdf` y archivos de solo estilo sin efecto funcional.

## Paso 1 — Clasificar los archivos cambiados

| Archivo o ruta cambiada | Documento probable | Capítulo / sección |
|---|---|---|
| `*/models.py`, `*/migrations/*`, `residencial/`, `structure/` | Técnico | 3 Arquitectura, 6 Modelo de datos |
| `*/serializers.py`, `*/views.py` (ViewSets), `*/urls.py` | Técnico | 7 API REST |
| `accounts/`, `accounts/permissions.py`, `login/` | Ambos | Técnico 5; Usuario 3, 18 |
| `*/forms.py`, `templates/**`, `static/**` | Usuario | Capítulo del módulo |
| `payments/`, `maintenance/` | Usuario (+Técnico si cambia modelo/API) | Usuario 8, 9; Técnico 6, 7 |
| `residents/`, `propietarios/`, `structure/` | Usuario (+Técnico) | Usuario 5, 6, 7; Técnico 6 |
| `incidents/`, `solicitudes/` | Usuario | 10, 11 |
| `visitors/`, `areas_comunes/`, `reservations/` | Usuario | 12, 13, 14 |
| `communications/`, `notifications/`, `reports/` | Usuario (+Técnico) | Usuario 15, 16; Técnico 7 |
| `chat/`, `condosys/asgi.py`, `settings.py` (channels) | Técnico | 3, 9 |
| `requirements.txt`, `settings.py`, `asgi.py` | Técnico | 2, 4, 10 |
| `login/`, `templates/base.html`, menú/sidebar | Usuario | 2, 3 |

Módulos = apps Django: `accounts`, `residents`, `propietarios`, `payments`, `maintenance`, `incidents`, `solicitudes`, `visitors`, `areas_comunes`, `reservations`, `communications`, `notifications`, `reports`, `chat`, `structure`, `residencial`, `configuracion`, `login`, `inicio`.

## Paso 2 — Decidir si hay impacto (puerta de calidad)

Antes de escribir una sola línea, responde:

1. ¿El cambio añade/quita/renombra una **funcionalidad, campo, botón, estado, rol, ruta o módulo** que ya está descrito en alguna guía?
2. ¿Contradice lo que el manual afirma hoy (p. ej. un "problema conocido" que ya se arregló, o un websocket que ya funciona)?
3. ¿Solo es refactor interno, renombrado de variables, formato o tests, sin cambio visible ni de contrato?

Solo edita si (1) o (2) es verdadero. Si (3) aplica y nada más → **no modifiques nada** y reporta por qué.

Casos que casi siempre impactan:
- Nueva app/módulo, nuevo rol o cambio en `accounts/permissions.py`.
- Nuevo endpoint, cambio de serializer o de permisos DRF.
- Cambios en `settings.py` (apps instaladas, auth, ASGI, DB) → Técnico.
- Cambios de campos/validaciones que el usuario percibe (formularios, columnas, estados).

Casos que casi nunca impactan: renombrados internos, `tests.py`, ajustes de formato, migraciones que solo reordenan, cambios de comentarios.

## Paso 3 — Editar conservando estilo

### `manual-de-usuario-condosys.md`
- Español, tuteo, instrucciones numeradas e imperativas ("Presiona…", "Elige…", "Escribe…").
- Empieza con un bloque `<style>` y usa HTML embebido. **No** añadas `<script>` inline, `style=` ni etiquetas nuevas fuera del vocabulario existente.
- Elementos a reutilizar: `<h1>`, `##`, `###`, `<span class="mencion-ui">Texto de la UI</span>`, badges (`badge-exito`, `badge-aviso`, `badge-error`), cajas (`caja caja-nota`, `caja caja-advertencia`, `caja caja-error`), `<div class="captura">` para capturas, `<span class="etiqueta-paso">Paso N</span>`, tablas comparativas.
- Si agregas un módulo o sección, actualiza también el **Índice** (lista numerada del inicio) y respeta la numeración correlativa.

### `MANUAL_TECNICO_CONDOSYS.md`
- Markdown puro, tono técnico en tercera persona.
- Mantén el bloque de metadatos inicial (`| Fecha | … |`, `Versión`). Si el cambio es sustancial, actualiza `Fecha` (mes/año actual) y sube `Versión` cuando sea estructural.
- **No reemplaces `<!--INDICE-->`**: es un marcador que se resuelve al generar. Simplemente no lo toques.
- Conserva las convenciones: cajas `> **ATENCIÓN** —`, `> **PENDIENTE**`, `> **BUG**`; pies de tabla `*Tabla X.Y - …*`; bloques ```` ```python ```` con extractos literales.
- Los identificadores (archivos, clases, funciones) van en backticks.
- Si un "problema conocido" del capítulo 11 ya se resolvió en el diff, actualízalo o retíralo; no dejes texto que contradiga el código.

### Sobre el PDF
`MANUAL_TECNICO_CONDOSYS.pdf` lo genera `generar_manual_tecnico.py`, y ese script **no lee** el `.md` (el contenido está en Python). Editar el `.md` **no** regenera el PDF. Si el usuario pide el PDF, hay que actualizar también el script y ejecutar `.venv\Scripts\python.exe generar_manual_tecnico.py`. Menciónalo, no lo hagas por iniciativa propia.

## Paso 4 — Verificar

- Relee la sección editada de principio a fin: sin HTML/Markdown roto, sin numeración saltada, sin contradicciones.
- `git diff -- manual-de-usuario-condosys.md MANUAL_TECNICO_CONDOSYS.md` para confirmar que el cambio es acotado.
- Verifica que los enlaces del índice sigan resolviendo.

## Paso 5 — Reportar

Resume: rango de commits revisado, archivos de código con impacto, secciones exactas modificadas y por qué. Si no hubo impacto, dilo explícitamente.

## Reglas de oro

- **No editar sin relación directa.** Ante la duda, no toques.
- **No reescribir** secciones completas ni reformatear: cambios quirúrgicos y en el mismo estilo.
- **No inventar** funcionalidades, capturas ni cifras que el diff no respalde.
- **No hacer commit** salvo que el usuario lo pida (el repo trabaja en la rama `desarrollo`).
- Reportar siempre el resultado, aunque sea "sin cambios".

## Prompt interno (flujo operativo)

Al activarte, sigue exactamente esto:

1. Identifica el rango con `git diff --stat ORIG_HEAD HEAD` y `git log ORIG_HEAD..HEAD --oneline` (fallback `HEAD@{1}`).
2. Lista los archivos cambiados y clasifícalos con la tabla del Paso 1.
3. Decide impacto con la puerta de calidad del Paso 2. Si no hay impacto, detente y reporta.
4. Para cada sección afectada, **lee el fragmento actual** del `.md` y edítalo en su lugar, imitando su estructura y vocabulario. No agregues dependencias ni estilos nuevos.
5. Actualiza índices y metadatos si corresponde.
6. Cierra con el reporte del Paso 5.
