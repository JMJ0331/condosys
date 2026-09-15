/**
 * Lógica específica del módulo Departamentos (structure).
 * - Página index (#filtros-departamentos): selector de columnas + auto-submit filtros.
 * - Página agregar: filtro de jardín → edificio, zona de imagen e interruptor ocupado.
 *
 * La plantilla agregar.html debe usar:
 *   - <select id="select-jardin">
 *   - <select data-departamento="edificio">     (sus opciones llevan data-garden)
 *   - <input type="file" data-departamento="foto">
 *   - <div id="zona-imagen"> + <img id="vista-previa-imagen"> + <span id="contenido-zona">
 *   - <button id="boton-subir-imagen">
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

  // --- Página agregar: jardín → edificio, zona de imagen y estado ---

  const selectJardin = document.getElementById('select-jardin');
  const selectEdificio = document.querySelector('[data-departamento="edificio"]');
  const toggleOcupado = document.getElementById('toggle-ocupado');
  const inputStatus = document.getElementById('id_status');
  const inputTorre = document.getElementById('torre-departamento');
  const inputBloque = document.getElementById('bloque-departamento');
  const zonaImagen = document.getElementById('zona-imagen');
  const inputFoto = document.querySelector('[data-departamento="foto"]');
  const botonSubir = document.getElementById('boton-subir-imagen');
  const vistaPrevia = document.getElementById('vista-previa-imagen');
  const contenidoZona = document.getElementById('contenido-zona');
  const nombreArchivo = document.getElementById('nombre-archivo');
  let urlPrevia = null;

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

  function sincronizarEstado() {
    if (toggleOcupado && inputStatus) {
      inputStatus.value = toggleOcupado.checked ? 'occupied' : 'empty';
    }
  }

  function mostrarVistaPrevia(archivo) {
    if (!archivo || !vistaPrevia) return;
    if (urlPrevia) URL.revokeObjectURL(urlPrevia);
    urlPrevia = URL.createObjectURL(archivo);
    vistaPrevia.src = urlPrevia;
    vistaPrevia.hidden = false;
    if (contenidoZona) contenidoZona.hidden = true;
    if (nombreArchivo) {
      nombreArchivo.textContent = archivo.name;
      nombreArchivo.hidden = false;
    }
  }

  function abrirSelectorImagen() {
    if (inputFoto) inputFoto.click();
  }

  if (selectJardin && selectEdificio) {
    selectJardin.addEventListener('change', filtrarEdificios);
    selectEdificio.addEventListener('change', mostrarUbicacion);
    filtrarEdificios();
    mostrarUbicacion();
  }

  if (toggleOcupado && inputStatus) {
    toggleOcupado.addEventListener('change', sincronizarEstado);
    sincronizarEstado();
  }

  if (zonaImagen && inputFoto) {
    zonaImagen.addEventListener('click', abrirSelectorImagen);
    zonaImagen.addEventListener('keydown', (evento) => {
      if (evento.key === 'Enter' || evento.key === ' ') {
        evento.preventDefault();
        abrirSelectorImagen();
      }
    });
    zonaImagen.addEventListener('dragover', (evento) => {
      evento.preventDefault();
      zonaImagen.classList.add('zona-activa');
    });
    zonaImagen.addEventListener('dragleave', () => {
      zonaImagen.classList.remove('zona-activa');
    });
    zonaImagen.addEventListener('drop', (evento) => {
      evento.preventDefault();
      zonaImagen.classList.remove('zona-activa');
      if (evento.dataTransfer.files.length > 0) {
        inputFoto.files = evento.dataTransfer.files;
        mostrarVistaPrevia(evento.dataTransfer.files[0]);
      }
    });
    inputFoto.addEventListener('change', () => {
      if (inputFoto.files.length > 0) mostrarVistaPrevia(inputFoto.files[0]);
    });
  }

  if (botonSubir) {
    botonSubir.addEventListener('click', abrirSelectorImagen);
  }
})();