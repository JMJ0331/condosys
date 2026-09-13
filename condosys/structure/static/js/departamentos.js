/**
 * Lógica específica del módulo Departamentos (structure).
 * Filtros de jardín/edificio, búsqueda de propietario y estado ocupado.
 *
 * La plantilla debe usar:
 *   - <select id="select-jardin">
 *   - <select data-departamento="edificio">     (sus opciones llevan data-garden)
 *   - <select data-departamento="propietario">
 *   - <input id="buscar-residente">
 *   - <input type="checkbox" id="toggle-ocupado">
 *   - <input type="hidden" id="id_status">
 */
(() => {
  const selectJardin = document.getElementById('select-jardin');
  const selectEdificio = document.querySelector('[data-departamento="edificio"]');
  const selectPropietario = document.querySelector('[data-departamento="propietario"]');
  const inputBuscarResidente = document.getElementById('buscar-residente');
  const toggleOcupado = document.getElementById('toggle-ocupado');
  const inputStatus = document.getElementById('id_status');

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
  }

  function mostrarUbicacion() {
    if (!selectEdificio) return;
    const opt = selectEdificio.selectedOptions[0];
    const jardinNombre = opt ? opt.textContent.split(' · ')[0] : '—';
    const infoJardin = document.getElementById('info-jardin');
    const infoUbicacion = document.getElementById('info-ubicacion');
    if (infoJardin) {
      infoJardin.textContent = `Jardín: ${jardinNombre}`;
    }
    if (infoUbicacion) {
      infoUbicacion.textContent =
        `Edificio: ${opt ? opt.value : '—'} · Bloque: ${opt ? opt.textContent.split('Bloque ')[1] || '—' : '—'}`;
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