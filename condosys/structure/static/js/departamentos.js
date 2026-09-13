/**
 * Lógica específica del módulo Departamentos (structure).
 * - Página index (#filtros-departamentos): selector de columnas + auto-submit filtros.
 * - Página agregar: filtro de jardín → edificio, búsqueda de propietario, interruptor ocupado.
 *
 * La plantilla agregar.html debe usar:
 *   - <select id="select-jardin">
 *   - <select data-departamento="edificio">     (sus opciones llevan data-garden)
 *   - <select data-departamento="propietario">
 *   - <input id="buscar-residente">
 *   - <input type="checkbox" id="toggle-ocupado">
 *   - <input type="hidden" id="id_status">
 */
(() => {
  // --- Página index: selector de columnas + auto-submit filtros ---

  const formularioFiltros = document.getElementById('filtros-departamentos');
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
      .map((th) => ({ nombre: th.dataset.columna, texto: th.textContent.trim() }));

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

  // --- Página agregar: filtros enlazados jardín → edificio + propietario ---

  const selectJardin = document.getElementById('select-jardin');
  const selectEdificio = document.querySelector('[data-departamento="edificio"]');
  const selectPropietario = document.querySelector('[data-departamento="propietario"]');
  const inputBuscarResidente = document.getElementById('buscar-residente');
  const toggleOcupado = document.getElementById('toggle-ocupado');
  const inputStatus = document.getElementById('id_status');
  const inputTorre = document.getElementById('torre-departamento');
  const inputBloque = document.getElementById('bloque-departamento');

  function filtrarEdificios() {
    if (!selectJardin || !selectEdificio) return;
    const jardin = selectJardin.value;
    selectEdificio.querySelectorAll('option[data-garden]').forEach((opt) => {
      opt.hidden = jardin !== '' && opt.dataset.garden !== jardin;
    });
    if (
      selectEdificio.value !== '' &&
      selectEdificio.selectedOptions[0]?.dataset.garden &&
      selectEdificio.selectedOptions[0].dataset.garden !== jardin
    ) {
      selectEdificio.value = '';
    }
    mostrarUbicacion();
  }

  function mostrarUbicacion() {
    if (!selectEdificio) return;
    const opt = selectEdificio.selectedOptions[0];
    if (inputTorre) {
      inputTorre.value = opt ? opt.dataset.torre || '' : '';
    }
    if (inputBloque) {
      inputBloque.value = opt ? opt.dataset.bloque || '' : '';
    }
  }

  function filtrarResidentes() {
    if (!inputBuscarResidente || !selectPropietario) return;
    const termino = inputBuscarResidente.value.trim().toLowerCase();
    selectPropietario.querySelectorAll('option').forEach((opt) => {
      opt.hidden = termino === '' || opt.textContent.toLowerCase().includes(termino);
    });
    if (
      selectPropietario.value !== '' &&
      !selectPropietario.selectedOptions[0]?.textContent.toLowerCase().includes(termino)
    ) {
      selectPropietario.value = '';
    }
  }

  function sincronizarEstado() {
    if (toggleOcupado && inputStatus) {
      inputStatus.value = toggleOcupado.checked ? 'occupied' : 'empty';
    }
  }

  if (selectJardin && selectEdificio) {
    selectJardin.addEventListener('change', filtrarEdificios);
    selectEdificio.addEventListener('change', mostrarUbicacion);
    filtrarEdificios();
    mostrarUbicacion();
  }

  if (inputBuscarResidente && selectPropietario) {
    inputBuscarResidente.addEventListener('input', filtrarResidentes);
  }

  if (toggleOcupado && inputStatus) {
    toggleOcupado.addEventListener('change', sincronizarEstado);
  }
})();