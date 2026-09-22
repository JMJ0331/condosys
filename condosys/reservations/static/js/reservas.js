/**
 * Lógica del formulario de reservas.
 *
 * La plantilla debe insertar en el formulario:
 *   - un <select> con data-reserva-area (opciones con data-horario,
 *     data-dias-val y data-dias)
 *   - un <select> con data-reserva-apartamento
 *   - un <select> con data-reserva-residente (sus opciones llevan data-apartment)
 *   - un <p> con id="aviso-horario-area"
 *   - inputs fecha_reserva, hora_inicio y hora_fin
 *
 * Filtra los propietarios/residentes según el apartamento, muestra el horario
 * permitido del área seleccionada y bloquea el envío si la fecha u hora queda
 * fuera del horario de esa área (el servidor también valida, por seguridad).
 *
 * Página index (#filtros-reservas): selector de columnas + auto-submit filtros.
 */

(() => {
  const form = document.querySelector('form[data-form-reserva]');
  if (!form) return;

  const selectApartamento = form.querySelector('[data-reserva-apartamento]');
  const selectResidente = form.querySelector('[data-reserva-residente]');
  const selectArea = form.querySelector('[data-reserva-area]');
  const aviso = form.querySelector('#aviso-horario-area');
  const inputFecha = form.querySelector('input[name="fecha_reserva"]');
  const inputHoraInicio = form.querySelector('input[name="hora_inicio"]');
  const inputHoraFin = form.querySelector('input[name="hora_fin"]');

  // ---------- Filtro propietarios/residentes por apartamento ----------
  function filtrarResidentes() {
    if (!selectApartamento || !selectResidente) return;
    const apartamento = selectApartamento.value;
    selectResidente.querySelectorAll('option[data-apartment]').forEach((opt) => {
      opt.hidden = apartamento !== '' && opt.dataset.apartment !== apartamento;
    });
    if (
      selectResidente.selectedOptions[0]?.dataset.apartment &&
      selectResidente.value !== '' &&
      selectResidente.selectedOptions[0].dataset.apartment !== apartamento
    ) {
      selectResidente.value = '';
    }
  }

  // ---------- Avance del horario del área seleccionada ----------
  function actualizarAvisoArea() {
    if (!selectArea || !aviso) return;
    const opt = selectArea.selectedOptions[0];
    if (!opt || !opt.value) {
      aviso.textContent = '';
      aviso.classList.remove('error');
      return;
    }
    const horario = opt.dataset.horario;
    const dias = opt.dataset.dias;
    aviso.textContent = `Horario permitido: ${horario || 'sin definir'} · Días: ${dias}`;
    aviso.classList.remove('error');
  }

  // ---------- Validación de horario y fecha contra el área ----------
  function areaSeleccionada() {
    if (!selectArea) return null;
    const opt = selectArea.selectedOptions[0];
    if (!opt || !opt.value) return null;
    return {
      horario: opt.dataset.horario || '',
      diasVal: opt.dataset.diasVal || '',
    };
  }

  function validarReserva() {
    const area = areaSeleccionada();
    if (!area) return true;

    const partes = area.horario.split(' - ');
    if (partes.length === 2 && partes[0] && partes[1]) {
      const inicio = inputHoraInicio ? inputHoraInicio.value : '';
      const fin = inputHoraFin ? inputHoraFin.value : '';
      if (inicio && inicio < partes[0]) {
        aviso.textContent = `No se puede reservar: la hora de inicio está antes del horario permitido (${area.horario}).`;
        aviso.classList.add('error');
        return false;
      }
      if (fin && fin > partes[1]) {
        aviso.textContent = `No se puede reservar: la hora de fin está después del horario permitido (${area.horario}).`;
        aviso.classList.add('error');
        return false;
      }
    }

    if (inputFecha && inputFecha.value) {
      const diaSemana = new Date(inputFecha.value + 'T00:00:00').getDay();
      if (area.diasVal === 'lun_vie' && (diaSemana === 0 || diaSemana === 6)) {
        aviso.textContent = 'No se puede reservar: esa área solo está disponible de lunes a viernes.';
        aviso.classList.add('error');
        return false;
      }
      if (area.diasVal === 'fines_semana' && diaSemana >= 1 && diaSemana <= 5) {
        aviso.textContent = 'No se puede reservar: esa área solo está disponible los fines de semana.';
        aviso.classList.add('error');
        return false;
      }
    }
    return true;
  }

  if (selectApartamento && selectResidente) {
    selectApartamento.addEventListener('change', filtrarResidentes);
    filtrarResidentes();
  }

  if (selectArea) {
    selectArea.addEventListener('change', actualizarAvisoArea);
    actualizarAvisoArea();
  }

  form.addEventListener('submit', (event) => {
    if (selectArea && !validarReserva()) {
      event.preventDefault();
      selectArea.focus();
    }
  });
})();

/**
 * Página index: selector de columnas visibles + auto-submit de filtros.
 * Bloque independiente: solo actúa si existe #filtros-reservas.
 */
(() => {
  const formularioFiltros = document.getElementById('filtros-reservas');
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
})();