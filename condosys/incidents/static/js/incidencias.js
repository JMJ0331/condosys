/**
 * Lógica del formulario de incidencias.
 *
 * La plantilla debe insertar en el formulario:
 *   - un <select> con data-incidencia-apartamento
 *   - un <select> con data-incidencia-residente (sus opciones llevan data-apartment)
 *   - un input[type="file"] con data-evidencia y un span data-texto-evidencia
 *
 * No usa variables de plantilla directamente para poder vivir en static/js.
 */

(() => {
  const inputEvidencia = document.querySelector('[data-evidencia]');
  if (!inputEvidencia) return;

  // Subimos al <form> que contiene al input de evidencia para filtrar los
  // campos dentro de él (evita tocar otros formularios de la página).
  const formIncidencia = inputEvidencia.closest('form');
  if (!formIncidencia) return;

  const selectApartamento = formIncidencia.querySelector('[data-incidencia-apartamento]');
  const selectResidente = formIncidencia.querySelector('[data-incidencia-residente]');

  // Muestra solo los residentes del apartamento elegido (cada <option> declara
  // su apartamento en data-apartment). Si el residente seleccionado ya no
  // corresponde, lo deseleccionamos para forzar una elección válida.
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

  if (selectApartamento && selectResidente) {
    selectApartamento.addEventListener('change', filtrarResidentes);
    filtrarResidentes();
  }

  // Muestro el nombre del archivo elegido sobre el botón de subida.
  function mostrarNombreArchivo() {
    const span = inputEvidencia.closest('label')?.querySelector('[data-texto-evidencia]');
    if (!span) return;
    if (inputEvidencia.files.length > 0) {
      span.textContent = inputEvidencia.files[0].name;
    } else {
      span.textContent = 'Subir imagen/archivo';
    }
  }

  inputEvidencia.addEventListener('change', mostrarNombreArchivo);
})();