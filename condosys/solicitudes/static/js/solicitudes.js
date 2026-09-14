/**
 * Lógica del formulario de solicitudes.
 *
 * La plantilla debe insertar en el formulario:
 *   - un <select> con data-solicitud-apartamento
 *   - un <select> con data-solicitud-residente (sus opciones llevan data-apartment)
 *   - un input[type="file"] con data-solicitud-documento y un span data-texto-archivo
 *
 * No usa variables de plantilla directamente para poder vivir en static/js.
 */

(() => {
  const inputDocumento = document.querySelector('[data-solicitud-documento]');
  if (!inputDocumento) return;

  // Subimos al <form> que contiene al input de documento para filtrar los
  // campos dentro de él (evita tocar otros formularios de la página).
  const formSolicitud = inputDocumento.closest('form');
  if (!formSolicitud) return;

  const selectApartamento = formSolicitud.querySelector('[data-solicitud-apartamento]');
  const selectResidente = formSolicitud.querySelector('[data-solicitud-residente]');

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
    const span = inputDocumento.closest('label')?.querySelector('[data-texto-archivo]');
    if (!span) return;
    if (inputDocumento.files.length > 0) {
      span.textContent = inputDocumento.files[0].name;
    } else {
      span.textContent = 'Subir imagen/archivo';
    }
  }

  inputDocumento.addEventListener('change', mostrarNombreArchivo);
})();