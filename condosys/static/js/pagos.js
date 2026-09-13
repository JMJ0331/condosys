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
  const btnComprobante = document.querySelector('[data-url-comprobante]');
  if (!btnComprobante) return;

  const formPago = btnComprobante.closest('form');
  if (!formPago) return;

  const selectApartamento = formPago.querySelector('[data-pago-apartamento]');
  const selectResidente = formPago.querySelector('[data-pago-residente]');
  const inputComprobante = formPago.querySelector('[name="receipt_image"]');
  const camposRequeridos = ['apartment', 'resident', 'amount', 'concept', 'period', 'status'];

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

  if (selectApartamento && selectResidente) {
    selectApartamento.addEventListener('change', filtrarResidentes);
    filtrarResidentes();
  }

  function formPagoCompleto() {
    return camposRequeridos.every((nombre) => {
      const el = formPago.querySelector(`[name="${nombre}"]`);
      return el && el.value && el.value.trim() !== '';
    });
  }

  function actualizarBloqueoComprobante() {
    const completo = formPagoCompleto();
    btnComprobante.disabled = !completo;
    if (inputComprobante) inputComprobante.disabled = !completo;
  }

  camposRequeridos.forEach((nombre) => {
    const el = formPago.querySelector(`[name="${nombre}"]`);
    if (el) {
      el.addEventListener('change', actualizarBloqueoComprobante);
      el.addEventListener('input', actualizarBloqueoComprobante);
    }
  });

  actualizarBloqueoComprobante();

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