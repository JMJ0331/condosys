/**
 * Lógica específica del módulo Departamentos (structure).
 * - Página index (#filtros-departamentos): selector de columnas + auto-submit filtros.
 * - Página agregar: cascada Jardín → Torre/Bloque → Edificio, zona de
 *   imagen e interruptor ocupado.
 *
 * La plantilla agregar.html debe usar:
 *   - <select id="select-jardin">
 *   - <select id="torre-departamento" data-departamento="torre">
 *   - <select id="bloque-departamento" data-departamento="bloque">
 *   - <select data-departamento="edificio">     (sus opciones llevan
 *     data-garden, data-torre y data-bloque)
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
  const selectTorre = document.getElementById('torre-departamento');
  const selectBloque = document.getElementById('bloque-departamento');
  const toggleOcupado = document.getElementById('toggle-ocupado');
  const inputStatus = document.getElementById('id_status');
  const zonaImagen = document.getElementById('zona-imagen');
  const inputFoto = document.querySelector('[data-departamento="foto"]');
  const botonSubir = document.getElementById('boton-subir-imagen');
  const vistaPrevia = document.getElementById('vista-previa-imagen');
  const contenidoZona = document.getElementById('contenido-zona');
  const nombreArchivo = document.getElementById('nombre-archivo');
  let urlPrevia = null;

  // Valores distintos de una dimensión (torre o bloque) entre los edificios
  // del jardín elegido. Fuente temporal hasta que torre/bloque se administren
  // desde el sidebar.
  function valoresDimension(atributo) {
    if (!selectEdificio) return [];
    const jardin = selectJardin ? selectJardin.value : '';
    const valores = new Set();
    selectEdificio.querySelectorAll('option[data-garden]').forEach((opt) => {
      if (jardin !== '' && opt.dataset.garden !== jardin) return;
      const valor = (opt.dataset[atributo] || '').trim();
      if (valor !== '') valores.add(valor);
    });
    return [...valores].sort((a, b) => a.localeCompare(b, 'es'));
  }

  // Reconstruye el select de una dimensión con los valores del jardín.
  // Sin valores (el residencial no usa esa dimensión), queda deshabilitado
  // con un texto que lo indica en vez de ocultarse.
  function reconstruirDimension(select, atributo, placeholder, sinTexto) {
    if (!select || !selectEdificio) return;
    const actual = select.value;
    const valores = valoresDimension(atributo);
    select.innerHTML = '';
    const inicial = document.createElement('option');
    inicial.value = '';
    if (valores.length === 0) {
      inicial.textContent = sinTexto;
      select.appendChild(inicial);
      select.value = '';
      select.disabled = true;
      return;
    }
    inicial.textContent = placeholder;
    select.appendChild(inicial);
    valores.forEach((valor) => {
      const opt = document.createElement('option');
      opt.value = valor;
      opt.textContent = valor;
      select.appendChild(opt);
    });
    select.disabled = false;
    select.value = valores.includes(actual) ? actual : '';
  }

  function filtrarEdificios() {
    if (!selectJardin || !selectEdificio) return;
    const jardin = selectJardin.value;
    const torre = selectTorre ? selectTorre.value : '';
    const bloque = selectBloque ? selectBloque.value : '';
    selectEdificio.querySelectorAll('option[data-garden]').forEach((opt) => {
      const coincideJardin = jardin === '' || opt.dataset.garden === jardin;
      const coincideTorre = torre === '' || (opt.dataset.torre || '').trim() === torre;
      const coincideBloque = bloque === '' || (opt.dataset.bloque || '').trim() === bloque;
      opt.hidden = !(coincideJardin && coincideTorre && coincideBloque);
    });
    const elegida = selectEdificio.selectedOptions[0];
    if (elegida && elegida.value !== '' && elegida.hidden) {
      selectEdificio.value = '';
    }
  }

  // Jardín reconstruye las dimensiones y filtra edificios;
  // torre/bloque solo filtran edificios.
  function filtrarUbicacion() {
    reconstruirDimension(selectTorre, 'torre', 'Torre', 'Sin torres');
    reconstruirDimension(selectBloque, 'bloque', 'Bloque', 'Sin bloques');
    filtrarEdificios();
  }

  // En actualizar, la plantilla marca el jardín/torre/bloque del departamento
  // en data-actual: se preseleccionan una vez al cargar sin tocar lo que el
  // usuario ya haya elegido.
  function preseleccionarUbicacion() {
    if (!selectJardin || selectJardin.value !== '' || !selectJardin.dataset.actual) return;
    selectJardin.value = selectJardin.dataset.actual;
    filtrarUbicacion();
    [[selectTorre], [selectBloque]].forEach(([select]) => {
      if (!select || !select.dataset.actual) return;
      const valor = select.dataset.actual;
      if ([...select.options].some((opt) => opt.value === valor)) {
        select.value = valor;
      }
    });
    filtrarEdificios();
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
    selectJardin.addEventListener('change', filtrarUbicacion);
    filtrarUbicacion();
    preseleccionarUbicacion();
  }

  if (selectTorre && selectEdificio) {
    selectTorre.addEventListener('change', filtrarEdificios);
  }

  if (selectBloque && selectEdificio) {
    selectBloque.addEventListener('change', filtrarEdificios);
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