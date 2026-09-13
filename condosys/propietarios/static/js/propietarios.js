/**
 * Lógica específica del módulo Propietarios.
 * Selector de columnas visibles + envío automático de filtros.
 *
 * La plantilla debe usar:
 *   - <select id="filtro-columnas">              (0 = todas, n = primeras n columnas)
 *   - <form id="filtros-propietarios">           (se enviará al cambiar filtros)
 *   - celdas con data-columna="clave"
 */
(() => {
  const formularioFiltros = document.getElementById('filtros-propietarios');
  if (formularioFiltros) {
    formularioFiltros.querySelectorAll('select').forEach((select) => {
      select.addEventListener('change', () => formularioFiltros.submit());
    });
  }

  const selectColumnas = document.getElementById('filtro-columnas');
  if (!selectColumnas) return;

  const columnas = Array.from(document.querySelectorAll('th[data-columna]'))
    .map((th) => th.dataset.columna);

  function aplicarColumnas() {
    const cantidad = Number(selectColumnas.value);
    columnas.forEach((columna, index) => {
      const visibles = cantidad === 0 || index < cantidad;
      document.querySelectorAll(`[data-columna="${columna}"]`).forEach((celda) => {
        celda.style.display = visibles ? '' : 'none';
      });
    });
  }

  selectColumnas.addEventListener('change', aplicarColumnas);
})();