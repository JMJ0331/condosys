/**
 * Acciones del encabezado en móvil (<=560px).
 * En escritorio viven a la derecha del encabezado (.app-header);
 * en móvil se trasladan al final del formulario (debajo del último
 * panel), apiladas a ancho completo (ver acciones.css), y vuelven
 * al encabezado al agrandar la pantalla.
 *
 * Requiere:
 *   - <div class="acciones-encabezado"> con un <button type="submit" form="...">
 * Solo actúa si existe; en páginas sin acciones no hace nada.
 * No usa etiquetas de plantilla Django.
 */

(() => {
  const CONSULTA_MOVIL = '(max-width: 560px)';

  function colocarAcciones(esMovil) {
    document.querySelectorAll('.acciones-encabezado').forEach((acciones) => {
      const botonEnviar = acciones.querySelector('button[type="submit"]');
      const formulario = botonEnviar ? botonEnviar.form : null;

      // Guarda la posición original la primera vez para poder restaurarla.
      if (acciones.dataset.padreOrigen === undefined) {
        const padre = acciones.parentElement;
        if (!padre) return;
        acciones.dataset.padreOrigen = '';
        acciones._padreOrigen = padre;
        acciones._siguienteOrigen = acciones.nextElementSibling;
      }

      if (esMovil && formulario) {
        formulario.appendChild(acciones);
        acciones.classList.add('acciones-abajo');
      } else {
        acciones._padreOrigen.insertBefore(acciones, acciones._siguienteOrigen);
        acciones.classList.remove('acciones-abajo');
      }
    });
  }

  const consulta = window.matchMedia(CONSULTA_MOVIL);
  colocarAcciones(consulta.matches);
  consulta.addEventListener('change', (evento) => colocarAcciones(evento.matches));
})();
