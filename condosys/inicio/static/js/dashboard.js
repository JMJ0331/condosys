/**
 * Lógica específica del dashboard (inicio).
 * Envío automático de los filtros de búsqueda al cambiar de jardín, edificio o departamento.
 *
 * La plantilla debe usar un formulario con class="contenedor-busqueda"
 * y selects con id garden-select / building-select / apartment-select.
 */
(() => {
  const formulario = document.querySelector('.contenedor-busqueda');
  if (!formulario) return;

  formulario.querySelectorAll('#garden-select, #building-select, #apartment-select').forEach((select) => {
    select.addEventListener('change', () => formulario.submit());
  });
})();