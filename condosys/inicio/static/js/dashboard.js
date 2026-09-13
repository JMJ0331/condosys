/**
 * Lógica específica del dashboard (inicio).
 * Envío automático de los filtros de búsqueda al cambiar de jardín, edificio o departamento.
 *
 * La plantilla debe usar un formulario con class="contenedor-busqueda"
 * y selects con id garden-select / building-select / apartment-select.
 */
(() => {
  // Buscamos el formulario de búsqueda del dashboard (filtros de residentes).
  const formulario = document.querySelector('.contenedor-busqueda');
  if (!formulario) return;

  // Los selects de jardín, edificio y departamento filtran por querystring;
  // al cambiarlos se envía el formulario automáticamente (como hacía onchange="this.form.submit()").
  formulario.querySelectorAll('#garden-select, #building-select, #apartment-select').forEach((select) => {
    select.addEventListener('change', () => formulario.submit());
  });
})();