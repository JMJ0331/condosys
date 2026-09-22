/**
 * Lógica del área de reportes (/reportes/).
 * - La lista "Reportes disponibles" cambia el tipo y genera el reporte.
 * - Las barras del gráfico toman su altura de data-altura (sin style inline).
 *
 * Sin etiquetas de plantilla Django: solo usa IDs y atributos data-*.
 */
(() => {
  const formulario = document.getElementById('filtros-reportes');
  const selectorTipo = document.getElementById('filtro-tipo');

  if (formulario && selectorTipo) {
    document.querySelectorAll('[data-tipo]').forEach((enlace) => {
      enlace.addEventListener('click', () => {
        selectorTipo.value = enlace.dataset.tipo;
        formulario.submit();
      });
    });
  }

  document.querySelectorAll('.relleno-barra[data-altura]').forEach((barra) => {
    const altura = Number.parseInt(barra.dataset.altura, 10);
    barra.style.height = `${Number.isNaN(altura) ? 0 : Math.min(Math.max(altura, 0), 100)}%`;
  });

  const selectorMes = document.getElementById('selector-mes');
  const totalMes = document.getElementById('total-mes');
  if (selectorMes && totalMes) {
    selectorMes.addEventListener('change', () => {
      const elegida = selectorMes.selectedOptions[0];
      if (elegida && elegida.dataset.total) totalMes.textContent = elegida.dataset.total;
    });
  }
})();
