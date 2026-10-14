# Paleta de colores CONDOSYS

Análisis de uso de las variables de color en los 25 archivos CSS del proyecto
(976 usos totales en 33 variables con uso; las 31 restantes aparecen en 0%).

## Colores más utilizados

| Variable CSS | Hexadecimal | % de uso | Uso |
|---|---|---|---|
| `--black-50` | `#E7E7E7` | 18.75% | Bordes de inputs, tarjetas y separadores (`1px solid`) |
| `--white-50` | `#fefefe` | 16.91% | Fondo de tarjetas, inputs y elementos; texto sobre fondos verdes |
| `--green-900` | `#163D1F` | 15.98% | Verde oscuro: fondo del sidebar, botones primarios, títulos y texto de acento |
| `--black-400` | `#41413D` | 13.42% | Texto principal del contenido (gris oscuro) |
| `--white-700` | `#acacac` | 5.64% | Texto secundario / enmudecido, placeholders y fechas |
| `--black-300` | `#60605d` | 3.69% | Texto secundario de tablas y descripciones |
| `--white-400` | `#f5f5f5` | 3.48% | Fondo de filas alternas en tablas y hover suave |
| `--red-500` | `#EE443F` | 3.38% | Alerts/errores, acciones de eliminar y estados de cancelación |
| `--green-700` | `#308242` | 2.87% | Hover/presionado de botones verdes secundarios |
| `--green-100` | `#c5e9cd` | 1.95% | Fondo de badges/estados activos y checkboxes marcados |
| `--white-500` | `#f2f2f2` | 1.64% | Fondo de filas alternas / headers de tabla |
| `--green-200` | `#a9deb4` | 1.54% | Anillo de foco de campos e inputs seleccionados |
| `--green-600` | `#3da755` | 1.54% | Verde medio: botones secundarios y scrollbar del sidebar |
| `--green-800` | `#256533` | 1.54% | Hover/dark de botones verdes (hover de primarios) |
| `--white-100` | `#fbfbfb` | 1.33% | Fondo de zonas secundarias (áreas de drop, paneles de detalle) |
| `--green-25` | `#F6FBF3` | 1.23% | Fondos de secciones de éxito / resultados |
| `--black-100` | `#B5B6B4` | 1.13% | Bordes discontinuos (`dashed`) de zonas de arrastre |
| `--green-50` | `#ecf8ef` | 0.82% | Fondos de estados "éxito/activo" suaves |
| `--red-50` | `#FDECEC` | 0.41% | Fondos de alerts de error |
| `--red-600` | `#D93E39` | 0.41% | Botones de eliminar (rojo) |
| `--red-700` | `#A9302D` | 0.41% | Botones de confirmar eliminación |
| `--red-900` | `#641D1A` | 0.41% | Hover del botón de eliminar |
| `--white-50-active` | `rgba(254,254,254,0.5)` | 0.20% | Estado activo de botones de icono |
| `--black-200` | `#929290` | 0.20% | Bordes/separadores grises secundarios |
| `--red-100` | `#FAC5C3` | 0.20% | Bordes de alerts de error |
| `--yellow-700` | `#B57900` | 0.20% | Fondos de estados pendientes / avisos |
| `--white-300` | `#f6f6f6` | 0.10% | Fondos hover sutiles |
| `--white-50-hover` | `rgba(254,254,254,0.2)` | 0.10% | Hover de botones de icono |
| `--green-75` | `#BECABE` | 0.10% | Verde grisáceo en divisores suaves |
| `--green-400` | `#69c57d` | 0.10% | Verde medio-claro de acento |
| `--green-500` | `#43b755` | 0.10% | Verde brillante (hover del scrollbar del sidebar) |
| `--blue-50` | `#e6f4ff` | 0.10% | Fondo de bloques informativos (azul suave) |
| `--yellow-100` | `#FFE5B0` | 0.10% | Fondo/borde de avisos ámbar suaves |

## Resumen de la paleta

