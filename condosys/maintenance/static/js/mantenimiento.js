/**
 * Lógica del formulario de cargo de mantenimiento.
 *
 * La plantilla debe insertar en el formulario:
 *   - un input[type="file"] con data-foto-mantenimiento
 *   - un span con data-texto-archivo dentro de la misma etiqueta <label>
 *
 * No usa variables de plantilla directamente para poder vivir en static/js.
 */

(() => {
  const inputFoto = document.querySelector('[data-foto-mantenimiento]');
  if (!inputFoto) return;

  // Muestro el nombre de la imagen elegida sobre el botón de subida.
  function mostrarNombreArchivo() {
    const span = inputFoto.closest('label')?.querySelector('[data-texto-archivo]');
    if (!span) return;
    if (inputFoto.files.length > 0) {
      span.textContent = inputFoto.files[0].name;
    } else {
      span.textContent = 'Subir imagen';
    }
  }

  inputFoto.addEventListener('change', mostrarNombreArchivo);
})();