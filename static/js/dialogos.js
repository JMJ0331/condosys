/**
 * Lógica compartida de diálogos <dialog>.
 *
 * La plantilla debe usar:
 *   - botones con data-dialog="id-del-dialog"   -> abren el diálogo (showModal)
 *   - botones con data-dialog-close             -> cierran el diálogo más cercano
 *
 * El clic fuera del área del diálogo lo cierra.
 */
(() => {
  // Apertura: cada botón con data-dialog="id" abre el <dialog> con ese id usando
  // showModal (modal con fondo oscuro y bloqueo del resto de la página).
  document.querySelectorAll('[data-dialog]').forEach((accion) => {
    accion.addEventListener('click', () => {
      const dialog = document.getElementById(accion.dataset.dialog);
      // showModal no existe en navegadores muy antiguos; en ese caso simplemente no hacemos nada.
      if (dialog && typeof dialog.showModal === 'function') {
        dialog.showModal();
      }
    });
  });

  // Cierre: cualquier botón con data-dialog-close cierra el <dialog> en el que está.
  document.querySelectorAll('[data-dialog-close]').forEach((boton) => {
    boton.addEventListener('click', () => boton.closest('dialog')?.close());
  });

  // Cierre por clic fuera: se compara la posición del clic con el rectángulo del
  // diálogo; si el clic cae fuera de ese rectángulo, se cierra el diálogo.
  document.querySelectorAll('dialog').forEach((dialog) => {
    dialog.addEventListener('click', (event) => {
      const rect = dialog.getBoundingClientRect();
      const dentro =
        event.clientX >= rect.left &&
        event.clientX <= rect.right &&
        event.clientY >= rect.top &&
        event.clientY <= rect.bottom;
      if (!dentro) {
        dialog.close();
      }
    });
  });
})();