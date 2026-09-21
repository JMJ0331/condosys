/**
 * Lógica de la cuadrícula de pagos (/pagos/).
 * - Auto-submit de filtros (#filtros-pagos).
 * - Selector de columnas visibles (#boton-columnas / #panel-columnas).
 * - Calendarios de mes y año (#boton-mes / #panel-mes, #boton-anio / #panel-anio):
 *   rejilla de meses y lista de años que filtran al elegir.
 *
 * Sin etiquetas de plantilla Django: solo usa IDs y atributos data-*.
 */
(() => {
  const formularioFiltros = document.getElementById('filtros-pagos');
  if (formularioFiltros) {
    formularioFiltros.querySelectorAll('select').forEach((select) => {
      select.addEventListener('change', () => formularioFiltros.submit());
    });
  }

  const botonColumnas = document.getElementById('boton-columnas');
  const panelColumnas = document.getElementById('panel-columnas');
  const toggleTodas = document.getElementById('toggle-todas-columnas');

  if (botonColumnas && panelColumnas) {
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
  }

  // --- Calendarios de mes y año: rejilla que filtra al elegir ---
  const calendarios = [
    { boton: 'boton-mes', panel: 'panel-mes', valor: 'valor-mes', opcion: 'mes' },
    { boton: 'boton-anio', panel: 'panel-anio', valor: 'valor-anio', opcion: 'anio' },
  ];

  function cerrarCalendarios(excepto) {
    calendarios.forEach(({ boton, panel }) => {
      if (panel === excepto) return;
      const panelEl = document.getElementById(panel);
      const botonEl = document.getElementById(boton);
      if (panelEl) panelEl.hidden = true;
      if (botonEl) botonEl.setAttribute('aria-expanded', 'false');
    });
  }

  calendarios.forEach(({ boton, panel, valor, opcion }) => {
    const botonEl = document.getElementById(boton);
    const panelEl = document.getElementById(panel);
    const valorEl = document.getElementById(valor);
    if (!botonEl || !panelEl || !valorEl || !formularioFiltros) return;

    botonEl.addEventListener('click', () => {
      const abierto = !panelEl.hidden;
      cerrarCalendarios(panel);
      panelEl.hidden = abierto;
      botonEl.setAttribute('aria-expanded', String(!abierto));
    });

    panelEl.querySelectorAll(`[data-${opcion}]`).forEach((opcionEl) => {
      opcionEl.addEventListener('click', () => {
        valorEl.value = opcionEl.dataset[opcion];
        formularioFiltros.submit();
      });
    });
  });

  document.addEventListener('click', (evento) => {
    if (!evento.target.closest('.selector-calendario')) cerrarCalendarios(null);
  });

  document.addEventListener('keydown', (evento) => {
    if (evento.key === 'Escape') cerrarCalendarios(null);
  });
})();
