/**
 * Lógica específica del módulo Áreas Comunes.
 * - Página index (#filtros-areas): selector de columnas + auto-submit filtros.
 *
 * La plantilla index.html debe usar:
 *   - <form id="filtros-areas"> con los <select> de filtro
 *   - <button id="boton-columnas"> + <div id="panel-columnas">
 *     + <input id="toggle-todas-columnas">
 *   - <th data-columna="..."> en la tabla (salvo acciones)
 *
 * La plantilla agregar.html debe usar:
 *   - <textarea data-contador="id-del-contador"> (el valor de maxlength
 *     es el límite) + <p id="id-del-contador"> con [data-contador-numero]
 *     y [data-contador-maximo].
 */
(() => {
  const formularioFiltros = document.getElementById('filtros-areas');
  if (formularioFiltros) {
    formularioFiltros.querySelectorAll('select').forEach((select) => {
      select.addEventListener('change', () => formularioFiltros.submit());
    });
  }

  const botonColumnas = document.getElementById('boton-columnas');
  const panelColumnas = document.getElementById('panel-columnas');
  const toggleTodas = document.getElementById('toggle-todas-columnas');

  if (botonColumnas && panelColumnas) {
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

    function aplicarCasilla(nombre, visible) {
      document.querySelectorAll(`[data-columna="${nombre}"]`).forEach((celda) => {
        celda.style.display = visible ? '' : 'none';
      });
    }

    function sincronizarTodas() {
      toggleTodas.checked = columnas.every(({ nombre }) => casillas.get(nombre).checked);
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

    toggleTodas.addEventListener('change', () => {
      columnas.forEach(({ nombre }) => {
        casillas.get(nombre).checked = toggleTodas.checked;
        aplicarCasilla(nombre, toggleTodas.checked);
      });
    });

    casillas.forEach((casilla, nombre) => {
      casilla.addEventListener('change', () => {
        aplicarCasilla(nombre, casilla.checked);
        sincronizarTodas();
      });
    });

    document.addEventListener('click', (evento) => {
      if (!evento.target.closest('.selector-columnas')) cerrarPanel();
    });
  }

  // --- Páginas agregar/actualizar: contador de caracteres ---
  document.querySelectorAll('textarea[data-contador]').forEach((campo) => {
    const contador = document.getElementById(campo.dataset.contador);
    if (!contador) return;
    const numero = contador.querySelector('[data-contador-numero]');
    const maximo = contador.querySelector('[data-contador-maximo]');
    const limite = Number.parseInt(campo.getAttribute('maxlength'), 10);

    function actualizar() {
      if (numero) numero.textContent = String(campo.value.length);
      if (maximo && !Number.isNaN(limite)) maximo.textContent = String(limite);
      contador.classList.toggle(
        'limite-alcanzado',
        !Number.isNaN(limite) && campo.value.length >= limite
      );
    }

    campo.addEventListener('input', actualizar);
    actualizar();
  });
})();
