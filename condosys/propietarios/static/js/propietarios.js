/**
 * Lógica específica del módulo Propietarios.
 * - Filtros: envío automático al cambiar cualquier select.
 * - Selector de columnas visibles: botón "Todas las columnas" que abre
 *   un panel con una casilla por columna + casilla "Todas"
 *   (mismo comportamiento que Residentes y Departamentos).
 *
 * La plantilla index.html debe usar:
 *   - <form id="filtros-propietarios">           (se enviará al cambiar filtros)
 *   - <button id="boton-columnas">
 *   - <div id="panel-columnas" hidden> con <input id="toggle-todas-columnas">
 *   - celdas con data-columna="clave"
 */
(() => {
  const formularioFiltros = document.getElementById('filtros-propietarios');
  if (formularioFiltros) {
    formularioFiltros.querySelectorAll('select').forEach((select) => {
      select.addEventListener('change', () => formularioFiltros.submit());
    });
  }

  const botonColumnas = document.getElementById('boton-columnas');
  const panelColumnas = document.getElementById('panel-columnas');
  const toggleTodas = document.getElementById('toggle-todas-columnas');

  if (!botonColumnas || !panelColumnas) return;

  // Recoge las claves de columna declaradas en los <th> para poder ocultarlas por nombre.
  // Excluye "acciones" que siempre debe permanecer visible.
  const columnas = Array.from(document.querySelectorAll('th[data-columna]'))
    .map((th) => ({ nombre: th.dataset.columna, texto: th.textContent.trim() }))
    .filter(({ nombre }) => nombre !== 'acciones');

  const casillas = new Map();
  columnas.forEach(({ nombre, texto }) => {
    const etiqueta = document.createElement('label');
    const casilla = document.createElement('input');
    const textoColumnas = document.createElement('span');
    etiqueta.className = 'opcion-columna';
    casilla.type = 'checkbox';
    casilla.checked = true;
    textoColumnas.textContent = texto;
    etiqueta.append(casilla, textoColumnas);
    panelColumnas.appendChild(etiqueta);
    casillas.set(nombre, casilla);
  });

  // Oculta o muestra las celdas y cabeceras que compartan el mismo data-columna.
  function aplicarCasilla(nombre, visible) {
    document.querySelectorAll(`[data-columna="${nombre}"]`).forEach((celda) => {
      celda.style.display = visible ? '' : 'none';
    });
  }

  function sincronizarTodas() {
    if (toggleTodas) {
      toggleTodas.checked = columnas.every(({ nombre }) => casillas.get(nombre).checked);
    }
  }

  function cerrarPanel() {
    panelColumnas.hidden = true;
    botonColumnas.setAttribute('aria-expanded', 'false');
  }

  botonColumnas.addEventListener('click', () => {
    const abierto = !panelColumnas.hidden;
    panelColumnas.hidden = abierto;
    botonColumnas.setAttribute('aria-expanded', String(!abierto));
  });

  if (toggleTodas) {
    toggleTodas.addEventListener('change', () => {
      columnas.forEach(({ nombre }) => {
        casillas.get(nombre).checked = toggleTodas.checked;
        aplicarCasilla(nombre, toggleTodas.checked);
      });
    });
  }

  casillas.forEach((casilla, nombre) => {
    casilla.addEventListener('change', () => {
      aplicarCasilla(nombre, casilla.checked);
      sincronizarTodas();
    });
  });

  document.addEventListener('click', (evento) => {
    if (!evento.target.closest('.selector-columnas')) cerrarPanel();
  });
})();
