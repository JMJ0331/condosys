/**
 * Lógica específica del módulo Residentes.
 * Selector de columnas visibles + envío automático de filtros.
 *
 * La plantilla debe usar:
 *   - <select id="filtro-columnas">              (0 = todas, n = primeras n columnas)
 *   - <form id="filtros-residentes">             (se enviará al cambiar filtros)
 *   - celdas con data-columna="clave"
 */
(() => {
  const formularioFiltros = document.getElementById('filtros-residentes');
  if (formularioFiltros) {
    // Envío automático de los filtros: al cambiar cualquier select del formulario
    // se reenvía con la nueva selección (sustituye a onchange="form.submit()").
    formularioFiltros.querySelectorAll('select').forEach((select) => {
      select.addEventListener('change', () => formularioFiltros.submit());
    });
  }

  const selectColumnas = document.getElementById('filtro-columnas');
  if (!selectColumnas) return;

  // Recoge las claves de columna declaradas en los <th> para poder ocultarlas por nombre.
  const columnas = Array.from(document.querySelectorAll('th[data-columna]'))
    .map((th) => th.dataset.columna);

  // Oculta o muestra columnas según el valor elegido:
  //   0 = mostrar todas; n = mostrar solo las primeras n columnas.
  // Se aplica a todas las celdas y cabeceras que compartan el mismo data-columna.
  function aplicarColumnas() {
    const cantidad = Number(selectColumnas.value);
    columnas.forEach((columna, index) => {
      const visibles = cantidad === 0 || index < cantidad;
      document.querySelectorAll(`[data-columna="${columna}"]`).forEach((celda) => {
        celda.style.display = visibles ? '' : 'none';
      });
    });
  }

  // Aplicar la visibilidad escogida en cuanto cambie el selector.
  selectColumnas.addEventListener('change', aplicarColumnas);
})();