- **Verde (`--green-*`)** — color corporativo del sistema (sidebar, botones, estados de éxito).
- **Neutros (blancos/negros)** — base: fondos, bordes y tipografía.
- **Rojo (`--red-500`)** — acento para acciones destructivas y errores.
- **Azul y amarillo** — acentos residuales (menos del 1% combinado).

Aplica el siguiente sistema de diseño visual (UI/CSS Style Guide) a las diapositivas/páginas. Mantén el texto existente intacto y aplica de forma estricta únicamente los estilos gráficos, colores, pesos y espaciados detallados a continuación:

1. PALETA DE COLORES:
- Color Primario Institucional: #163D1F (--green-900) para fondos de encabezados superiores, títulos principales H1/H2, botones primarios y encabezados de tablas.
- Fondo General de Tarjetas/Documento: #FEFEFE (--white-50).
- Texto Principal del Cuerpo: #41413D (--black-400).
- Texto Secundario/Metadatos/Placeholders: #60605D (--black-300) y #ACACAC (--white-700).
- Bordes de Tarjetas, Inputs y Separadores: 1px solid #E7E7E7 (--black-50).
- Fondos Alternos de Tablas (Efecto Cebra): #F5F5F5 (--white-400).
- Cajas de Notas / Consejos: Fondo #F6FBF3 (--green-25) con borde lateral izquierdo de 3px solid #3DA755 (--green-600).
- Cajas de Advertencias / Importante: Fondo #FFE5B0 (--yellow-100) con borde lateral izquierdo de 3px solid #B57900 (--yellow-700).
- Cajas de Errores / Alertas: Fondo #FDECEC (--red-50) con borde lateral izquierdo de 3px solid #D93E39 (--red-500).

2. TIPOGRAFÍA Y PESOS (FONT-WEIGHT):
- Familia Tipográfica: Sans-serif limpia estilo UI (Inter o Roboto).
- Títulos Principales (H1): Peso 700 (Bold), color #163D1F, tamaño 20pt / 28px, line-height 1.2.
- Subtítulos y Secciones (H2 / H3): Peso 600 (Semi-Bold), color #41413D.
- Botones, Badges y Etiquetas de Pasos ("Paso 1", "Paso 2"): Peso 600 (Semi-Bold).
- Cuerpo de Texto y Pasos Numerados: Peso 400 (Regular), color #41413D, line-height 1.5 a 1.6, tamaño 10.5pt / 14px.
- Mención de Botones/Elementos UI en el Texto: Aplicar estilo de contenedor tipo Pill/Badge con fondo #F5F5F5, borde 1px solid #E7E7E7, texto en color #163D1F con peso 600.

3. ESPACIADOS, PADDING Y TRACKING:
- Tracking / Letter-spacing para mayúsculas sostenidas ("CONDOSYS", "IMPORTANTE", "CONSEJO"): +0.05em (+0.8px).
- Tracking para Badges/Estados ("Pagado", "Pendiente", "Vencido"): +0.02em (+0.3px).
- Espaciado entre bloques de pasos: 20px a 24px.
- Padding interno de cajas de llamado/alerta: 12px vertical, 16px horizontal, border-radius de 6px.

4. MAQUETADO DE TABLAS Y PLACEMENT DE IMÁGENES:
- Encabezados de Tabla (TH): Fondo #163D1F, texto #FEFEFE en negrita (peso 600), padding de 10px 14px.
- Filas de Tabla (TD): Bordes en #E7E7E7 (1px solid), alternando fondo de fila con #F5F5F5.
- Badges de Estado en Tablas: 
  * Activo / Pagado: Fondo #C5E9CD, Texto #163D1F.
  * Pendiente / Aviso: Fondo #FFE5B0, Texto #B57900.
  * Vencido / Rechazado: Fondo #FDECEC, Texto #D93E39.
- Bloques Marcadores para Capturas de Pantalla: Cajas contenedoras con fondo #FBFBFB, borde discontinuo (1px dashed #B5B6B4) y texto de la leyenda en #60605D.
