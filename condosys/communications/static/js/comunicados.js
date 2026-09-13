/**
 * Lógica del formulario de comunicado.
 *
 * La plantilla debe insertar en el formulario:
 *   - un input[type="file"] con data-imagen-comunicado
 *   - un span con data-texto-archivo dentro de la misma etiqueta <label>
 */

(() => {
  const inputImagen = document.querySelector('[data-imagen-comunicado]');
  if (!inputImagen) return;

  function mostrarNombreArchivo() {
    const span = inputImagen.closest('label')?.querySelector('[data-texto-archivo]');
    if (!span) return;
    span.textContent = inputImagen.files.length > 0 ? inputImagen.files[0].name : 'Subir imagen';
  }

  inputImagen.addEventListener('change', mostrarNombreArchivo);
})();