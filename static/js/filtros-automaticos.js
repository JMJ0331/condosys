/**
 * Formularios de filtros con [data-envio-automatico]: se envían al cambiar
 * cualquier select. Debe cargarse después de cascada.js para que la cascada
 * limpie primero los niveles inferiores que ya no aplican.
 */

(() => {
  document.querySelectorAll('form[data-envio-automatico]').forEach((formulario) => {
    formulario.querySelectorAll('select').forEach((select) => {
      select.addEventListener('change', () => formulario.submit());
    });
  });
})();
