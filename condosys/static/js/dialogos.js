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
  document.querySelectorAll('[data-dialog]').forEach((accion) => {
    accion.addEventListener('click', () => {
      const dialog = document.getElementById(accion.dataset.dialog);
      if (dialog && typeof dialog.showModal === 'function') {
        dialog.showModal();
      }
    });
  });

  document.querySelectorAll('[data-dialog-close]').forEach((boton) => {
    boton.addEventListener('click', () => boton.closest('dialog')?.close());
  });

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