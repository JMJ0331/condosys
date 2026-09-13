/**
 * Lógica compartida del formulario de pagos.
 * Usado por el módulo de pagos y por el dashboard (inicio).
 *
 * La plantilla debe insertar en el formulario:
 *   - un control <select> con data-pago-apartamento
 *   - un <select> con data-pago-residente  (sus opciones llevan data-apartment)
 *   - un botón con data-url-comprobante="{% url 'generar_comprobante' %}"
 *
 * No usa variables de plantilla directamente para poder vivir en static/js.
 */

(() => {
  // El botón de comprobante trae en data-url-comprobante la URL de la vista Django.
  // Si no está presente, no hay formulario de pago en la página y salimos.
  const btnComprobante = document.querySelector('[data-url-comprobante]');
  if (!btnComprobante) return;

  // Subimos al <form> que contiene al botón para filtrar los campos dentro de él
  // (evita tocar otros formularios con nombres similares en la misma página).
  const formPago = btnComprobante.closest('form');
  if (!formPago) return;

  const selectApartamento = formPago.querySelector('[data-pago-apartamento]');
  const selectResidente = formPago.querySelector('[data-pago-residente]');
  const inputComprobante = formPago.querySelector('[name="receipt_image"]');

  // Campos que deben tener valor para habilitar el botón "Generar comprobante".
  const camposRequeridos = ['apartment', 'resident', 'amount', 'concept', 'period', 'status'];

  // Muestra solo los residentes del apartamento elegido (cada <option> declara su
  // apartamento en data-apartment). Si el residente seleccionado ya no corresponde,
  // lo deseleccionamos para forzar una elección válida.
  function filtrarResidentes() {
    if (!selectApartamento || !selectResidente) return;
    const apartamento = selectApartamento.value;
    selectResidente.querySelectorAll('option[data-apartment]').forEach((opt) => {
      opt.hidden = apartamento !== '' && opt.dataset.apartment !== apartamento;
    });
    if (
      selectResidente.selectedOptions[0]?.dataset.apartment &&
      selectResidente.value !== '' &&
      selectResidente.selectedOptions[0].dataset.apartment !== apartamento
    ) {
      selectResidente.value = '';
    }
  }

  // Enlazamos el filtro: cada vez que cambia el apartamento se re-filtran residentes.
  if (selectApartamento && selectResidente) {
    selectApartamento.addEventListener('change', filtrarResidentes);
    filtrarResidentes();
  }

  // true si todos los campos obligatorios tienen un valor no vacío.
  function formPagoCompleto() {
    return camposRequeridos.every((nombre) => {
      const el = formPago.querySelector(`[name="${nombre}"]`);
      return el && el.value && el.value.trim() !== '';
    });
  }

  // Deshabilita (o habilita) el botón de comprobante y el campo de imagen según
  // si el formulario está completo. Así evita generar PDFs con datos faltantes.
  function actualizarBloqueoComprobante() {
    const completo = formPagoCompleto();
    btnComprobante.disabled = !completo;
    if (inputComprobante) inputComprobante.disabled = !completo;
  }

  // Recalculamos el bloqueo cuando el usuario toque cualquiera de los campos clave.
  camposRequeridos.forEach((nombre) => {
    const el = formPago.querySelector(`[name="${nombre}"]`);
    if (el) {
      el.addEventListener('change', actualizarBloqueoComprobante);
      el.addEventListener('input', actualizarBloqueoComprobante);
    }
  });

  // Estado inicial (por si el formulario ya viene con datos).
  actualizarBloqueoComprobante();

  // Al pulsar "Generar comprobante" enviamos los valores del formulario como
  // query-string a la vista del PDF y lo abrimos en una pestaña nueva.
  btnComprobante.addEventListener('click', () => {
    const params = new URLSearchParams();
    [
      'apartment', 'resident', 'amount', 'concept',
      'period', 'payment_date', 'payment_method', 'status',
    ].forEach((nombre) => {
      const el = formPago.querySelector(`[name="${nombre}"]`);
      if (el && el.value) params.set(nombre, el.value);
    });
    window.open(`${btnComprobante.dataset.urlComprobante}?${params.toString()}`, '_blank');
  });
})();