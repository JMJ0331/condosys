/**
 * Configuración: pestañas + selector de columnas visibles.
 * El selector replica el comportamiento de los demás módulos:
 * botón que abre un panel con una casilla por columna + casilla "Todas".
 */
(() => {
  const contenedor = document.querySelector('[data-pestanas]');
  if (contenedor) {
    const pestanas = Array.from(contenedor.querySelectorAll('[data-pestana]'));
    const paneles = Array.from(document.querySelectorAll('[data-panel]'));

    function mostrar(clave) {
      pestanas.forEach((pestana) => {
        const activa = pestana.dataset.pestana === clave;
        pestana.classList.toggle('pestana-activa', activa);
        pestana.setAttribute('aria-selected', String(activa));
      });
      paneles.forEach((panel) => {
        const visible = panel.dataset.panel === clave;
        panel.classList.toggle('panel-activo', visible);
        if (visible) {
          panel.removeAttribute('hidden');
        } else {
          panel.setAttribute('hidden', '');
        }
      });
    }

    pestanas.forEach((pestana) => {
      pestana.addEventListener('click', () => mostrar(pestana.dataset.pestana));
    });
  }

  const botonColumnas = document.getElementById('boton-columnas');
  const panelColumnas = document.getElementById('panel-columnas');
  const toggleTodas = document.getElementById('toggle-todas-columnas');
  const formularioFiltros = document.getElementById('filtros-usuarios');

  if (formularioFiltros) {
    formularioFiltros.querySelectorAll('select').forEach((select) => {
      select.addEventListener('change', () => formularioFiltros.submit());
    });
  }

  // Integración AI: al guardar se detecta si el input API Key trae valor.
  // Vacío y sin clave guardada -> se bloquea el envío con un aviso;
  // vacío con clave guardada -> se envía para conservar la actual.
  const formularioIA = document.querySelector('.formulario-ia');
  if (formularioIA) {
    const inputClave = formularioIA.querySelector('input[name="api_key"]');
    const errorClave = document.getElementById('error-ia-clave');
    const configurada = formularioIA.dataset.iaConfigurada === '1';

    // Sugerencias dependientes: al elegir proveedor se listan sus modelos
    // conocidos en el datalist; el campo queda libre para IDs nuevos.
    const selectProveedor = formularioIA.querySelector('select[name="proveedor"]');
    const inputModelo = formularioIA.querySelector('input[name="modelo"]');
    const listaModelos = document.getElementById('lista-modelos');
    if (selectProveedor && inputModelo && listaModelos) {
      let modelos = {};
      try {
        modelos = JSON.parse(formularioIA.dataset.modelos || '{}');
      } catch (error) {
        modelos = {};
      }

      function poblarModelos() {
        const lista = modelos[selectProveedor.value] || [];
        listaModelos.innerHTML = '';
        lista.forEach(([valor, texto]) => {
          const opcion = document.createElement('option');
          opcion.value = valor;
          opcion.label = texto;
          listaModelos.appendChild(opcion);
        });
        if (lista.length > 0) {
          inputModelo.placeholder = `Ej.: ${lista[0][0]}`;
          inputModelo.disabled = false;
        } else {
          inputModelo.placeholder = 'Sin modelos de visión';
          inputModelo.disabled = true;
        }
      }

      poblarModelos();
      selectProveedor.addEventListener('change', poblarModelos);
    }

    formularioIA.addEventListener('submit', (evento) => {
      const vacia = !inputClave || inputClave.value.trim() === '';
      if (vacia && !configurada) {
        evento.preventDefault();
        if (errorClave) errorClave.hidden = false;
        if (inputClave) inputClave.focus();
      }
    });

    if (inputClave) {
      inputClave.addEventListener('input', () => {
        if (errorClave && inputClave.value.trim() !== '') errorClave.hidden = true;
      });
    }

    // Ojo ver/no ver: alterna el tipo del input entre password y texto.
    const botonOjo = document.getElementById('boton-ojo-clave');
    const iconoAbierto = document.getElementById('icono-ojo-abierto');
    const iconoCerrado = document.getElementById('icono-ojo-cerrado');
    if (botonOjo && inputClave) {
      // En <svg> la propiedad .hidden no refleja al atributo: se alterna
      // el atributo directamente para que el CSS lo muestre/oculte.
      function alternarIconos(mostrar, ocultar) {
        if (mostrar) mostrar.removeAttribute('hidden');
        if (ocultar) ocultar.setAttribute('hidden', '');
      }
      botonOjo.addEventListener('click', () => {
        const visible = inputClave.type === 'text';
        inputClave.type = visible ? 'password' : 'text';
        botonOjo.setAttribute('aria-pressed', String(!visible));
        botonOjo.setAttribute('aria-label', visible ? 'Mostrar API Key' : 'Ocultar API Key');
        if (visible) {
          alternarIconos(iconoAbierto, iconoCerrado);
        } else {
          alternarIconos(iconoCerrado, iconoAbierto);
        }
      });
    }
  }

  if (!botonColumnas || !panelColumnas) return;

  const columnas = Array.from(document.querySelectorAll('th[data-columna]'))
    .map((th) => ({ nombre: th.dataset.columna, texto: th.textContent.trim() }))
    .filter(({ nombre }) => nombre !== 'acciones');

  const casillas = new Map();
  columnas.forEach(({ nombre, texto }) => {
    const etiqueta = document.createElement('label');
    const casilla = document.createElement('input');
    const textoColumna = document.createElement('span');
    etiqueta.className = 'opcion-columna';
    casilla.type = 'checkbox';
    casilla.checked = true;
    textoColumna.textContent = texto;
    etiqueta.append(casilla, textoColumna);
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
})();
